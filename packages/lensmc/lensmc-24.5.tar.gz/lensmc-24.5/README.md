# LensMC
#### Weak lensing shear measurement with forward modelling and MCMC sampling

## Author

**Giuseppe Congedo**

Institute for Astronomy <br>
Royal Observatory of Edinburgh <br>
University of Edinburgh <br>
Blackford Hill <br>
Edinburgh <br>
EH9 3HJ <br>
UK

**<giuseppe.congedo@ed.ac.uk>**

To acknowledge this work, please cite: [Euclid Collaboration: Giuseppe Congedo et al. (2024)](https://arxiv.org/abs/2405.00669).

[Copyright & licence](LICENSE).

## Description

LensMC is a Python package for weak lensing shear measurement that includes a framework for
images simulation, measurement, calibration, and shear bias analysis.

It inherits the same lensfit principles about galaxy model fitting and marginalisation.
It implements a fast and accurate MCMC sampling for model fitting.

## Dependencies

LensMC requires Python 3.6, but is expected to be backward compatible with earlier versions (apart from the recently introduced f-strings).

Python dependencies (see [requirements.txt](requirements.txt)):
- astropy==4.0.1
- cython==0.29.17
- dask[array]==2.16.0 (not required for measurement)
- dask[delayed]==2.16.0 (not required for measurement)
- matplotlib==3.2.1 (not required for measurement)
- numpy==1.18.4
- pyfftw==0.12.0
- PyQt5==5.15.0 (not required for measurement, but only as a dependency for matplotlib)
- scipy==1.4.1
- tqdm==4.46.0 (not required for measurement)

## Install via setuptools

If all dependencies are satisfied, LensMC can be easily compiled and installed with setuptools,
e.g. with user privileges:
```
$ python3 setup.py install --user
```
This is useful when one wants to integrate LensMC within a pre-existing setup.

## Build and install in a confined environment

If dependencies are not satisfied, or one needs to have a confined installation, it is advisable to build a
full environment from scratch. The environment will build Python and all modules required to run the code.

__Dependencies.__ Please make sure you have the [(Debian) packages](deb-pkg-requirements.txt) installed in your system,
and run:
```
$ sudo apt update
$ sudo apt install $(cat deb-pkg-requirements.txt)
```

__Fix xlocale.h (to be deprecated).__ It may be necessary to fix this in some systems:
```
$ ls /usr/include/xlocale.h
$ ls: cannot access '/usr/include/xlocale.h': No such file or directory
```
If so, make a symbolic link:
```
$ sudo ln -s /usr/include/locale.h /usr/include/xlocale.h
```

__Build.__ We can build the environment by running:
```
$ make
```
the code will then create a confined Python environment, including Python itself and all module dependencies.

__Install.__ The final step is to install LensMC:
```
$ make install
```
Please verify that both the build and install steps went through without problems.
To activate the environment:
```
$ source lensmc-env/bin/activate
```
and then LensMC can be imported straightaway:
```
(lensmc-env) $ python
>>> import lensmc
```
To exit the environment:
```
(lensmc-env) $ deactivate
```

__Additional make recipes.__ Useful recipes for development:
1. `clean`: clean up the installation (i.e. undo `make install`);
2. `purge`: clean up `lensmc-env`, auxiliary files, and build directories;
3. `install-inplace`: build LensMC inplace instead of installing in `lensmc-env`.

__Optional make parameters.__ Useful parameters for development:
1. `make PREFIX=...`: install in another user defined directory instead of `./lensmc-env`;
2. `make CC=icc LDSHARED="icc -shared"`: use Intel compiler instead of `gcc`
(we will need to source the Intel installation beforehand, e.g. `source /workspace/intel/bin/compilervars.sh intel64`);
3. `make CFLAGS="-O3 -fPIC"`: pass optimisation flags to the compiler;
4. `make FFTW-VER=...`: specify which `fftw` version should be installed.
