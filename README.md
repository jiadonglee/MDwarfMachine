# M_Dwarf_Machine (MDM)
STELLAR PARAMETRIZATION OF LAMOST M DWARF STARS

Created by jdli@nao.cas.cn, Fri. Mar. 13 2020.

## Getting Started

MDM do not need to install locally, but it requires to download models pre trained by SLAM (https://github.com/hypergravity/astroslam) . There are 2 models trained by BT-Settl synthetic spectra and ASPCAP labels respectively.  Users can get models on https://drive.google.com/open?id=1RRrVS9QsLBweDK-OBW2KfPkn5CevQRjC named `bt_settl.dump` and `aspcap.dump`.

### Author

Jiadong LI (jdli@nao.cas.cn)

### Prerequisites

Libraries you need to install the software.

* numpy

* scipy

* matplotlib

* astropy

* scikit-learn

* joblib

* pandas

* emcee

* slam (`pip install astroslam` or `pip install git+git://github.com/hypergravity/astrosla`)

  [https://github.com/hypergravity/astroslam]


## Running the tests

See on mdwarf/tutorial.ipynb


## License

This project is licensed under the MIT License.

## Acknowledgments
