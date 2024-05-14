![alt text](docs/_static/logo.png)

# Overview

Python scripts to analyze the morphology of isolated and interacting galaxies.
The package is designed to download S-PLUS (https://splus.cloud/),
Legacy (https://www.legacysurvey.org) and SDSS (https://www.sdss4.org/dr17/imaging)
images automatically. There are functions
to calculate a 2D sky background of the images and deblended segmentation maps of
interacting systems with merger isophotes. The non-parametric analysis is
performed by using `statmorph` package (https://github.com/vrodgom/statmorph).  
The user can study the environment of the object/system by downloading a list of
the galaxies within Field-of-View of S-PLUS/Legacy images from SIMBAD server
(http://simbad.u-strasbg.fr/simbad/). In addition, there is a function to
display DSS2 (http://alasky.u-strasbg.fr/hips-image-services/hips2fits) images
of any size.

Website: https://gitlab.com/joseaher/astromorphlib

## Documentation

The documentation is available at https://astromorphlib.readthedocs.io


## Installation

**Requirements**

Astromorphlib requires to run the following packages:

    * statmorph
    * splusdata
    * astro-datalab
    * astroplotlib
    * astropy
    * astroquery
    * photutils (1.5.0 <)**
    * numpy
    * scipy
    * matplotlib
    * wget

** to install this specific version of photutils you can try:

    % pip install photutils==1.5.0


This version can be easily installed via PyPI (https://pypi.org/project/astromorphlib/):

    % pip install astromorphlib

If you prefer to install astromorphlib manually, you can clone the developing
version at https://gitlab.com/joseaher/astromorphlib. In the directory this
README is in, simply type:

    % pip install .

or,

    % python setup.py install

## Uninstallation

To uninstall astromorphlib, just type:

    % pip uninstall astromorphlib

## Publications

- [Krabbe & Hernandez-Jimenez et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024MNRAS.528.1125K/abstract).
     In this paper Astromorphlib was applied to study ram-pressure stripped candidates.

## Authors

- Jose Hernandez-Jimenez (joseaher@gmail.com)
- Angela Krabbe                              

**Acknowledgements**

This software was funded partially by Brazilian agency FAPESP,
process number 2021/08920-8.

## Citing

If you use this code for a scientific publication, please
cite [Hernandez-Jimenez & Krabbe et al. (2022)](https://zenodo.org/records/6940848) and [Krabbe & Hernandez-Jimenez et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024MNRAS.528.1125K/abstract).
The BibTeX entries for this package are:

```
@MISC{hernandez_jimenez_2022,
  author       = {Hernandez-Jimenez, J. A. and
                  Krabbe, A. C.},
  title        = {{Astromorphlib: Python scripts to analyze the
                   morphology of isolated and interacting galaxies}},
  month        = jul,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {0.2},
  url          = {https://doi.org/10.5281/zenodo.6940848},
  doi          = {10.5281/zenodo.6940848}
}

@ARTICLE{2024MNRAS.528.1125K,
       author = {{Krabbe}, A.~C. and {Hernandez-Jimenez}, J.~A. and {Mendes de Oliveira}, C. and {Jaffe}, Y.~L. and {Oliveira}, C.~B. and {Cardoso}, N.~M. and {Smith Castelli}, A.~V. and {Dors}, O.~L. and {Cortesi}, A. and {Crossett}, J.~P.},
        title = "{Diagnostic diagrams for ram pressure stripped candidates}",
      journal = {\mnras},
     keywords = {galaxies: clusters: general, galaxies: clusters: intracluster medium, galaxies: evolution, galaxies: interactions, galaxies: irregular, galaxies: structure, Astrophysics - Astrophysics of Galaxies},
         year = 2024,
        month = feb,
       volume = {528},
       number = {2},
        pages = {1125-1141},
          doi = {10.1093/mnras/stad3881},
archivePrefix = {arXiv},
       eprint = {2312.09220},
 primaryClass = {astro-ph.GA},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2024MNRAS.528.1125K},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
