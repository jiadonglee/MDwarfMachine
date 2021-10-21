# MDwarfMachine (MDM)
STELLAR PARAMETRIZATION OF LAMOST M DWARF STARS

Created by jdli@nao.cas.cn, Fri. Mar. 13 2020.

## Getting Started

MDM does not need to install locally, but it requires download models pre-trained by SLAM (https://github.com/hypergravity/astroslam). The trained model of MDM is on the basis of stellar parameters of APOGEE DR16. Users can download trained models on [ASPCAP_DR16.dump](http://vospace.china-vo.org/vospace/sharefile?Ravu36E%2F2jYZNzt02j3veAZPh4BY%2FLyrotXvCXHpya0%2F7YjJhP7oZ9jpqI1rP82tUzcIXRICrD0e%0ATDKhXgjkcQ%3D%3D). For more details, see ["Stellar Parameterization of LAMOST M Dwarf Stars"](https://iopscience.iop.org/article/10.3847/1538-4365/abe1c1) 

### Author

Jiadong Li (jdli@nao.cas.cn)   
Chao Liu (NAOC)   
Bo Zhang (NAOC)

### Prerequisites

Libraries you need to install the software.

* numpy

* scipy

* matplotlib

* astropy

* scikit-learn (1.0)

* joblib

* pandas

* emcee

* slam (`pip install astroslam` or `pip install git+git://github.com/hypergravity/astroslam`)

  [https://github.com/hypergravity/astroslam]


## Running the tests

See on mdwarf/tutorial.ipynb

## How to cite
```
@ARTICLE{2021ApJS..253...45L,
       author = {{Li}, Jiadong and {Liu}, Chao and {Zhang}, Bo and {Tian}, Hao and {Qiu}, Dan and {Tian}, Haijun},
        title = "{Stellar Parameterization of LAMOST M Dwarf Stars}",
      journal = {\apjs},
     keywords = {M dwarf stars, Astronomy data analysis, Low mass stars, Catalogs, 982, 1858, 2050, 205, Astrophysics - Solar and Stellar Astrophysics, Astrophysics - Earth and Planetary Astrophysics, Astrophysics - Astrophysics of Galaxies},
         year = 2021,
        month = apr,
       volume = {253},
       number = {2},
          eid = {45},
        pages = {45},
          doi = {10.3847/1538-4365/abe1c1},
archivePrefix = {arXiv},
       eprint = {2012.14080},
 primaryClass = {astro-ph.SR},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2021ApJS..253...45L},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
## License

This project is licensed under the MIT License.
