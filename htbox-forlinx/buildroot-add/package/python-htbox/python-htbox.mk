################################################################################
#
# python-htbox
#
################################################################################

PYTHON_HTBOX_VERSION = 1.0
PYTHON_HTBOX_SITE = $(TOPDIR)/package/python-htbox/htbox-src
PYTHON_HTBOX_SITE_METHOD=local
PYTHON_HTBOX_SETUP_TYPE = setuptools

$(eval $(python-package))
