import flet as ft

from presenters.budget import Budget as BudgetPresenter

from views.base import Base as BaseView
from views.budget.editor import BudgetEditor
from views.budget.history.view import HistoryView
from views.budget.navbar import BudgetNavBar

class Budget(BaseView):

    def __init__(self, page):
        super().__init__(page, BudgetPresenter(self))

        self.editor = BudgetEditor(self._page, on_save=self._presenter.refresh)


    def _layout(self):
        self.list_view = ft.ListView()
        self.content = self.list_view

        self.history_view = HistoryView(self._page)
        self._page.overlay.append(self.history_view)

        self._presenter.refresh()


    def _layout_navbar(self):
        self._navbar = BudgetNavBar(
            self._page,
            callbacks={
                "on_refresh": self._presenter.refresh,
                "on_new": self._presenter.handle_new
            }
        )

    def handle_keyboard_event(self, event):
        if event.ctrl or event.meta:
            if event.key == "F":
                self._navbar.handle_keyboard_event(event)
            elif event.key == "N":
                self._presenter.handle_new(None)
