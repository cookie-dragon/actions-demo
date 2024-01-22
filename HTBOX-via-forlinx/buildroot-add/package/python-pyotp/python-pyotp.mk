################################################################################
#
# python-pyotp
#
################################################################################

PYTHON_PYOTP_VERSION = 2.6.0
PYTHON_PYOTP_SOURCE = pyotp-$(PYTHON_PYOTP_VERSION).tar.gz
PYTHON_PYOTP_SITE = https://files.pythonhosted.org/packages/61/cc/3f440f8ec7611e1252826d304f4807b25d1814c606037af31b8af50dcd80
PYTHON_PYOTP_SETUP_TYPE = setuptools
PYTHON_PYOTP_LICENSE = MIT
PYTHON_PYOTP_LICENSE_FILES = LICENSE

$(eval $(python-package))
