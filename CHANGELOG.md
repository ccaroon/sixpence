# CHANGELOG

## UNRELEASED: v2.0.0 - Pristine Penny (????? ??, 2025)
Complete rewrite using Flet/Flutter


--------------------------------------------------------------------------------


## v1.13.2 - Glimmering Gil - Patch #2 (May 21, 2022)
### Misc
* Updated the App Icon to be less transparent

## v1.13.1 - Glimmering Gil - Patch #1 (December 5, 2021)
### Bugs Fixes
* In Reports -> Yearly Budget -> Category by Month screen the Total Spent and
  Average Per Month Spent were always displaying NaN

## v1.13.0 - Glimmering Gil (October 16, 2021)
### Features
* Added "Recalculate Monthly Rollover" choice to Expenses Menu
* Added "View Zero Dollar Categories" choice to Expenses Menu
  - ...also made menu building & choice handling more generic
* Added next & previous month buttons to the Expenses toolbar
* Added button to Expenses toolbar to return to current month
* Added Calendar View type to Expenses. See income & spending amounts per day.
* Added Icon beside Expense menu to identify which (if any) filter mode is enabled.
  - All catetories vs. Overbudget catetories vs. Zero Dollar categories
* Added `get` method to Icons class to get an icon by exact name

### Changes
* Removed `dense` attribute from Budget, Expenses & Reports AppBars
* Expenses search enhancements...
  - no longer assumes search values are strings; can be numbers too
  - support for multiple operators: `==`, `~=`, `>`, `>=`, `<`, `<=`
  - NO LONGER supports `?` search separator
  - can search for multiple `&` separated terms
    - only supports AND at the moment: `key1<OP>value1&key2<OP>value2`
  - Search code mostly re-written
* Fixed several MDI icons that were either removed from the set or renamed.
* Moved Expenses toolbar button for Actual vs. Budgeted numbers to *before* the numbers.
* Icon Updates:
    - Budget: Income, Expense & Balance in a couple places
    - Expenses:
      - Income, Expense & Balance
      - Actual (Bank) numbers vs Budgeted numbers toggle button

### Bug Fixes
* Fixed a bug where you had to click the "Save" button twice to save a Budget entry

### Misc
* Upgrade Electron from 11.x to 12.2.x
* Lots of NPM package updates
  - `@mdi/fonts`
  - `vuetify`
  - etc...
* Removed `yarn` support. Just use `npm` instead. `yarn` got weird.

## v1.12.1 - Grookey.1 (February 06, 2021)
### Changes
* Upgraded Electron from 4.x to 11.x
* Upgraded yarn to v2 (berry)

## v1.12.0 - Grookey (February 05, 2020)
### Changes
* Expense entries are now taggable instead of having a free-form text field for `notes`.
    - There's a DB migration which will indicate if any entries exist with a `notes` field.
    - There is **not** an automatic migration from `notes` to `tags`.
    - The user can manually edit an entry to add tags. Doing so will remove the `notes` field.
    - Expense search now searches `category` and `tags` for matches.
    - Clicking on a `[TAG]` in the Entry listing will filter on that tag.
* Added the version codename to the About dialog.

### Misc
* Updated VuetifyJS
* Updated VueJS

## v1.11.0 - Codename Goes Here (November 07, 2019)
### Features
#### General
* Data File Backup
    - Data files are backed-up to a ZIP file when you exit the app.
    - Backup to a `backups` directory by default. User configureable.
    - Set the number of backup files to keep. Defaults to five. User configurable.
* User Options (Config)
    - New UI (Ctrl+,) and Menu Option
    - Lives in data directory and is included in data backup.

#### Expense
* If budgeted category, show budgeted value as placeholder text for expense entry amount.
* On new entry show form as red or green based on category to indicate that it will default to an Income or Expense entry.

#### Budget
* When updating a budget entry, you can now add a note regarding the change.

### Changes
#### General
* Update Vuetify to v2.x (v2.1.5)
* Misc UI improvement made possible by Vuetify v2.

## v1.10.0 - Repentant Rupees (September 27, 2019)
The Archive feature in v1.9.0 was NOT well thought out and resulted in many
undesireable issues when a Budget Entry was archived.

This version is a complete re-do of the Archive feature.

### Features
* Ability to archive a budget entry.
* Budget menu includes choice to view archived entries.

### Changes
* `isArchived` flag field was changed to a date field named `archivedAt`

### Bug Fixes
* Known issues that v1.9.0 created when a budget entry was archived.

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
