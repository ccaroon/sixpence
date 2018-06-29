const constants = {
  TYPE_INCOME: 0,
  TYPE_EXPENSE: 1,

  BUDGET_VIEW_BYMONTH: 0,
  BUDGET_VIEW_SUMMARY: 1,

  VIEW_STYLE_GROUP: 0,
  VIEW_STYLE_LIST: 1,

  IE_VIEW_BUDGETED: null,
  IE_VIEW_TO_DATE: 0,

  FORMATS: {
    entryDate: 'YYYY-MM-DD'
  },

  FREQUENCY: [
    {text: 'Monthly', value: 1},
    {text: 'Bi-Monthly', value: 2},
    {text: 'Quarterly', value: 3},
    {text: 'Bi-Yearly', value: 6},
    {text: 'Yearly', value: 12}
  ],

  MONTHS: [
    {text: 'January', value: 1, icon: 'mdi-snowflake'},
    {text: 'February', value: 2, icon: 'mdi-snowman'},
    {text: 'March', value: 3, icon: 'mdi-weather-windy'},
    {text: 'April', value: 4, icon: 'mdi-weather-rainy'},
    {text: 'May', value: 5, icon: 'mdi-flower'},
    {text: 'June', value: 6, icon: 'mdi-tree'},
    {text: 'July', value: 7, icon: 'mdi-beach'},
    {text: 'August', value: 8, icon: 'mdi-school'},
    {text: 'September', value: 9, icon: 'mdi-leaf'},
    {text: 'October', value: 10, icon: 'mdi-ghost'},
    {text: 'November', value: 11, icon: 'mdi-meteor'},
    {text: 'December', value: 12, icon: 'mdi-pine-tree'}
  ]
}

export default constants
