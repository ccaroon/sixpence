# CHANGELOG

## v1.2.3 (June 15, 2018)
* Code: Make better use of Promises - Cleaned up the code a bit by having BudgetDB &
  ExpenseDB methods create and return promises instead of having to pass in callbacks.

## v1.2.2 (June 11, 2018)
* Swapped out most of the Date/Time manipulation to use MomentJS instead of the
  `Date()` class. Makes the code easier to understand.

## v1.2.1 (June 11, 2018)
* Bug: Expenses: Edit entry does not populate date

## v1.2.0 (June 8, 2018)
* Updated to use Electron 2.0.2
* Updated several other node modules
* Changed `import Mousetrap ...` to use lowercase name for module. The import
  was breaking on case-sensitive OSes like Linux.

## v1.1.0 (June 4, 2018)
* Expenses: Include "unbudgeted" categories in Category drop-down.
* Expenses: Shouldn't need to use +/- sign to indicate Income or Expense
* Expenses: View only over-budget items
* Expenses: Make it easier to change the date

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
