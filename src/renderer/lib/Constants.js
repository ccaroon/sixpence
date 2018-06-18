const constants = {
  TYPE_INCOME: 0,
  TYPE_EXPENSE: 1,

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
    {text: 'January', value: 1},
    {text: 'February', value: 2},
    {text: 'March', value: 3},
    {text: 'April', value: 4},
    {text: 'May', value: 5},
    {text: 'June', value: 6},
    {text: 'July', value: 7},
    {text: 'August', value: 8},
    {text: 'September', value: 9},
    {text: 'October', value: 10},
    {text: 'November', value: 11},
    {text: 'December', value: 12}
  ]
}

export default constants
