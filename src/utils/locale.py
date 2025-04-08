import arrow
import locale

from app.config import Config

class Locale:
    @classmethod
    def init(cls, lcid=''):
        """
        Initialze the locale to the given `lcid` for all categories.

        Args:
            lcid (str|None): Language Code ID. See https://www.crmportalconnector.com/developer-network/documentation/developing-for-tpc/language-code-table

        Examples:
            # None - Use current locale for all categories
            >>> Locale.init()
            None

            # String - Use specific locale
            >>> Locale.init("en_US")
            None
        """
        if not lcid:
            locale.setlocale(locale.LC_ALL, '')
        else:
            normal_lcid = locale.normalize(lcid)
            locale.setlocale(locale.LC_ALL, normal_lcid)

        # for key, value in locale.localeconv().items():
        #     print("%s: %s" % (key, value))


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
