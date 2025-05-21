class Reports:
    def __init__(self, view):
        self.__view = view


    def handle_report_click(self, evt):
        report = evt.control.data

        # Update title & add report specific actions
        self.__view._navbar.set_title(report.name)
        self.__view._navbar.actions.extend(report.actions)
        self.__view._navbar.update()

        # Display
        report.render()
        self.__view.content = report
        self.__view.update()


    def handle_report_home(self, evt):
        # Reset NavBar
        self.__view._navbar.set_title("All")
        self.__view._navbar.reset_actions()
        self.__view._navbar.update()

        # Reset content to report list
        self.__view.content = self.__view.reports
        self.__view.update()
