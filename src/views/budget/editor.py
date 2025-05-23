import flet as ft

from controls.icon_select import IconSelect
from views.budget.history.prompt import HistoryPrompt

from models.budget import Budget
from models.tag import Tag
import utils.tools as tools
import utils.constants as const

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

        self.__tag_aliases = self.__page.session.get("config").get("tag_aliases",{})


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


    def __on_category_blur(self, evt):
        self.__category_ctrl.value = Budget.normalize_category(evt.control.value)
        self.__icon_ctrl.update_options(evt)
        self.__category_ctrl.update()


    def __on_tags_blur(self, evt):
        tag_str = evt.control.value
        input_tags = tag_str.split(",")

        tag_names = []
        for tg in input_tags:
            tg = Tag.normalize(tg)
            if tg in self.__tag_aliases:
                tg = Tag.normalize(self.__tag_aliases.get(tg))

            tag_names.append(tg)

        unknown_tags = []
        for tg_name in tag_names:
            if not Tag.exists(tg_name):
                unknown_tags.append(tg_name)

        msg = None
        border_color = None
        if unknown_tags:
            msg = f"New Tags: {",".join(unknown_tags)}"
            border_color = ft.Colors.AMBER

        # Set value as normalized names
        self.__tags_ctrl.value = ",".join(tag_names)
        self.__tags_ctrl.helper_text = msg
        self.__tags_ctrl.border_color = border_color
        self.__tags_ctrl.update()


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
        self.__tags_ctrl.error_text = None

        self.__control.update()

        return valid


    def __populate_model(self):
        self.__item.icon = self.__icon_ctrl.value
        self.__item.amount = float(self.__amount_ctrl.value)
        self.__item.category = self.__category_ctrl.value
        self.__item.frequency = int(self.__freq_ctrl.value)
        self.__item.first_due = int(self.__first_due_ctrl.value)
        new_tags = self.__tags_ctrl.value.split(",")
        self.__item.tags = new_tags


    def __populate_controls(self):
        self.__icon_ctrl.init_options(self.__item.category or "money")
        self.__icon_ctrl.value = self.__item.icon
        self.__icon_ctrl.leading_icon = self.__item.icon or ft.Icons.SEARCH

        self.__amount_ctrl.value = self.__item.amount
        self.__update_color(self.__item.amount)

        self.__category_ctrl.value = self.__item.category
        self.__freq_ctrl.value = self.__item.frequency
        self.__first_due_ctrl.value = self.__item.first_due
        self.__tags_ctrl.value = ",".join(self.__item.tag_list())


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
            self.__page.close(self.__control)


    def _layout(self):
        # icon
        self.__icon_ctrl = IconSelect("money")
        # category
        self.__category_ctrl = ft.TextField(
            label="Category",
            prefix_icon=ft.Icons.CATEGORY,
            on_blur=self.__on_category_blur
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
        # tags
        self.__tags_ctrl = ft.TextField(
            label="Tags",
            prefix_icon=ft.Icons.TAG,
            hint_text="Comma-separted list",
            on_blur=self.__on_tags_blur
        )

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
        # Set the BudgetItem being edited
        self.__item = item
        self.__populate_controls()
        self.__page.open(self.__control)
