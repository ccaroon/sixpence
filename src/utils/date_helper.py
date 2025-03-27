import arrow

from app.config import Config

class DateHelper:

    __TIMEZONE = None

    # TODO: don't like this
    @classmethod
    def __init(cls):
        # cls.__CONFIG = Config()
        cfg = Config()
        cls.__TIMEZONE = cfg.get("app:timezone")


    @classmethod
    def now(cls):
        cls.__init()
        return arrow.now(cls.__TIMEZONE)


    @classmethod
    def as_arrow(cls, date_time):
        cls.__init()
        return arrow.get(date_time).replace(tzinfo=cls.__TIMEZONE)
