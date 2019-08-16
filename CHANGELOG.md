# CHANGELOG

## v1.10.0a - Repentant Rupees (August 30, 2019)
The Archive feature in v1.9.0 was NOT well thought out and resulted in many 
undesireable isses when a Budget Entry was archived.

This version is a complete re-do of the Archive feature.

### Features
* Ability to archive a budget entry.
* Budget menu includes choice to view archived entries.

### Changes
* `isArchived` flag field was changed to a date field named `archivedAt`

### Bug Fixes
...

### Misc
* BudgetDB - Cleaned up a bit; simplified?
* `v-select autocomplete>` deprecated. Changed to `v-autocomplete`.

## v1.9.0 - H2OMG (August 15, 2019)
### Features
* Budget
    + Added ability to archive an entry. 
      - Archiving will:
        1. Hide the entry in the UI
        2. Remove it from calculations
    + Adds `isArchived` field to the Budget database
* Database Migrations
    + Added ability to detect if user's databases need updating and then apply those updates.
      - I.e. A database migration system with user notifications.

## v1.8.0 - Atomic Fireball (June 22, 2019)
### Features
* Reports
    - Multi-year Income/Expense Comparison

### Improvements
* Fixed extra space between list items for lists -- tightens lists up a bit
* Reports - Monthly Category breakdown for  year
    - Removed category name and year from `v-chips` for better readability
    - Average per month amount for current year only averages up to current month (not across entire year)

### Code Cleanup
* Added color constants for more consistent colors

## v1.7.0 - El Psy Kongroo (May 28, 2019)
### Features
* Budget History
    - Editing a budget entry now keeps a history of changed amount values.
    - New Icon on each budget entry allows the user to view history.

### Misc
* Updated a few NodeJS packages; Of note:
    - Electron --> 4.1.5
* Fix a couple Vue-lint issues
* Misc file re-formatting

## v1.6.0 - Frivolous Fruitbat (Dec 14, 2018)
### Features
* Entry Date Handling
    - Re-instated the pop-up calendar
    - Using the '+' and '-' keys will inc/dec the date

### Bug Fixes
* Expenses: Fixed broken Income/Expense View Button (The Cent Button)
* Expenses: Tabbing in the Expense Entry sheet now works much better

### Misc
* `v-jumbotron` is deprecated; replaced with `v-responsive`
* `v-select combobox` is deprecated; replaced with `v-combobox`

## v1.5.1 (Nov 30, 2018)
* Backend updates:
    * Upgraded Electron to v3 (3.0.10)
    * Upgraded Vuetify to 1.3.11
    * Misc NodeJS modules updates

## v1.5.0 (Nov 09, 2018)
* New Feature: __Reports__
    * Button on Home Page to navigate to Reports
    * Reports added to View menu
    * One report added "Yearly by Category"

## v1.4.0 (July 06, 2018)
* Budget: Ability to show budgeted Income/Expenses for each month in a list.

## v1.3.0 (June 18, 2018)
* Expenses: Icon Match against Notes

## v1.2.3 (June 15, 2018)
* Code: Make better use of Promises - Cleaned up the code a bit by having BudgetDB &
  ExpenseDB methods create and return promises instead of having to pass in callbacks.
* Added more icons: bike, fish, camera, baby, tooth, toys, etc.

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
