import flet as ft

import pprint

import utils.tools
import utils.constants as const

from models.budget import Budget as BudgetItem
from utils.locale import Locale
from views.base import Base as BaseView
from views.budget.editor import BudgetEditor
from views.budget.history.view import HistoryView
from views.budget.navbar import BudgetNavBar

class BudgetView(BaseView):

    DEFAULT_FILTERS = {"deleted_at": "null"}

    def __init__(self, page):
        self.__filters = self.DEFAULT_FILTERS.copy()
        super().__init__(page)

        self.__editor = BudgetEditor(self._page, on_save=self._update)


    def _update(self, reset_filters=False, **kwargs):
        self.__list_view.controls.clear()

        if reset_filters:
            self.__filters = self.DEFAULT_FILTERS.copy()

        # kwargs is assumed to be search filters
        # Value of 'None' == delete from filters
        for fld, value in kwargs.items():
            if value is None:
                del self.__filters[fld]
            else:
                self.__filters[fld] = value

        # print(f"Filters: [{self.__filters}]")

        budget_items = BudgetItem.find(
            op="and",
            sort_by="type,category",
            **self.__filters
        )
        inc_total = 0.0
        exp_total = 0.0

        for idx, item in enumerate(budget_items):
            inc_color = utils.tools.cycle(const.INCOME_COLORS, idx)
            inc_color_alt = utils.tools.cycle(const.INCOME_COLORS, idx+1)
            exp_color = utils.tools.cycle(const.EXPENSE_COLORS, idx)
            exp_color_alt = utils.tools.cycle(const.EXPENSE_COLORS, idx+1)

            bgcolor = None
            tag_color = None
            if item.type == BudgetItem.TYPE_INCOME:
                bgcolor = inc_color
                tag_color = inc_color_alt
                inc_total += (item.amount / item.frequency)
            else:
                bgcolor = exp_color
                tag_color = exp_color_alt
                exp_total += (item.amount / item.frequency)

            display_amt = f"{Locale.currency(item.amount)}"
            if item.frequency > 1:
                display_amt += f" ({Locale.currency(item.amount / item.frequency)})"

            has_history = len(item.history) > 0

            tags = []
            for tag_name in item.tag_list():
                tags.append(
                    ft.Chip(
                        label=ft.Text(tag_name),
                        bgcolor=tag_color,
                        on_click=self.__filter_by_tag
                    )
                )

            actions = []
            if item.deleted_at:
                actions.extend([
                    ft.IconButton(ft.Icons.RESTORE_FROM_TRASH,
                        data=item,
                        icon_color=ft.Colors.GREY_800,
                        on_click=self.__on_undelete,
                    )
                ])
            else:
                actions.extend([
                    # NOTE: if icon_color is set, then disabled_color has
                    #       no effect
                    #       Instead, have to adjust icon_color according
                    #       to if the button is disabled
                    ft.IconButton(ft.Icons.HISTORY,
                        data=item,
                        icon_color=ft.Colors.GREY_800 if has_history else ft.Colors.GREY_500,
                        disabled=not has_history,
                        on_click=self.__on_history
                    ),
                    ft.IconButton(ft.Icons.EDIT,
                        data=item,
                        icon_color=ft.Colors.GREY_800,
                        on_click=self.__on_edit
                    ),
                    ft.IconButton(ft.Icons.DELETE,
                        data=item,
                        icon_color=ft.Colors.GREY_800,
                        on_click=self.__on_delete,
                    )
                ])

            tile = ft.ListTile(
                leading=ft.Icon(item.icon, color="black"),
                title=ft.Row(
                    [
                        ft.Text(item.category,
                            color="black",
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=4),
                        ft.Text(
                            display_amt,
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=4),
                        # TODO: Support Tags instead of Notes
                        ft.Row(tags, expand=4),
                        ft.VerticalDivider(),
                        # TODO: actions go here
                        *actions
                    ],
                ),
                subtitle=ft.Text(f"{item.frequency_desc()} / {const.MONTH_NAMES[item.first_due]}", color="black"),
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

        self.__history_view = HistoryView(self._page)
        self._page.overlay.append(self.__history_view)

        self._update()


    def _layout_navbar(self):
        self._navbar = BudgetNavBar(
            self._page,
            callbacks={
                "on_refresh": self._update,
                "on_new": self.__on_new
            }
        )


    def __filter_by_tag(self, evt):
        self._update(
            tags=evt.control.label.value
        )


    def __on_edit(self, evt):
        budget_item = evt.control.data
        self.__editor.edit(budget_item)


    def __on_new(self, evt):
        budget_item = BudgetItem()
        self.__editor.edit(budget_item)


    def __on_history(self, evt):
        budget_item = evt.control.data
        self.__history_view.display(budget_item)


    def __on_delete(self, evt):
        budget_item = evt.control.data
        budget_item.delete(safe=True)
        self._update()


    def __on_undelete(self, evt):
        budget_item = evt.control.data
        budget_item.undelete()
        self._update()


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self._navbar.handle_keyboard_event(event)
            elif event.key == "N":
                self.__on_new(None)
