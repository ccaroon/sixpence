import flet as ft

from utils.icon_search import IconSearch

class IconSelect(ft.Dropdown):
    def __init__(self, init_keyword):
        self.__icon_search = IconSearch()
        init_icons = self.__icon_search.by_keyword(init_keyword)

        super().__init__(
            # label="Icon",
            leading_icon=ft.Icons.SEARCH,
            options=self.build_options(init_icons),
            enable_filter=True,
            on_change=self.on_icon_change
        )


    def update_options(self, evt):
        """
        Should be connected to/used by another control like a TextField
        where a string of some sort can be entered and used to search the
        icons.
        """
        icons = self.__icon_search.by_category(evt.control.value)
        self.options=self.build_options(icons)
        if icons:
            self.leading_icon = icons[0]
        self.update()


    def build_options(self, icon_list):
        options = []
        for icon in icon_list:
            options.append(
                ft.DropdownOption(text=" ", key=icon, leading_icon=icon)
            )
        return options


    def on_icon_change(self, evt):
        self.leading_icon = evt.data
        self.update()
