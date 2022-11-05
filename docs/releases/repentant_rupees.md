# Notes

## What Nots
* July 17, 2019 == 1563336000000

## isArchived
* If Budget entry is archived:
    + Budget
      - [x] DONT show in budget item list
      - [x] DONT use in budget calculation(s)
    + Expenses
      - [x] DO show in PAST month expense lists
      - [x] DO show in CURRENT month expense list (current being month it was archived)
      - [x] DONT show in FUTURE month expense lists
    + Reports
      - [x] DO show if entry was archived THIS year or AFTER (i.e. Active After first of year)
* [x] DB migration `isArchived` => `archivedAt`

### thoughts
* BudgetDB:
    - [x] getAllBudgetEntries
    - [x] getActiveBudgetEntries
    - [x] getAllBudgetCategories
    - [x] getActiveBudgetCategories
    - [x] ACTIVE means: (isArchived == null) OR (archivedDate in [CURR_MONTH | SOME_DATE_RANGE])
    - [x] Use `archivedAt` instead of `isArchived` flag?
      - `archivedAt`: last day of the current month it was archived.
