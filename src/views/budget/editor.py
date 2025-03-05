import flet as ft

from controls.icon_select import IconSelect

import views.constants as const

class Editor(ft.BottomSheet):
    def __init__(self):
        self.__container = self._layout()

        super().__init__(
            self.__container,
            shape=ft.ContinuousRectangleBorder(radius=25),
            size_constraints=ft.BoxConstraints(min_width=1)
        )


    def __on_amount_blur(self, evt):
        amount = float(evt.control.value) if evt.control.value else 0.0

        if amount < 0.0:
            self.__container.bgcolor = const.COLOR_EXPENSE_ALT
        elif amount > 0.0:
            self.__container.bgcolor = const.COLOR_INCOME_ALT
        else:
            self.__container.bgcolor = ft.Colors.WHITE

        self.__container.update()


    def __on_save(self, evt):
        print("Save")


    def _layout(self):
        # icon
        icon_fld = IconSelect("money")
        # category
        category_fld = ft.TextField(
            label="Category",
            prefix_icon=ft.Icons.CATEGORY,
            on_submit=icon_fld.update_options,
            on_blur=icon_fld.update_options
        )
        # amount
        amount_fld = ft.TextField(
            label="Amount",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            on_blur=self.__on_amount_blur
        )
        # frequency
        freq_fld = ft.Dropdown(
            label="Freq",
            leading_icon=ft.Icons.EVENT_REPEAT,
            options=[
                ft.DropdownOption(key=1, text="Monthly"),
                ft.DropdownOption(key=2, text="Bi-Monthly"),
                ft.DropdownOption(key=3, text="Quarterly"),
                ft.DropdownOption(key=6, text="Bi-Yearly"),
                ft.DropdownOption(key=12, text="Yearly"),
            ],
            enable_filter=True
        )
        # first_due
        first_due_fld = ft.Dropdown(
            label="First Due",
            leading_icon=ft.Icons.CALENDAR_MONTH,
            options=[ft.DropdownOption(key=idx, text=name) for idx,name in enumerate(const.MONTH_NAMES[1:])],
            enable_filter=True
        )
        # note
        note_fld = ft.TextField(
            label="Notes",
            prefix_icon=ft.Icons.STICKY_NOTE_2)

        main_container = ft.Container(
            ft.Row(
                [
                    # Icon
                    ft.Column([icon_fld],
                        expand=1,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Category
                    ft.Column([category_fld],
                        expand=3,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Amount
                    ft.Column([amount_fld],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Frequency
                    ft.Column([freq_fld],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # First Due
                    ft.Column([first_due_fld],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Notes
                    ft.Column([note_fld],
                        expand=5,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Save Button
                    ft.Column(
                        [
                            ft.IconButton(
                                ft.Icons.SAVE,
                                icon_size=const.ICON_MEDIUM,
                                on_click=self.__on_save
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        expand=1
                    ),
                ],
                height=75,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            bgcolor=ft.Colors.WHITE
        )

        return main_container


    # def new(self):
    #     pass

    # def edit(self, item):
    #     pass
