################################################################################
#
# python-htbox
#
################################################################################

PYTHON_HTBOX_VERSION = 1.2
PYTHON_HTBOX_SITE = $(TOPDIR)/package/python-htbox/htbox
PYTHON_HTBOX_SITE_METHOD=local
PYTHON_HTBOX_SETUP_TYPE = setuptools

$(eval $(python-package))
