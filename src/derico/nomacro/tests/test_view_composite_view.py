# -*- coding: utf-8 -*-
from derico.nomacro.testing import DERICO_NOMACRO_FUNCTIONAL_TESTING
from derico.nomacro.testing import DERICO_NOMACRO_INTEGRATION_TESTING
from derico.nomacro.views.composite_view import ICompositeView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = DERICO_NOMACRO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_composite_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="composite-view"
        )
        self.assertTrue(ICompositeView.providedBy(view))

    def test_composite_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST), name="composite-view"
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = ICompositeView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = DERICO_NOMACRO_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
