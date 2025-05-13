import dateutil

class Settings:
    def __init__(self, view, config):
        self.__view = view
        self.__cfg = config


    def handle_save_click(self, evt):
        self.__cfg.save()
        self.__view.notification_bar.info("Settings Saved")


    def handle_keep_change(self, evt):
        new_value = round(evt.control.value)
        self.__cfg.set("backup:keep", new_value)

        self.__view.keep_text.value = new_value
        self.__view.keep_text.update()


    def handle_choose_path(self, evt):
        self.__cfg.set("backup:path", evt.path)

        self.__view.backup_path_text.value = evt.path
        self.__view.backup_path_text.update()


    def handle_mode_change(self, evt):
        new_mode = list(evt.control.selected)[0]
        self.__cfg.set("app:mode", new_mode)
        evt.page.theme_mode = new_mode
        evt.page.update()


    def handle_timezone_blur(self, evt):
        new_tz = evt.control.value

        if dateutil.tz.gettz(new_tz):
            self.__cfg.set("app:timezone", new_tz)
            evt.control.error_text = None
        else:
            evt.control.error_text = "Invalid Time Zone"

        evt.control.update()


    def handle_locale_blur(self, evt):
        old_locale = self.__cfg.get("app:locale")
        new_locale = evt.control.value

        if new_locale != old_locale:
            self.__cfg.set("app:locale", new_locale)
            evt.control.helper_text = "Takes affect on restart"
            evt.control.update()


    def handle_startup_view_change(self, evt):
        new_view = evt.control.value
        self.__cfg.set("app:startup_view", new_view)
