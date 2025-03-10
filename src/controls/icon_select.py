import flet as ft

from utils.icon_search import IconSearch

class IconSelect(ft.Dropdown):
    def __init__(self, init_keyword):
        self.__icon_search = IconSearch()
        init_icons = self.__icon_search.by_keyword(init_keyword)

        super().__init__(
            leading_icon=None,
            width=75,
            options=self.__build_options(init_icons),
            on_change=self.__on_change
        )


    def init_options(self, category):
        icons = self.__icon_search.by_category(category)
        self.options = self.__build_options(icons)


    def update_options(self, evt):
        """
        Should be connected to/used by another control like a TextField
        where a string of some sort can be entered and used to search the
        icons.
        """
        self.init_options(evt.control.value)
        self.border_color = ft.Colors.PRIMARY
        self.border_width = 3
        self.helper_text = "Choose"
        self.update()


    def __build_options(self, icon_list):
        options = []
        for icon in icon_list:
            options.append(
                ft.DropdownOption(text=" ", key=icon, leading_icon=icon)
            )
        return options


    def __on_change(self, evt):
        self.leading_icon = evt.data
        self.border_color = "black"
        self.border_width = 1
        self.helper_text = None
        self.update()
