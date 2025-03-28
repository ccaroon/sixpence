import flet as ft

import arrow

import utils.constants as const

class HistoryPrompt(ft.AlertDialog):
    def __init__(self, page, **kwargs):
        super().__init__(modal=True)

        self.__page = page
        self.__layout()


    def __on_continue(self, evt):
        reason = self.__reason_ctrl.value

        if not reason:
            # Set Error Msg
            self.__reason_ctrl.error_text = "Required"
            self.__reason_ctrl.update()
        else:
            # Clear Error Msg
            self.__reason_ctrl.error_text = None
            self.__reason_ctrl.update()

            # Reset for next time
            self.__reason_ctrl.value = ""

            self.__new_item.history.append({
                "date": arrow.now(),
                "amount": self.__old_item.amount,
                "note": reason
            })

            self.__new_item.save()
            if self.__on_save:
                self.__on_save()

            self.__page.close(self)


    def __layout(self):
        # icon - Category - Change Note
        self.__icon_ctrl = ft.Icon(
            ft.Icons.INFO, size=const.ICON_MEDIUM, color="black")
        self.__category_ctrl = ft.Text(
            "",
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL
        )
        self.__reason_ctrl = ft.TextField(label="Reason For Change")

        self.title = ft.Row(
            [
                self.__icon_ctrl,
                self.__category_ctrl
            ]
        )
        self.content = self.__reason_ctrl
        self.actions = [
            ft.ElevatedButton(
                "Continue",
                color=ft.Colors.PRIMARY,
                on_click=self.__on_continue
            )
        ]

        self.__page.overlay.append(self)


    def display(self, old_item, new_item, **kwargs):
        self.__old_item = old_item
        self.__new_item = new_item
        self.__on_save = kwargs.get("on_save")

        self.__icon_ctrl.name = self.__new_item.icon
        self.__category_ctrl.value = self.__new_item.category

        self.__page.open(self)
