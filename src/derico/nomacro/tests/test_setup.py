# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from derico.nomacro.testing import DERICO_NOMACRO_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that derico.nomacro is properly installed."""

    layer = DERICO_NOMACRO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if derico.nomacro is installed."""
        self.assertTrue(self.installer.is_product_installed("derico.nomacro"))

    def test_browserlayer(self):
        """Test that IDericoNomacroLayer is registered."""
        from derico.nomacro.interfaces import IDericoNomacroLayer
        from plone.browserlayer import utils

        self.assertIn(IDericoNomacroLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DERICO_NOMACRO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("derico.nomacro")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if derico.nomacro is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("derico.nomacro"))

    def test_browserlayer_removed(self):
        """Test that IDericoNomacroLayer is removed."""
        from derico.nomacro.interfaces import IDericoNomacroLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDericoNomacroLayer, utils.registered_layers())
