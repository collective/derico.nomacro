# -*- coding: utf-8 -*-

# from derico.nomacro import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ICompositeView(Interface):
    """Marker Interface for ICompositeView"""


@implementer(ICompositeView)
class CompositeView(BrowserView):

    def __call__(self):
        self.items = [
            "Hello World",
            "Hello Plone",
            "Hello Classic UI",
        ]
        return self.index()

    def render_item(self, item):
        template = ViewPageTemplateFile('item.pt')
        return template(self, title=item)

