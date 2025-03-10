import flet as ft

from controls.icon_select import IconSelect
from views.budget.history.prompt import HistoryPrompt

import utils.tools as tools
import views.constants as const

class BudgetEditor:
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

        self.__history_prompt = HistoryPrompt(page)


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

        # Icon
        self.__icon_ctrl.error_text = None
        if not self.__icon_ctrl.value:
            self.__icon_ctrl.error_text = "Required"
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

        # Frequency
        self.__freq_ctrl.error_text = None
        if not self.__freq_ctrl.value:
            self.__freq_ctrl.error_text = "Required"
            valid = False

        # First Due
        self.__first_due_ctrl.error_text = None
        if not self.__first_due_ctrl.value:
            self.__first_due_ctrl.error_text = "Required"
            valid = False

        # Notes
        # Not required | Free form text | No validation needed
        self.__note_ctrl.error_text = None

        self.__control.update()

        return valid


    def __populate_model(self):
        self.__item.icon = self.__icon_ctrl.value
        self.__item.amount = float(self.__amount_ctrl.value)
        self.__item.category = self.__category_ctrl.value
        self.__item.frequency = int(self.__freq_ctrl.value)
        self.__item.first_due = int(self.__first_due_ctrl.value)
        self.__item.notes = self.__note_ctrl.value


    def __populate_controls(self):
        self.__icon_ctrl.init_options(self.__item.category or "money")
        self.__icon_ctrl.value = self.__item.icon
        self.__icon_ctrl.leading_icon = self.__item.icon or ft.Icons.SEARCH

        self.__amount_ctrl.value = self.__item.amount
        self.__update_color(self.__item.amount)

        self.__category_ctrl.value = self.__item.category
        self.__freq_ctrl.value = self.__item.frequency
        self.__first_due_ctrl.value = self.__item.first_due
        self.__note_ctrl.value = self.__item.notes


    def __on_save(self, evt):
        if self.__validate():
            # Clone with "old" values
            old_item = self.__item.clone()

            # Update self.__item with "new" values
            self.__populate_model()

            # Update History if necessary.
            # Only care about history if `amount` changed.
            # Also saves __item and calls on-save handler
            # ...Is edit and amount changed...
            if old_item.id and (old_item.amount != self.__item.amount):
                self.__history_prompt.display(
                    old_item, self.__item,
                    on_save=self.__handle_on_save
                )
            else:
                # New item, not history to record; just save
                self.__item.save()
                if self.__handle_on_save:
                    self.__handle_on_save()

            # Close
            self.__control.open = False
            self.__control.update()


    def _layout(self):
        # icon
        self.__icon_ctrl = IconSelect("money")
        # category
        self.__category_ctrl = ft.TextField(
            label="Category",
            prefix_icon=ft.Icons.CATEGORY,
            on_submit=self.__icon_ctrl.update_options,
            on_blur=self.__icon_ctrl.update_options
        )
        # amount
        self.__amount_ctrl = ft.TextField(
            label="Amount",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            on_blur=self.__on_amount_blur
        )
        # frequency
        self.__freq_ctrl = ft.Dropdown(
            label="Frequency",
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
        self.__first_due_ctrl = ft.Dropdown(
            label="First Due",
            leading_icon=ft.Icons.CALENDAR_MONTH,
            options=[ft.DropdownOption(key=idx+1, text=name) for idx,name in enumerate(const.MONTH_NAMES[1:])],
            enable_filter=True
        )
        # note
        self.__note_ctrl = ft.TextField(
            label="Notes",
            prefix_icon=ft.Icons.STICKY_NOTE_2)

        main_container = ft.Container(
            ft.Row(
                [
                    # Icon
                    ft.Column([self.__icon_ctrl],
                        expand=1,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Category
                    ft.Column([self.__category_ctrl],
                        expand=3,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Amount
                    ft.Column([self.__amount_ctrl],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Frequency
                    ft.Column([self.__freq_ctrl],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # First Due
                    ft.Column([self.__first_due_ctrl],
                        expand=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Notes
                    ft.Column([self.__note_ctrl],
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
        # Set the BudgetItem being edited
        self.__item = item
        self.__populate_controls()
        self.__page.open(self.__control)
