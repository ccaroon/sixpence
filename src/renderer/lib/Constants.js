const constants = {
  TYPE_INCOME: 0,
  TYPE_EXPENSE: 1,

  VIEW_STYLE_GROUP: 0,
  VIEW_STYLE_LIST: 1,

  IE_VIEW_BUDGETED: null,
  IE_VIEW_TO_DATE: 0,

  ICONS: [
    {text: 'Dollar', value: 'mdi-currency-usd', keywords: ['money', 'cost']},
    {text: 'Android Phone', value: 'mdi-cellphone-android', keywords: ['android']},
    {text: 'Account', value: 'mdi-account', keywords: ['personal']},
    {text: 'Amazon', value: 'mdi-amazon', keywords: []},
    {text: 'Audiobook', value: 'mdi-audiobook', keywords: []},
    {text: 'Bank', value: 'mdi-bank', keywords: []},
    {text: 'Book', value: 'mdi-book-open-variant', keywords: []},
    {text: 'Bug', value: 'mdi-bug', keywords: []},
    {text: 'Car', value: 'mdi-car', keywords: ['auto']},
    {text: 'Cart', value: 'mdi-cart', keywords: []},
    {text: 'Cash', value: 'mdi-cash-usd', keywords: []},
    {text: 'Clothes', value: 'mdi-tshirt-crew', keywords: ['shirt', 'blouse']},
    {text: 'Church', value: 'mdi-church', keywords: ['tithe']},
    {text: 'Food', value: 'mdi-food-fork-drink', keywords: ['drink', 'snack']},
    {text: 'Fuel', value: 'mdi-fuel', keywords: []},
    {text: 'Gas', value: 'mdi-gas-station', keywords: []},
    {text: 'Gift', value: 'mdi-gift', keywords: ['present', 'donation']},
    {text: 'Heart', value: 'mdi-heart-pulse', keywords: ['love']},
    {text: 'House', value: 'mdi-home-variant', keywords: ['home']},
    {text: 'Hulu', value: 'mdi-hulu', keywords: []},
    {text: 'iPhone', value: 'mdi-cellphone-iphone', keywords: ['apple']},
    {text: 'Flower', value: 'mdi-flower', keywords: ['landscaping', 'gardening']},
    {text: 'Light', value: 'mdi-lightbulb-on', keywords: []},
    {text: 'Medical', value: 'mdi-medical-bag', keywords: []},
    {text: 'Medicine', value: 'mdi-pill', keywords: []},
    {text: 'Misc', value: 'mdi-dots-horizontal', keywords: []},
    {text: 'Music', value: 'mdi-music', keywords: []},
    {text: 'Needle', value: 'mdi-needle', keywords: []},
    {text: 'Netflix', value: 'mdi-netflix', keywords: []},
    {text: 'Network', value: 'mdi-lan-connect', keywords: ['internet']},
    {text: 'Pets', value: 'mdi-paw', keywords: ['cat', 'dog']},
    {text: 'Playstation', value: 'mdi-playstation', keywords: ['ps1', 'ps2', 'ps3', 'ps4']},
    {text: 'Radiator', value: 'mdi-radiator', keywords: ['heat']},
    {text: 'RV', value: 'mdi-caravan', keywords: ['camper', 'caravan']},
    {text: 'Spotify', value: 'mdi-spotify', keywords: []},
    {text: 'Store', value: 'mdi-store', keywords: []},
    {text: 'Storm', value: 'mdi-weather-lightning-rainy', keywords: ['rain']},
    {text: 'Sports Car', value: 'mdi-car-sports', keywords: []},
    {text: 'Tax', value: 'mdi-currency-usd-off', keywords: []},
    {text: 'TV', value: 'mdi-television-classic', keywords: ['television']},
    {text: 'Towing', value: 'mdi-towing', keywords: []},
    {text: 'Transfer', value: 'mdi-transfer', keywords: []},
    {text: 'Video Games', value: 'mdi-gamepad-variant', keywords: []},
    {text: 'Water', value: 'mdi-water', keywords: []}
  ],

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
