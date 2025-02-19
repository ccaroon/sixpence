import flet as ft

import views.constants as const

class Settings(ft.Container):
    def __init__(self, page):
        super().__init__()

        self.__page = page
        self.__snackbar = ft.SnackBar(
            ft.Row([
                ft.Icon(),
                ft.Text(""),
            ])
        )

        self.__layout()


    def __snack_msg(self, message, icon=ft.Icons.INFO_OUTLINE):
        # TODO: not great indexing into content/controls
        self.__snackbar.content.controls[0].name = icon
        self.__snackbar.content.controls[1].value = message
        self.__page.open(self.__snackbar)


    def __layout(self):
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
                            text="Backup",
                            icon=ft.Icons.BACKUP,
                            content=self.__backup()
                        )
                    ]
                )
            ]
        )


    def __backup(self):
        cfg = self.__page.session.get("config")

        keep_text = ft.Text(
            f"{cfg.get('backup:keep')}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            expand=1
        )

        def on_save(evt):
            cfg.save()
            self.__snack_msg("Settings Saved")

        def on_slider_change(evt):
            new_value = round(evt.control.value)
            cfg.set("backup:keep", new_value)
            keep_text.value = new_value
            keep_text.update()

        def on_choose_path(evt):
            cfg.set("backup:path", evt.path)
            backup_path_text.value = evt.path
            backup_path_text.update()

        backup_path_text = ft.Text(
            f"{cfg.get('backup:path')}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            expand=10
        )
        file_picker = ft.FilePicker(
            on_result=on_choose_path
        )
        self.__page.overlay.append(file_picker)

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
                                value=cfg.get("backup:keep"),
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
                                on_click=on_save
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )
