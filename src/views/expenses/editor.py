import arrow
import flet as ft

from controls.icon_select import IconSelect

from utils.date_helper import DateHelper
import utils.tools as tools
import views.constants as const

# date | category | amount | tags | save

class ExpenseEditor:
    def __init__(self, page, **kwargs):
        self.__page = page
        self.__handle_on_save = kwargs.get("on_save")

        self.__item = None
        self.__container = self._layout()

        self.__control = ft.BottomSheet(
            self.__container,
            shape=ft.ContinuousRectangleBorder(radius=25),
            size_constraints=ft.BoxConstraints(min_width=1)
        )
        self.__page.overlay.append(self.__control)


    def __update_color(self, amount):
        # Change the color of the container based on whether it's
        # and income or expense
        if amount < 0.0:
            self.__container.bgcolor = const.COLOR_EXPENSE_ALT
        elif amount > 0.0:
            self.__container.bgcolor = const.COLOR_INCOME_ALT
        else:
            self.__container.bgcolor = ft.Colors.WHITE

        self.__container.update()


    def __on_amount_blur(self, evt):
        if tools.is_numeric(str(evt.control.value)):
            amount = float(evt.control.value) if evt.control.value else 0.0
            self.__update_color(amount)


    def __validate(self):
        valid = True

        # Date
        self.__date_ctrl.error_text = None
        if not self.__date_ctrl.value:
            self.__date_ctrl.error_text = "Required"
            valid = False

        # Category
        self.__category_ctrl.error_text = None
        if not self.__category_ctrl.value:
            self.__category_ctrl.error_text = "Required"
            valid = False

        # Amount
        self.__amount_ctrl.error_text = None
        amount = self.__amount_ctrl.value
        if not tools.is_numeric(str(amount)) or amount == 0.0:
            self.__amount_ctrl.error_text = "Invalid"
            valid = False

        # Tags
        # Not required | Free form text | No validation needed
        self.__tags_ctrl.error_text = None

        self.__control.update()

        return valid


    def __populate_model(self):
        # TODO: date
        self.__item.date = arrow.get(self.__date_picker.value)

        # category
        self.__item.category = self.__category_ctrl.value

        # amount
        self.__item.amount = float(self.__amount_ctrl.value)

        # tags
        new_tags = self.__tags_ctrl.value.split(",")
        self.__item.tags = new_tags


    def __populate_controls(self):
        # date
        self.__date_picker.value = self.__item.date
        self.__date_ctrl.text = self.__item.date.format("MM-DD-YYYY")

        # category
        self.__category_ctrl.value = self.__item.category

        # amount
        self.__amount_ctrl.value = self.__item.amount
        self.__update_color(self.__item.amount)

        # tags
        self.__tags_ctrl.value = ",".join(self.__item.tag_list())


    def __on_save(self, evt):
        if self.__validate():
            # Update self.__item with "new" values
            self.__populate_model()

            # Save
            self.__item.save()
            if self.__handle_on_save:
                self.__handle_on_save()

            # Close
            self.__page.close(self.__control)


    def __on_choose_date(self, evt):
        chosen_date = arrow.get(evt.control.value)
        self.__date_ctrl.text = chosen_date.format("MM-DD-YYYY")
        self.__date_ctrl.update()


    def _layout(self):
        # date
        self.__date_picker = ft.DatePicker(
            on_change=self.__on_choose_date
        )
        self.__date_ctrl = ft.OutlinedButton(
            # DateHelper.now().format("MM-DD-YYYY"),
            icon=ft.Icons.CALENDAR_MONTH,
            icon_color="black",
            style=ft.ButtonStyle(
                # alignment=ft.alignment.top_center,
                shape=ft.RoundedRectangleBorder(radius=5),
                side=ft.BorderSide(
                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                    width=1
                ),
                icon_size=const.ICON_MEDIUM,
                text_style=ft.TextStyle(
                    size=18
                )
            ),
            on_click=lambda e: self.__page.open(self.__date_picker)
        )
        # category
        self.__category_ctrl = ft.TextField(
            label="Category",
            prefix_icon=ft.Icons.CATEGORY
        )
        # amount
        self.__amount_ctrl = ft.TextField(
            label="Amount",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            on_blur=self.__on_amount_blur
        )
        # tags
        self.__tags_ctrl = ft.TextField(
            label="Tags",
            prefix_icon=ft.Icons.TAG,
            hint_text="Comma-separted list"
        )

        main_container = ft.Container(
            ft.Row(
                [
                    # Date
                    ft.Column([self.__date_ctrl],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER),
                    # Category
                    ft.Column([self.__category_ctrl],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Amount
                    ft.Column([self.__amount_ctrl],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Tags
                    ft.Column([self.__tags_ctrl],
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


    def edit(self, item):
        # Set the Expense item being edited
        self.__item = item
        self.__populate_controls()
        self.__page.open(self.__control)
