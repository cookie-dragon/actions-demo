################################################################################
#
# python-asyncua
#
################################################################################

PYTHON_ASYNCUA_VERSION = 0.9.12
PYTHON_ASYNCUA_SOURCE = asyncua-$(PYTHON_ASYNCUA_VERSION).tar.gz
PYTHON_ASYNCUA_SITE = https://files.pythonhosted.org/packages/bc/d2/8e06399cd4d7316b0ac3986972558fae7e873bd402039ae4a99a6323f8e9
PYTHON_ASYNCUA_SETUP_TYPE = setuptools
PYTHON_ASYNCUA_LICENSE = GNU Lesser General Public License v3 or later (LGPLv3+)

$(eval $(python-package))
