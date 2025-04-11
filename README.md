# Sixpence v2

**A Simple Budget Manager**

This is version 2 of Sixpence. It abandons [Electron][electron] for [Flutter][flutter] using [flet][Flet].

Sixpence is a cross-platform application and can be built to run on Linux, MS Windows or MacOS.

However, it's only been tested on Linux & MaxOS. It will likely have issues on MS Windows.

Sixpence exists because I couldn't find another application to manage my budget
the way **I** wanted to manage my budget. I built it for myself, my use case.
But if it works for you too, then great!

One day I'll get around to writing some docs to explain how it works and the general philosophy of it's usage. Until then, feel free to download it and try it out.

Sixpence allows you to create a budget and then track your progress. It is **not** Quicken or Moneydance or Mint.com. It can be used in conjunction with those kinds of applications.

## Features
* Create and Maintain a Budget
* Budgeted items can recur Monthly, Bi-Monthly, Quarterly, Bi-Yearly or Yearly
* Track Expenses and progress towards budgeted items
* Automatically tracks un-budgeted income & expenses
* Expense tracking focuses on the current month, but allows you to view/edit previous months.
* Monthly expense tracking takes into account non-monthly budgeted items. E.g. Your yearly subscription for Amazon Prime will show up as an expected (budgeted) expense for the month that it is due. Meaning you'll know that in June you have an extra $99 to shell out that month.
* Quickly and Easily search your Budget or Expenses
* View your expenses as a timeline list
* View your expenses grouped by category showing progress toward each budgeted item.
* Icons to help you quickly identify categories

## Screen Shots
...TODO...


## Development
### Notes / Links
* https://github.com/xzripper/flet_navigator
* https://github.com/codingjq/flet-routing-tutorial/tree/main
* https://flet.dev/docs/getting-started/navigation-and-routing
* https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors
* https://gallery.flet.dev/icons-browser/


### Setup
Create a Virtual Environment using `venv` or `pyenv` or whatever and activate it.

``` bash
# Install Requirements
bash> pip install -r requirements-dev.txt

# Unit Tests & Coverage
bash> invoke check.unit-tests

bash> invoke check.coverage

# Run in Dev Mode
bash> invoke dev.run

# Build Executable
bash> invoke app.build

# Run Built App
bash> invoke app.run

# Clean Build
bash> invoke app.build-clean

# Other Commands
bash> invoke -l
```

-----

[electron]: https://electronjs.org
[flet]: https://flet.dev
[flutter]: https://flutter.dev
