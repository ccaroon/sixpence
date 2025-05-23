import flet as ft

from abc import abstractmethod

class Base(ft.Container):
    def __init__(self, page, presenter=None):
        super().__init__(expand=True)

        self._navbar = None
        self._page = page
        self._presenter = presenter

        self._layout_navbar()
        self._layout()


    @property
    def navbar(self):
        return self._navbar


    @abstractmethod
    def _layout(self):
        """ Override to define the layout of the View """
        raise NotImplementedError("_layout must be defined in your sub-class")


    def _layout_navbar(self):
        """ Override to define a NavBar for the View """
        self._navbar = None


    def handle_keyboard_event(self, event):
        """ Override to define keyboard shortcuts for the View """
