const constants = {
  TYPE_INCOME: 0,
  TYPE_EXPENSE: 1,

  BUDGET_VIEW_BYMONTH: 0,
  BUDGET_VIEW_SUMMARY: 1,
  BUDGET_VIEW_ARCHIVED: 2,

  VIEW_STYLE_GROUP: 0,
  VIEW_STYLE_LIST: 1,

  ROLLOVER_CATEGORY: 'Sixpence:Rollover',

  IE_VIEW_BUDGETED: undefined,
  IE_VIEW_TO_DATE: 0,

  COLORS: {
    INCOME: 'green accent-1',
    INCOME_ALT: 'green accent-3',

    EXPENSE: 'red accent-1',
    EXPENSE_ALT: 'red lighten-1',

    OK_BUTTON: 'green accent-3',
    CANCEL_BUTTON: 'red lighten-1',

    TOOLBAR_BUTTON: 'orange lighten-2',
    TOOLBAR: 'grey darken-2',

    ITEM_HIGHLIGHT: 'orange lighten-2',

    GREY: 'grey lighten-2',
    GREY_ALT: 'grey lighten-4',

    PROGRESS_GOOD: 'green accent-1',
    PROGRESS_WARN: 'yellow accent-1',
    PROGRESS_BULLSEYE: 'green accent-3',
    PROGRESS_DANGER: 'red accent-2'
  },

  FORMATS: {
    entryDate: 'YYYY-MM-DD'
  },

  FREQUENCY: [
    { text: 'Monthly', value: 1 },
    { text: 'Bi-Monthly', value: 2 },
    { text: 'Quarterly', value: 3 },
    { text: 'Bi-Yearly', value: 6 },
    { text: 'Yearly', value: 12 }
  ],

  MONTHS: [
    { text: 'January', value: 1, icon: 'mdi-snowflake' },
    { text: 'February', value: 2, icon: 'mdi-snowman' },
    { text: 'March', value: 3, icon: 'mdi-weather-windy' },
    { text: 'April', value: 4, icon: 'mdi-weather-rainy' },
    { text: 'May', value: 5, icon: 'mdi-flower' },
    { text: 'June', value: 6, icon: 'mdi-tree' },
    { text: 'July', value: 7, icon: 'mdi-beach' },
    { text: 'August', value: 8, icon: 'mdi-school' },
    { text: 'September', value: 9, icon: 'mdi-leaf' },
    { text: 'October', value: 10, icon: 'mdi-ghost' },
    { text: 'November', value: 11, icon: 'mdi-meteor' },
    { text: 'December', value: 12, icon: 'mdi-pine-tree' }
  ]
}

export default constants
