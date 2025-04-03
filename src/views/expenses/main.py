import flet as ft

from models.budget import Budget
from models.expense import Expense

import utils.tools
from utils.locale import Locale
import utils.constants as const

from views.base import Base as BaseView
from views.expenses.editor import ExpenseEditor
from views.expenses.navbar import ExpenseNavBar

class ExpenseView(BaseView):

    def __init__(self, page):
        now = Locale.now()
        self.__curr_date = now.floor("month")

        Expense.update_rollover(now)

        self.__filters = self.__default_search_filters()
        super().__init__(page)

        self.__budget = Budget.for_month(self.__curr_date.month)
        self.__editor = ExpenseEditor(self._page, on_save=self._update)


    @property
    def current_date(self):
        return self.__curr_date


    def _update(self, reset_filters=False, **kwargs):
        self.__list_view.controls.clear()

        if reset_filters:
            self.__filters = self.__default_search_filters()

        # kwargs is assumed to be search filters
        # Value of 'None' == delete from filters
        for fld, value in kwargs.items():
            if value is None:
                del self.__filters[fld]
            else:
                self.__filters[fld] = value

        # pprint.pprint(f"Filters: [{self.__filters}]")
        expenses = Expense.find(
            op="and",
            sort_by="type,date",
            **self.__filters
        )
        inc_total = 0.0
        exp_total = 0.0

        for idx, item in enumerate(expenses):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            inc_color_alt = utils.tools.cycle(const.INCOME_COLORS, idx+1)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)
            exp_color_alt = utils.tools.cycle(const.EXPENSE_COLORS, idx+1)

            bgcolor = None
            tag_color = None
            if item.type == Expense.TYPE_INCOME:
                bgcolor = inc_color
                tag_color = inc_color_alt
                inc_total += item.amount
            else:
                bgcolor = exp_color
                tag_color = exp_color_alt
                exp_total += item.amount

            display_amt = f"{Locale.currency(item.amount)}"

            tags = []
            for tag_name in item.tag_list():
                tags.append(
                    ft.Chip(
                        label=ft.Text(tag_name),
                        bgcolor=tag_color,
                        on_click=self.__filter_by_tag,
                        padding=ft.padding.all(0)
                    )
                )

            tile = ft.ListTile(
                leading=ft.Icon(item.icon, color="black"),
                title=ft.Row(
                    [
                        ft.Text(item.category,
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Text(
                            display_amt,
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=3),
                        ft.Row(tags, expand=4),
                        ft.VerticalDivider(),
                        # NOTE: if icon_color is set, then disabled_color has
                        #       no effect
                        #       Instead, have to adjust icon_color accoriding
                        #       to if the button is disabled
                        ft.IconButton(ft.Icons.EDIT,
                            data=item,
                            icon_color=ft.Colors.GREY_500 if item.deleted_at else ft.Colors.GREY_800,
                            on_click=self.__on_edit,
                            disabled=item.deleted_at is not None,
                        ),
                        ft.IconButton(ft.Icons.DELETE_FOREVER,
                            data=item,
                            icon_color=ft.Colors.GREY_500 if item.deleted_at else ft.Colors.GREY_800,
                            on_click=self.__on_delete_confirm,
                            disabled=item.deleted_at is not None
                        )
                    ],
                ),
                subtitle=ft.Text(
                    item.date.format("MMM DD, YYYY"),
                    color="black"),
                bgcolor=bgcolor
            )

            self.__list_view.controls.append(tile)

        self._navbar.income_total = inc_total
        self._navbar.expense_total = exp_total
        net_balance = inc_total + exp_total
        self._navbar.net_balance = net_balance

        self._page.update()


    def _layout(self):
        self.__list_view = ft.ListView()
        self.content = self.__list_view
        self.__layout_dlg()
        self._update()


    def _layout_navbar(self):
        self._navbar = ExpenseNavBar(
            self._page,
            parent=self,
            callbacks={
                "on_refresh": self._update,
                "on_new": self.__on_new,
                "on_change_month": self.__on_change_month
            }
        )


    def __layout_dlg(self):
        self.__confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please Confirm"),
            content=ft.Text("PLACEHOLDER"),
            actions=[
                ft.TextButton("Yes", on_click=self.__on_delete),
                ft.TextButton("No", on_click=self.__on_delete),
            ]
        )

        self._page.overlay.append(self.__confirm_dlg)


    def __default_search_filters(self):
        end_date = self.__curr_date.ceil("month")
        return {
            "date": f"btw:{self.__curr_date.int_timestamp}:{end_date.int_timestamp}"
        }


    def __filter_by_tag(self, evt):
        self._update(
            tags=evt.control.label.value
        )


    def __on_edit(self, evt):
        expense = evt.control.data
        self.__editor.edit(expense, self.__budget)


    def __on_new(self, evt):
        expense = Expense(
            date=Locale.now()
        )
        self.__editor.edit(expense, self.__budget)


    def __on_delete(self, evt):
        self._page.close(self.__confirm_dlg)

        if evt.control.text == "Yes":
            expense = self.__confirm_dlg.data
            expense.delete()
            self._update()


    def __on_delete_confirm(self, evt):
        item = evt.control.data

        self.__confirm_dlg.content = ft.Column(
            [
                ft.Text("Are you sure you want to delete this Expense?"),
                ft.Text(
                    f"{item.date.format("MMM DD, YYYY")} | {item.category} | {Locale.currency(item.amount)}?",
                    weight=ft.FontWeight.BOLD
                )
            ],
            tight=True
        )

        self.__confirm_dlg.data = item
        self._page.open(self.__confirm_dlg)


    def __set_month(self, date):
        self.__curr_date = date.floor("month")
        end_date = date.ceil("month")

        self._navbar.set_date_display(self.__curr_date.format("MMM YYYY"))

        self.__budget = Budget.for_month(self.__curr_date.month)
        self._update(
            date=f"btw:{self.__curr_date.int_timestamp}:{end_date.int_timestamp}"
        )


    def __on_change_month(self, evt):
        if isinstance(evt.control, ft.DatePicker):
            chosen_date = Locale.as_arrow(evt.control.value)
            self.__set_month(chosen_date)
        else:
            offset = evt.control.data.get("offset", 0)
            # current month
            if offset == 0:
                self.__set_month(Locale.now())
            # month + offset
            else:
                new_month = self.__curr_date.shift(months=offset)
                self.__set_month(new_month)


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self._navbar.handle_keyboard_event(event)
            elif event.key == "N":
                self.__on_new(None)
        elif event.key in ("Arrow Up", "Arrow Down"):
            self.__editor.handle_keyboard_event(event)
