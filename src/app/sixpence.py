import flet as ft
import screeninfo
import os

from app.config import Config

from controls.app_bar import AppBar
from controls.nav_rail import NavRail
from controls.router import Router

from views.home import Home
from views.budget import Budget
from views.expenses import Expenses
from views.reports import Reports
from views.settings import Settings

class Sixpence:
    SCREEN_SCALE_WIDTH  = .60 #.70
    SCREEN_SCALE_HEIGHT = .80 #.90

    def __init__(self, page):
        self.__page = page

        self.__init_window()
        self.__init_settings()

        self.__page.on_keyboard_event = self.__handle_on_keyboard

        # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Overall Color Theme
        self.__page.theme = ft.Theme(
            font_family="Latin Modern Mono",
            color_scheme_seed=ft.Colors.GREEN_400
        )

        self.__appbar = NavRail(self.__page)
        self.__router = Router(
            self.__page,
            appbar=self.__appbar,
            route_map={
                "/home": Home(self.__page),
                "/budget": Budget(self.__page),
                "/expenses": Expenses(self.__page),
                "/reports": Reports(self.__page),
                "/settings": Settings(self.__page)
            }
        )


    def __init_window(self):
        monitors = screeninfo.get_monitors()

        mon_width = monitors[0].width
        mon_height = monitors[0].height

        # Size
        self.__page.window.width = mon_width * self.SCREEN_SCALE_WIDTH
        self.__page.window.height = mon_height * self.SCREEN_SCALE_HEIGHT

        # Top/Left placement
        ## Center Left-to-Right
        self.__page.window.left = (mon_width / 2) - (self.__page.window.width / 2)
        ## At top of screen
        self.__page.window.top = mon_height * 0.0

        # Window Events
        # TODO: is not working. why????
        # https://flet.dev/docs/reference/types/window/
        # self.__page.window.prevent_close = True
        # self.__page.window.on_event = self.__handle_window_event


    def __init_settings(self):
        # NOTE: Built-in Storage Locations...I don't like them
        # FLET_APP_STORAGE_TEMP == .cache/org.....
        # FLET_APP_STORAGE_DATA == Documents/flet/sixpence

        # Where to look for sixpence.yml config/settings file
        config_home = os.getenv(
            "XDG_CONFIG_HOME",
            os.getenv("HOME") + "/.config"
        )
        config_dir = f"{config_home}/sixpence"
        os.makedirs(config_dir, exist_ok=True)

        # Temp Storage
        cache_home = os.getenv(
            "XDG_CACHE_HOME",
            os.getenv("HOME") + "/.cache"
        )
        cache_dir = f"{cache_home}/sixpence"
        os.makedirs(cache_dir, exist_ok=True)

        # Where to Store main files
        data_home = os.getenv(
            "XDG_DATA_HOME",
            os.getenv("HOME") + "/Documents"
        )
        docs_dir = f"{data_home}/sixpence"
        os.makedirs(docs_dir, exist_ok=True)

        # Init Config
        config = Config.initialize(
            f"{config_dir}/sixpence.yml",
            transient=["session"]
        )
        self.__page.session.set("config", config)

        # Set some app/session options
        # These options are transient and NOT saved to the config file
        config.set("session:cache_dir", cache_dir)
        config.set("session:config_dir", config_dir)
        config.set("session:docs_dir", docs_dir)


    def __handle_on_keyboard(self, event):
        # print(
        #     f"Key: {event.key}, Shift: {event.shift}, Control: {event.ctrl}, Alt: {event.alt}, Meta: {event.meta}"
        # )
        if event.ctrl:
            if event.key == "B":
                # self.__page.go("/budget")
                # TODO: does not work
                self.__appbar.selected_index = 1
            elif event.key == "E":
                # self.__page.go("/expenses")
                self.__appbar.selected_index == 2
            elif event.key == "R":
                # self.__page.go("/reports")
                self.__appbar.selected_index == 3


    def __handle_window_event(self, event):
        # if event.data == "close":
        print(event)






#
