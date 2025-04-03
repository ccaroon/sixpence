import arrow
import locale

from app.config import Config

class Locale:
    @classmethod
    def init(cls, locale_id=None):
        """
        Initialze the locale to the given `locale_id` for all categories.

        Args:
            locale_id (str|tuple|None): Locale identifier.

        Examples:
            # None - Use current local for all categories
            >>> Locale.init()
            None

            # String
            >>> Locale.init("en_US.UTF-8")
            None

            # Tuple - normalized case
            >>> Locale.init(("en_US", "UTF-8"))
            None

            # Tuple - all lowercase
            >>> Locale.init(("en_us", "utf-8"))
            None

            # Tuple - lowercase / no dash
            >>> Locale.init(("en_us", "utf8"))
            None
        """
        if not locale_id:
            locale_id = locale.getlocale()
            # TODO: find a better way to handle this instead of defaulting
            #       to english/US/UTF-8
            if locale_id[0] is None or locale_id[1] is None:
                locale_id = ('en_US', 'UTF-8')

        locale.setlocale(locale.LC_ALL, locale_id)


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
            date_time (int|float|string):  Value to convert

        Returns:
            Arrow: An Arrow object for the `date_time` value in the configured time zone.
        """
        return arrow.get(date_time).replace(tzinfo=Config().get("app:timezone"))
