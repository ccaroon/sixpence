import flet as ft

import views.constants as const
from views.base import Base as BaseView

class Settings(BaseView):
    def __init__(self, page):
        # Specific Icon and Text set in __snack_msg()
        self.__snackbar = ft.SnackBar(
            ft.Row([
                ft.Icon(),
                ft.Text(""),
            ])
        )

        self.__cfg = page.session.get("config")

        super().__init__(page)


    def __snack_msg(self, message, icon=ft.Icons.INFO_OUTLINE):
        # TODO: not great indexing into content/controls
        self.__snackbar.content.controls[0].name = icon
        self.__snackbar.content.controls[1].value = message
        self._page.open(self.__snackbar)


    def _layout(self):
        self.content = ft.Column(
            controls=[
                # Header
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SETTINGS, size=const.ICON_LARGE),
                        ft.Text(
                            "Settings",
                            weight=ft.FontWeight.BOLD,
                            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
                    ]
                ),
                # Tab View for Settings Groups
                ft.Tabs(
                    selected_index=0,
                    tabs=[
                        ft.Tab(
                            text="App",
                            icon=ft.Icons.SETTINGS_APPLICATIONS,
                            content=self.__app_controls()
                        ),
                        ft.Tab(
                            text="Backup",
                            icon=ft.Icons.BACKUP,
                            content=self.__backup_controls()
                        )
                    ]
                )
            ]
        )


    def __handle_on_save(self, evt):
            self.__cfg.save()
            self.__snack_msg("Settings Saved")


    def __backup_controls(self):
        keep_text = ft.Text(
            f"{self.__cfg.get('backup:keep')}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            expand=1
        )

        def on_slider_change(evt):
            new_value = round(evt.control.value)
            self.__cfg.set("backup:keep", new_value)
            keep_text.value = new_value
            keep_text.update()

        def on_choose_path(evt):
            self.__cfg.set("backup:path", evt.path)
            backup_path_text.value = evt.path
            backup_path_text.update()

        backup_path_text = ft.Text(
            f"{self.__cfg.get('backup:path')}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            expand=10
        )
        file_picker = ft.FilePicker(
            on_result=on_choose_path
        )
        self._page.overlay.append(file_picker)

        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Keep",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Number of backup files to keep",
                                    ),
                                ],
                                expand=1
                            ),
                            keep_text,
                            ft.Slider(
                                label="Keep {value} Backup Files",
                                min=1, max=30,
                                divisions=30,
                                value=self.__cfg.get("backup:keep"),
                                on_change_end=on_slider_change,
                                expand=10
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Path",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Save backup files to this directory",
                                    ),
                                ],
                                expand=1
                            ),
                            backup_path_text,
                            ft.ElevatedButton(
                                "Choose Path",
                                on_click=lambda _: file_picker.get_directory_path(),
                                expand=1
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Save",
                                icon=ft.Icons.SAVE,
                                on_click=self.__handle_on_save
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )

    def __app_controls(self):

        def on_mode_change(evt):
            new_mode = list(evt.control.selected)[0]
            self.__cfg.set("app:mode", new_mode)
            self._page.theme_mode = new_mode
            self._page.update()


        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Mode",
                                        weight=ft.FontWeight.BOLD,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE
                                    ),
                                    ft.Text(
                                        "Light, Dark or System Default",
                                    ),
                                ],
                                expand=1
                            ),
                            ft.SegmentedButton(
                                on_change=on_mode_change,
                                selected=[self.__cfg.get("app:mode")],
                                segments=[
                                    ft.Segment(
                                        value="light",
                                        label=ft.Text("Light"),
                                        icon=ft.Icon(ft.Icons.LIGHT_MODE)
                                    ),
                                    ft.Segment(
                                        value="dark",
                                        label=ft.Text("Dark"),
                                        icon=ft.Icon(ft.Icons.DARK_MODE)
                                    ),
                                    ft.Segment(
                                        value="system",
                                        label=ft.Text("System Default"),
                                        icon=ft.Icon(ft.Icons.SETTINGS_SUGGEST)
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Save",
                                icon=ft.Icons.SAVE,
                                on_click=self.__handle_on_save
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )


    def handle_keyboard_event(self, event):
        if event.ctrl:
            if event.key == "S":
                self.__handle_on_save(None)





#
