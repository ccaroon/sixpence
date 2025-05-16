import flet as ft

from presenters.expenses import Expenses as ExpensesPresenter

from views.base import Base as BaseView
from views.expenses.editor import ExpenseEditor
from views.expenses.navbar import ExpenseNavBar

class Expense(BaseView):
    def __init__(self, page):
        super().__init__(page, ExpensesPresenter(self))
        self.editor = ExpenseEditor(page, on_save=self._presenter.refresh)


    @property
    def current_date(self):
        return self._presenter.current_date


    def _layout(self):
        self.list_view = ft.ListView()
        self.content = self.list_view
        self.__layout_dlg()
        self._presenter.refresh()


    def _layout_navbar(self):
        self._navbar = ExpenseNavBar(
            self._page,
            parent=self,
            callbacks={
                "on_refresh": self._presenter.refresh,
                "on_new": self._presenter.handle_new,
                "on_change_month": self._presenter.handle_month_change
            }
        )


    def __layout_dlg(self):
        self.confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please Confirm"),
            content=ft.Text("PLACEHOLDER"),
            actions=[
                ft.TextButton("Yes", on_click=self._presenter.handle_delete),
                ft.TextButton("No", on_click=self._presenter.handle_delete),
            ]
        )

        self._page.overlay.append(self.confirm_dlg)


    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self._navbar.handle_keyboard_event(event)
            elif event.key == "N":
                self._presenter.handle_new(None)
        elif event.key in ("Arrow Up", "Arrow Down"):
            self.editor.handle_keyboard_event(event)
