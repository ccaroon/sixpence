import arrow
import locale

from app.config import Config

class Locale:
    @classmethod
    def init(cls, identifier):
        """
        Initialze the locale to the give locale identifier
        """
        locale.setlocale(locale.LC_ALL, identifier)


    @classmethod
    def currency(cls, value):
        """
        Format the given currency value for the locale.

        Args:
            value (float): A currency value to format

        Returns:
            string: The formatted value
        """
        return locale.currency(value, grouping=True)


    @classmethod
    def now(cls):
        """
        Get the current date/time for the configured time zone

        Returns:
            Arrow: The current date/time as an Arrow object
        """
        return arrow.now(Config().get("app:timezone"))


    @classmethod
    def as_arrow(cls, date_time):
        """
        Convert the given `date_time` for the configured time zone

        Args:
            date_time (any): (int | float | string) to convert

        Returns:
            Arrow: An Arrow object for the `date_time` value in the configured time zone.
        """
        return arrow.get(date_time).replace(tzinfo=Config().get("app:timezone"))
