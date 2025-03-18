import arrow

from app.config import Config

class DateHelper:

    # TODO: don't like this
    @classmethod
    def __init(cls):
        cls.__CONFIG = Config()

    @classmethod
    def now(cls):
        cls.__init()
        return arrow.now(cls.__CONFIG.get("app:timezone"))
