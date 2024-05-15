"""
LensMC - a Python package for weak lensing shear measurements.
Module to process the input and output catalogue of LensMC.

Copyright 2015 Giuseppe Congedo
"""

import astropy.io.fits as fits
import multiprocessing as mp
import numpy as np
import os
import pickle
from astropy import wcs
from multiprocessing.pool import ThreadPool as Pool

from lensmc import __author__, __email__, __version__, __status__, __copyright__
from lensmc.segmentation import make_obj_segm
from lensmc.utils import LensmcMessage, LensmcError


def make_input_catalogue(detection_files, image_files, data_format='euclid', offset=4,
                         psf_files=None,
                         dir=dir, filename='input_catalogue.lmc',
                         cores=0, verbose=True):

    assert detection_files
    assert image_files
    assert '.lmc' in filename

    LensmcMessage('Make detections catalogue')

    # make merged detection catalogue
    detections_catalogue = make_detections_catalogue(detection_files,
                                                     data_format=data_format, cores=cores)

    # save
    fname = os.path.join(dir, filename.replace('.lmc', '.detections.lmc'))
    with open(fname, 'wb') as fo:
        pickle.dump(detections_catalogue, fo)
        fo.close()

    LensmcMessage('Make exposures catalogue')

    # make catalogue of exposures and central positions
    exposures_catalogue = make_exposures_catalogue(image_files,
                                                   psf_files=psf_files, data_format=data_format, cores=cores)
    exposures_catalogue = match_exposures_with_detections(exposures_catalogue, detections_catalogue,
                                                          offset=offset, cores=cores)

    LensmcMessage('Make segmentation maps for all exposures')

    exposures_catalogue = make_segmentation_maps(exposures_catalogue,
                                                 dir=os.path.join(dir, 'seg_maps'), cores=cores, verbose=verbose)

    # save
    fname = os.path.join(dir, filename.replace('.lmc', '.exposures.lmc'))
    with open(fname, 'wb') as fo:
        pickle.dump(exposures_catalogue, fo)
        fo.close()

    LensmcMessage('Make matched detections + exposures catalogue')

    matched_catalogue = match_detections_with_exposures(detections_catalogue, exposures_catalogue,
                                                        offset=offset, cores=cores, verbose=verbose)

    # save
    fname = os.path.join(dir, filename)
    with open(fname, 'wb') as fo:
        pickle.dump(matched_catalogue, fo)
        fo.close()

    # print end of the process
    LensmcMessage('Matched catalogue saved to \'' + fname + '\'')

    return matched_catalogue


def make_detections_catalogue(files, data_format='euclid', cores=0):

    # initialise output matched catalogue
    dtype = [('ID', np.chararray), ('RA', np.float32), ('DEC', np.float32), ('Star', np.uint32), ('LensMC_ID', np.uint32)]

    n_files = len(files)
    data = [None] * n_files

    # define worker to loop over catalogues
    def worker(ff):

        file = files[ff]

        # read in HDU list
        with fits.open(file) as hdulist:

            if data_format == 'euclid':

                # consistent with MER data format
                assert 'EUC_MER_FINAL-CAT' in file
                assert '.fits' in file

                # read catalogue entries
                id = hdulist[1].data['ObjectId']
                ra = hdulist[1].data['RightAscension']
                dec = hdulist[1].data['Declination']
                star_flag = hdulist[1].data['StarFlag']

                # redefine IDs
                tile = os.path.basename(os.path.dirname(file))
                fcn = lambda ii: '{}_{}'.format(tile, ii)
                id = np.array(list(map(fcn, id)))

                # save
                tempdata = np.recarray((len(id),), dtype=dtype)
                tempdata['ID'] = id
                tempdata['RA'] = ra
                tempdata['DEC'] = dec
                tempdata['Star'] = star_flag

                data[ff] = tempdata

            else:
                raise LensmcError('Format non recognised.')

        return

    if cores == 0:
        cores = mp.cpu_count()

    # run
    pool = Pool(cores)
    pool.map(worker, range(n_files))
    pool.close()
    pool.join()

    # collate
    data = np.concatenate(data)
    data = data.view(np.recarray)  # make sure we get a recarray

    # define LensMC internal ID
    data['LensMC_ID'] = np.arange(data.size)

    return data


def make_exposures_catalogue(image_files, psf_files=None, data_format='euclid', cores=0):

    # initialise output matched catalogue
    dtype = [('Exposure', np.chararray), ('RA', np.float32), ('DEC', np.float32), ('WCS', np.object),
             ('Mask', np.chararray), ('PSF', np.chararray)]

    n_files = len(image_files)
    data = [None] * n_files

    # define worker to loop over images
    def worker(ff):

        img_file = image_files[ff]

        # read in HDU list
        with fits.open(img_file) as hdulist:

            if data_format == 'euclid':

                # consistent with VIS data format
                assert 'EUC_VIS_SWL-DET' in img_file
                assert '.fits' in img_file

                # loop over FITS extensions for individual detector images
                # we have 6 x 6 CCDs
                ccd_rows, ccd_columns = 6, 6
                ccd_rows_columns = ccd_rows * ccd_columns
                tempdata = np.recarray((ccd_rows_columns,), dtype=dtype)
                for kk in range(ccd_rows_columns):

                    ii, jj = kk // ccd_rows + 1, kk % ccd_columns + 1

                    # define the FITS extension name that labels the CCD
                    ext = 'CCDID {:d}-{:d}.SCI'.format(ii, jj)

                    # get the header of a given detector
                    hdr = hdulist[ext].header

                    # fix VIS bug in WCS (won't be needed in future releases)
                    # uses TPV (Scamp like WCS) instead of TAN projection,
                    # which would break the subsequent line
                    if 'TAN' in hdr['CTYPE1'] or hdr['CTYPE2']:
                        hdr['CTYPE1'] = 'RA---TPV'
                        hdr['CTYPE2'] = 'DEC--TPV'
                    if 'PC1_1' in hdr:
                        hdr.remove('PC1_1')
                    if 'PC1_2' in hdr:
                        hdr.remove('PC1_2')
                    if 'PC2_1' in hdr:
                        hdr.remove('PC2_1')
                    if 'PC2_2' in hdr:
                        hdr.remove('PC2_2')
                    if 'CDELT1' in hdr:
                        hdr.remove('CDELT1')
                    if 'CDELT2' in hdr:
                        hdr.remove('CDELT2')

                    # get the WCS
                    w = wcs.WCS(hdr)

                    # define the centre of the image
                    xdim, ydim = w._naxis
                    x, y = xdim // 2, ydim // 2

                    # transform to world coordinates
                    ra, dec = w.all_pix2world(x, y, 0)

                    # get the corresponding PSF
                    add_psf = psf_files is not None
                    if add_psf:
                        psf_file, _ = img_file.replace('DET', 'PSF').split('__')
                        for pp in psf_files:
                            if psf_file in pp:
                                psf_file = pp
                                break

                    # save
                    tempdata['Exposure'][kk] = '{}|{}'.format(img_file, ext)
                    tempdata['RA'][kk] = ra
                    tempdata['DEC'][kk] = dec
                    tempdata['WCS'][kk] = w
                    if add_psf:
                        tempdata['PSF'][kk] = '{}|{}'.format(psf_file, 'chip{:02d}'.format(kk + 1))
                    tempdata['Mask'][kk] = '{}|{}'.format(img_file, ext.replace('.SCI', '.FLG'))

                data[ff] = tempdata

            else:
                raise LensmcError('Format non recognised.')

        return

    if cores == 0:
        cores = mp.cpu_count()

    # run
    pool = Pool(cores)
    pool.map(worker, range(n_files))
    pool.close()
    pool.join()

    # collate
    data = np.concatenate(data)
    data = data.view(np.recarray)  # make sure we get a recarray

    return data


def match_exposures_with_detections(exposures_catalogue, detections_catalogue, offset=4, cores=0):

    dtype = [('Detections', np.object)]
    det_dtype = [('LensMC_ID', np.chararray), ('x', np.float32), ('y', np.float32), ('Star', np.uint32)]
    n = exposures_catalogue.size
    data = np.recarray((n,), dtype=dtype)

    # define the radius of a circle that a galaxy should fall within
    # units in degrees
    # Euclid: every CCD is 4100 x 4100, this makes a radius of ~0.08 deg, and we make it 20% bigger
    deg_to_rad = np.pi / 180
    r = 0.1 * deg_to_rad

    # get sin and cos of angles
    sin_det_dec = np.sin(deg_to_rad * detections_catalogue['DEC'])
    cos_det_dec = np.cos(deg_to_rad * detections_catalogue['DEC'])
    sin_exp_dec = np.sin(deg_to_rad * exposures_catalogue['DEC'])
    cos_exp_dec = np.cos(deg_to_rad * exposures_catalogue['DEC'])
    det_ra = deg_to_rad * detections_catalogue['RA']
    exp_ra = deg_to_rad * exposures_catalogue['RA']

    # get the number of available cores
    if cores == 0:
        cores = mp.cpu_count()

    # split run in batches
    batch_length = n // cores
    batch_range = np.arange(batch_length)
    batches = [None] * cores
    if cores > 1:
        for bb in range(cores - 1):
            batches[bb] = batch_range + bb * batch_length
        batches[-1] = np.arange(batches[cores - 2][-1] + 1, n)
    else:
        batches[0] = batch_range

    # define worker to loop over exposures
    def worker(iter):

        for ii in batches[iter]:

            # define distance to all exposure centres
            d = sin_det_dec * sin_exp_dec[ii] + cos_det_dec * cos_exp_dec[ii] * np.cos(det_ra - exp_ra[ii])
            ix = np.where(d > 1)
            if np.sum(ix) > 0:
                d[ix] = 1
            ix = np.where(d < -1)
            if np.sum(ix) > 0:
                d[ix] = - 1
            d = np.abs(np.arccos(d))

            # find exposures within circle around the nominal position
            ix = d <= r
            n = np.sum(ix)
            if n > 0:

                # initialise output matched catalogue
                det_data = np.recarray((n,), dtype=det_dtype)

                # get indices of galaxies within circle
                gg, = np.where(ix)

                # transform to pixel coordinates
                w = exposures_catalogue['WCS'][ii]
                x, y = w.all_world2pix(detections_catalogue['RA'][gg], detections_catalogue['DEC'][gg], 0)

                # loop over galaxies in the circle and check whether they are actually in the image
                xdim, ydim = w._naxis
                in_image = np.zeros((n,), dtype=bool)
                for iii in range(n):

                    # check if the galaxy is in the image
                    if offset <= x[iii] < xdim - offset and offset <= y[iii] < ydim - offset:

                        in_image[iii] = 1

                        # save
                        det_data['LensMC_ID'][iii] = detections_catalogue['LensMC_ID'][gg[iii]]
                        det_data['x'][iii] = x[iii]
                        det_data['y'][iii] = y[iii]
                        det_data['Star'][iii] = detections_catalogue['Star'][gg[iii]]

                data['Detections'][ii] = det_data[in_image]

        return

    if cores == 0:
        cores = mp.cpu_count()

    # run
    pool = Pool(cores)
    pool.map(worker, range(cores))
    pool.close()
    pool.join()

    # collate
    exposures_catalogue_appended = np.recarray((exposures_catalogue.size,),
                                               dtype=exposures_catalogue.dtype.descr + dtype)
    for cc in exposures_catalogue.dtype.names:
        exposures_catalogue_appended[cc] = exposures_catalogue[cc]
    for ii in range(data.size):
        exposures_catalogue_appended[ii]['Detections'] = data[ii]['Detections']

    return exposures_catalogue_appended


def match_detections_with_exposures(detections_catalogue, exposures_catalogue, offset=4, cores=0, verbose=True):

    # initialise output catalogue
    dtype = [('Exposures', np.object), ('LensMC_Flag', np.uint32)]
    n = detections_catalogue.size
    matched_catalogue = np.recarray((n,), dtype=detections_catalogue.dtype.descr + dtype)
    for cc in detections_catalogue.dtype.names:
        matched_catalogue[cc] = detections_catalogue[cc]
    matched_catalogue['LensMC_Flag'] = 0

    # define the radius of a circle that a galaxy should fall within
    # units in degrees
    # Euclid: every CCD is 4100 x 4100, this makes a radius of ~0.08 deg, and we make it 20% bigger
    deg_to_rad = np.pi / 180
    r = 0.1 * deg_to_rad

    # get sin and cos of angles
    sin_det_dec = np.sin(deg_to_rad * detections_catalogue['DEC'])
    cos_det_dec = np.cos(deg_to_rad * detections_catalogue['DEC'])
    sin_exp_dec = np.sin(deg_to_rad * exposures_catalogue['DEC'])
    cos_exp_dec = np.cos(deg_to_rad * exposures_catalogue['DEC'])
    det_ra = deg_to_rad * detections_catalogue['RA']
    exp_ra = deg_to_rad * exposures_catalogue['RA']

    # get the number of available cores
    if cores == 0:
        cores = mp.cpu_count()

    # split run in batches
    batch_length = n // cores
    batch_range = np.arange(batch_length)
    batches = [None] * cores
    if cores > 1:
        for bb in range(cores - 1):
            batches[bb] = batch_range + bb * batch_length
        batches[-1] = np.arange(batches[cores - 2][-1] + 1, n)
    else:
        batches[0] = batch_range

    # define worker to loop over detection catalogues
    def worker(iter):

        for ii in batches[iter]:

            # define distance to all exposure centres
            d = sin_det_dec[ii] * sin_exp_dec + cos_det_dec[ii] * cos_exp_dec * np.cos(det_ra[ii] - exp_ra)
            ix = np.where(d > 1)
            if np.sum(ix) > 0:
                d[ix] = 1
            ix = np.where(d < -1)
            if np.sum(ix) > 0:
                d[ix] = - 1
            d = np.abs(np.arccos(d))

            # find exposures within circle around the nominal position
            ix = d <= r
            n = np.sum(ix)
            if n > 0:

                # initialise output matched catalogue
                matched_exposures = np.recarray((0,), dtype=exposures_catalogue.dtype)

                # loop over image files to find all the matching exposures for a given object
                for ee in range(exposures_catalogue.size):

                    # get WCS
                    w = exposures_catalogue[ee]['WCS']

                    # transform world to pixel coordinates
                    x, y = w.all_world2pix(detections_catalogue['RA'][ii], detections_catalogue['DEC'][ii], 0)

                    # check if the galaxy is in the image, and append if it's in there
                    xdim, ydim = w._naxis
                    if offset <= x < xdim - offset and offset <= y < ydim - offset:
                        matched_exposures = np.append(matched_exposures, exposures_catalogue[ee]).view(np.recarray)

                if matched_exposures.size > 0:
                    matched_catalogue['Exposures'][ii] = matched_exposures
                    matched_catalogue['LensMC_Flag'][ii] = 1

                    if verbose:
                        LensmcMessage('Found object ID {} in {}'.format(
                            detections_catalogue['ID'][ii], matched_exposures['Exposure']))

        return

    # run
    pool = Pool(cores)
    pool.map(worker, range(cores))
    pool.close()
    pool.join()

    return matched_catalogue


def make_segmentation_maps(exposures_catalogue, dir, cores=0, verbose=True):

    # check whether output directory exists
    if not os.path.isdir(dir):
        os.mkdir(dir)

    dtype = [('LensMC_Seg', np.chararray), ('LensMC_Blends', np.object)]
    n = exposures_catalogue.size
    segm = np.recarray((n,), dtype=dtype)

    # get the number of available cores
    if cores == 0:
        cores = mp.cpu_count()

    # split run in batches
    batch_length = n // cores
    batch_range = np.arange(batch_length)
    batches = [None] * cores
    if cores > 1:
        for bb in range(cores - 1):
            batches[bb] = batch_range + bb * batch_length
        batches[-1] = np.arange(batches[cores - 2][-1] + 1, n)
    else:
        batches[0] = batch_range

    # define worker to loop over exposures
    def worker(iter):

        for ii in batches[iter]:

            # get the exposure filename and extension
            fname, ext = read_fits_extension_field(exposures_catalogue[ii]['Exposure'])

            # get the mask filename and extension
            mask_fname, mask_ext = read_fits_extension_field(exposures_catalogue[ii]['Mask'])

            # read in HDU list
            with fits.open(fname) as hdulist:

                # get the data of a given detector
                image = hdulist[ext].data

                # get the detections
                id = exposures_catalogue[ii]['Detections']['LensMC_ID']
                x = exposures_catalogue[ii]['Detections']['x']
                y = exposures_catalogue[ii]['Detections']['y']

                # get the mask
                with fits.open(mask_fname) as mask_hdulist:
                    mask = mask_hdulist[mask_ext].data
                    mask[mask > 0] = 1
                    mask = ~mask.astype(bool)
                if 'mask' not in locals():
                    mask = None

                # make object segmentation map without taking the mask into account
                # we'll also get information about possible objects to mask out
                obj_segm_map, blends = make_obj_segm(image, id, x, y)

                # save to FITS
                fname, extension = os.path.splitext(os.path.basename(fname))
                if ext != 0:
                    fname = '{}.{}.lensmc-seg{}'.format(fname, ext, extension)
                else:
                    fname = '{}.lensmc-seg{}'.format(fname, extension)
                fname = fname.replace(' ', '_')

                # primary extension
                hdr = fits.Header()
                hdr['INFO'] = 'Segmentation map by LensMC.'
                hdr['AUTHOR'] = __author__
                hdr['EMAIL'] = __email__
                hdr['VERSION'] = __version__
                hdr['STATUS'] = __status__
                hdr['CPRGHT'] = __copyright__
                hdr['BLENDS'] = str(blends)
                hdu = fits.PrimaryHDU(data=obj_segm_map, header=hdr, do_not_scale_image_data=True)

                # save image
                fname = os.path.join(dir, fname)
                hdu = fits.HDUList(hdu)
                hdu.writeto(fname, overwrite=True)

                # save to numpy object
                segm[ii]['LensMC_Seg'] = fname
                segm[ii]['LensMC_Blends'] = blends

                if verbose:
                    LensmcMessage('Segmentation map saved to {}'.format(fname))

        return

    # run
    pool = Pool(cores)
    pool.map(worker, range(cores))
    pool.close()
    pool.join()

    # collate
    exposures_catalogue_appended = np.recarray((exposures_catalogue.size,),
                                               dtype=exposures_catalogue.dtype.descr + dtype)
    for cc in exposures_catalogue.dtype.names:
        exposures_catalogue_appended[cc] = exposures_catalogue[cc]
    exposures_catalogue_appended['LensMC_Seg'] = segm['LensMC_Seg']
    exposures_catalogue_appended['LensMC_Blends'] = segm['LensMC_Blends']

    return exposures_catalogue_appended


def make_input_stacks(input_catalogue, dir, n=1000, filename='input_stack.lmc'):

    # check whether output directory exists
    if not os.path.isdir(dir):
        os.mkdir(dir)

    # select objects validated by matching between detections and exposures
    ix = input_catalogue['LensMC_Flag'] == 1
    input_catalogue = input_catalogue[ix]

    # split catalogue in stacks
    stack_range = np.arange(n)
    n_stacks = input_catalogue.size // n + 1
    stacks = [None] * n_stacks
    for ii in range(n_stacks - 1):
        stacks[ii] = stack_range + ii * n
    stacks[-1] = np.arange(stacks[n_stacks - 2][-1] + 1, input_catalogue.size)

    # save
    for ii in range(n_stacks):
        fname = filename.replace('.lmc', '.stack_{}.lmc'.format(ii))
        fname = os.path.join(dir, fname)
        with open(fname, 'wb') as fo:
            pickle.dump(input_catalogue[stacks[ii]], fo)
            fo.close()

    return


def make_shear_catalogue(stacks, filename='shear_catalogue.fits'):

    # save
    n_stacks = len(stacks)
    catalogue = [None] * n_stacks
    for ii in range(n_stacks):
        with open(stacks[ii], 'rb') as fo:
            catalogue[ii] = pickle.load(fo)

    # collate
    catalogue = np.concatenate(catalogue)
    catalogue = catalogue.view(np.recarray)  # make sure we get a recarray

    # primary extension
    hdr = fits.Header()
    hdr['INFO'] = 'Shear catalogue by LensMC.'
    hdr['AUTHOR'] = __author__
    hdr['EMAIL'] = __email__
    hdr['VERSION'] = __version__
    hdr['STATUS'] = __status__
    hdr['CPRGHT'] = __copyright__
    hdu = fits.PrimaryHDU(header=hdr, do_not_scale_image_data=True)

    # binary fits table
    cols = from_record_to_fits_cols(catalogue)
    tbhdu = fits.BinTableHDU.from_columns(cols)

    # save
    hdu = fits.HDUList([hdu, tbhdu])
    hdu.writeto(filename, overwrite=True)

    return catalogue


def from_record_to_fits_cols(catalogue):

    cols = []
    dtypes = catalogue.dtype
    fields = catalogue.dtype.names
    for ff in range(len(fields)):
        if dtypes[ff] == 'bool':
            fmt = 'L'
        elif dtypes[ff] == 'uint32':
            fmt = 'J'
        elif dtypes[ff] == 'float32':
            fmt = 'E'
        elif dtypes[ff] == 'O':
            fmt = 'A1000'
        else:
            continue
        cols += [fits.Column(name=fields[ff], format=fmt, array=catalogue[fields[ff]])]

    return cols


def read_fits_extension_field(field):

    # get filename and extension, assuming they were saved in a single string with a '|' separator
    fields = field.split('|')

    # check length
    if len(fields) == 2:
        fname, ext = fields
        if not ext:
            ext = 0
    elif len(fields) == 1:
        fname, ext = fields[0], 0
    else:
        raise LensmcError('Could not read in fits and extension strings.')

    return fname, ext


def validate_input_catalogue(catalogue):

    # check data type
    assert type(catalogue) is np.recarray

    # check existence of fields
    fields = catalogue.dtype.names
    assert fields is not None

    # check esistence of specific fields
    assert 'ID' in fields
    assert 'RA' in fields
    assert 'DEC' in fields
    assert 'Star' in fields
    assert 'LensMC_ID' in fields
    assert 'LensMC_Flag' in fields

    # check existence of sub-array containing the exposures
    assert 'Exposures' in fields
    assert type(catalogue[0]['Exposures']) is np.recarray
    exp_fields = catalogue[0]['Exposures'].dtype.names
    assert exp_fields is not None
    assert 'Exposure' in exp_fields
    assert 'WCS' in exp_fields
    assert 'Mask' in exp_fields
    assert 'PSF' in exp_fields

    return
