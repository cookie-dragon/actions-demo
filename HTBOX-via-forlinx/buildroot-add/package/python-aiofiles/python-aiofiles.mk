################################################################################
#
# python-aiofiles
#
################################################################################

PYTHON_AIOFILES_VERSION = 0.6.0
PYTHON_AIOFILES_SOURCE = aiofiles-$(PYTHON_AIOFILES_VERSION).tar.gz
PYTHON_AIOFILES_SITE = https://files.pythonhosted.org/packages/77/47/19e5951cc6ed771669906d2946b3deac32a35a9a155f730be49d8fa73dc9
PYTHON_AIOFILES_SETUP_TYPE = setuptools
PYTHON_AIOFILES_LICENSE = Apache-2.0
PYTHON_AIOFILES_LICENSE_FILES = LICENSE

$(eval $(python-package))
