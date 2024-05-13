#!/Users/cmarsh/Documents/science/code/mesher/._venv-mesher/uhisduhrb2ci2oefpd5ssn2smmqydjei/bin/python3.11

import sys

from osgeo.gdal import UseExceptions, deprecation_warn

# import osgeo_utils.gdal_sieve as a convenience to use as a script
from osgeo_utils.gdal_sieve import *  # noqa
from osgeo_utils.gdal_sieve import main

UseExceptions()

deprecation_warn("gdal_sieve")
sys.exit(main(sys.argv))
