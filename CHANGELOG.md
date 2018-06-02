# CHANGELOG

## v1.0.4 (June 2, 2018)
* Fixed *yet another* date related issue: The start-of-month balance rollover code
  was using the start of the day on the previous month end date calculations and was
  therefore missing some transactions in computing the balance to rollover.

## v1.0.3 (May 31, 2018)
* Fixed *another* date related issue. The `monthNumberToName` function was returning
  the incorrect name b/c it was using the current day-of-the-month, but changing
  the month number. This was causing it to rollover to the next month when the current
  month had more days in it than the next month.

## v1.0.2 (May 31, 2018)
* Fixed a bug that was causing expense entries to be excluded when loading data
  b/c the end date for loading data (last day of the month) was using
  midnight (the start of the day) for the time and actual entries had a time
  AFTER midnight, i.e. outside of the range of 1st day of month at midnight to
  last day of month at midnight. Now the range is: 1st Day @ Midnight to Last Day
  @ 23:59:59.

## v1.0.1 (May 5, 2018)
* Fixed bug where the "About Sixpence" sub-menu has not showing up in the Help
  menu on non-MacOS OSes.
* Added CHANGELOG.md

## v1.0.0 (May 4, 2018)
* First major release.
