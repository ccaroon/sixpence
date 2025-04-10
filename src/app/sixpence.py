import flet as ft
import screeninfo

import os
import pprint

from app.config import Config

from controls.notification_bar import NotificationBar
from controls.nav_rail import NavRail
from controls.router import Router

from utils.locale import Locale
from utils.archive import Archive

from app.about import About
from views.home import Home
from views.budget.main import BudgetView
from views.expenses.main import ExpenseView
from views.reports.main import ReportView
from views.settings import Settings

class Sixpence:
    SCREEN_SCALE_WIDTH  = .60 #.70
    SCREEN_SCALE_HEIGHT = .80 #.90

    def __init__(self, page):
        self.__app_name = "sixpence"
        self.__page = page

        self.__init_window()
        self.__init_settings()

        # No available until AFTER init_settings
        config = page.session.get("config")

        Locale.init(config.get("app:locale", ""))

        self.__page.title = self.__app_name.capitalize()
        self.__page.on_keyboard_event = self.__handle_on_keyboard

        # Overall Color Theme
        self.__page.theme = ft.Theme(
            font_family="Latin Modern Mono",
            color_scheme_seed=ft.Colors.GREEN_400,
        )

        self.__page.theme_mode = config.get("app:mode", "system")

        self.__about_view = About(self.__page)
        self.__page.overlay.append(self.__about_view)

        self.__notify_bar = NotificationBar(self.__page)

        self.__appbar = NavRail(self.__page)
        self.__router = Router(
            self.__page,
            appbar=self.__appbar,
            route_map={
                "/home": Home(self.__page),
                "/budget": BudgetView(self.__page),
                "/expenses": ExpenseView(self.__page),
                "/reports": ReportView(self.__page),
                "/settings": Settings(self.__page)
            }
        )
        self.__appbar.navigate_to(config.get("app:startup_view", "/home"))


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
        # https://flet.dev/docs/reference/types/window/
        self.__page.window.prevent_close = True
        self.__page.window.on_event = self.__handle_window_event



    # FLET_APP_STORAGE_DATA
    # * linux:
    #   - dev   -> ~/src/github/sixpence/storage/data
    #   - prod: -> ~/Documents/flet/sixpence
    # * macos:
    #   - dev:  -> ~/src/github/sixpence/storage/data
    #   - prod: -> ~/Documents/flet/org.caroon.sixpence
    def __determine_env(self):
        """
        Determine mode (dev or prod) based on FLET env var(s)
        """
        env = "dev"
        # NOTE: wish there was a better way, but can't find one
        data_dir = os.getenv("FLET_APP_STORAGE_DATA")
        if "/Documents/flet/" in data_dir:
            env = "prod"

        return env


    def __init_settings(self):
        env = self.__determine_env()

        # Where to look for sixpence.yml config/settings file
        config_home = os.getenv(
            "XDG_CONFIG_HOME",
            os.getenv("HOME") + "/.config"
        )
        config_dir = f"{config_home}/{self.__app_name}"
        os.makedirs(config_dir, exist_ok=True)

        # Temp Storage
        cache_home = os.getenv(
            "XDG_CACHE_HOME",
            os.getenv("HOME") + "/.cache"
        )
        cache_dir = f"{cache_home}/{self.__app_name}"
        os.makedirs(cache_dir, exist_ok=True)

        # Where to Store main files
        data_home = os.getenv(
            "XDG_DATA_HOME",
            os.getenv("HOME") + "/Documents"
        )
        docs_dir = f"{data_home}/{self.__app_name}"
        os.makedirs(docs_dir, exist_ok=True)

        # Init Config
        suffix = f"-{env}" if env != "prod" else ""
        config = Config.initialize(
            f"{config_dir}/settings{suffix}.yml",
            transient=["session"]
        )
        self.__page.session.set("config", config)

        # Set some app/session options
        # These options are transient and NOT saved to the config file
        config.set("session:env", env)
        config.set("session:cache_dir", cache_dir)
        config.set("session:config_dir", config_dir)
        config.set("session:docs_dir", docs_dir)


    def __backup_data(self):
        config = self.__page.session.get("config")

        keep = config.get("backup:keep", 14)
        backup_path = config.get("backup:path", ".")

        backup = Archive(f"{backup_path}/{self.__app_name}.tgz")
        backup.add(config.get("session:docs_dir"))
        backup.add(config.get("session:config_dir"))

        backup.write()

        backup.clean(older_than=keep)


    def __handle_on_keyboard(self, event):
        # import pprint
        # pprint.pprint(event)

        # TODO: simple way to denote cmd-KEY on MacOS &  ctrl-KEY others
        # MacOS -- cmd == event.meta
        # Linux -- ??? == event.meta


        # First, handle "global" keyboard events
        # TODO: better organize "global" events
        # -- About
        if (event.ctrl or event.meta) and event.shift and event.key == "?":
            self.__about_view.display()
        elif (event.ctrl or event.meta) and event.key == "B":
            self.__backup_data()
            self.__notify_bar.notify(ft.Icons.BACKUP, "Backup Complete")
        # --------------------------------------------------------------------
        # -- Quit
        # --------------------------------------------------------------------
        # NOTE: Quitting the app seems to be hard-coded into flet/flutter
        # Catching this keyboard event works, but there not time to execute
        # anything before the app is forcefully destroyed.
        # I.e. window.destroy() has already been initiated by the time
        # this code start to run.
        # elif (event.ctrl or event.meta) and event.key == "Q":
            # self.__backup_data()
            # self.__page.window.destroy() <-- not even necessary
        # --------------------------------------------------------------------
        # If not handled, passed to router to distribute to correct View
        else:
            self.__router.handle_keyboard_event(event)


    def __handle_window_event(self, evt):
        if evt.data == "close":
            self.__backup_data()
            evt.page.window.destroy()






#
