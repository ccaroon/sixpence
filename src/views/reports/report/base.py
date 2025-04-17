import flet as ft

from abc import ABC, abstractmethod

class ReportBase(ABC, ft.Container):
    def __init__(self, page):
        super().__init__()

        self._page = page
        self._actions = []
        self._init_actions()


    @property
    @abstractmethod
    def icon(self):
        """ Icon Representing the Report """

    @property
    @abstractmethod
    def name(self):
        """ Name of the Report """


    @property
    @abstractmethod
    def description(self):
        """ Description of the Report """

    @abstractmethod
    def render(self):
        """ Render the Report """


    @abstractmethod
    def _on_export(self, evt):
        """ Export Data to Markdown File """


    @property
    def actions(self):
        return self._actions


    def _init_actions(self):
        file_picker = ft.FilePicker(
            on_result=self._on_export
        )
        self._page.overlay.append(file_picker)

        self._actions = [
            ft.VerticalDivider(),
            ft.IconButton(
                icon=ft.Icons.SAVE_ALT,
                icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                on_click=lambda _: file_picker.get_directory_path(),
                tooltip="Export"
            ),
            ft.VerticalDivider()
        ]
