export default {
  ICONS: [
    { text: 'Account', value: 'mdi-account', keywords: ['personal'] },
    { text: 'Apple', value: 'mdi-apple', keywords: [] },
    { text: 'Audiobook', value: 'mdi-book-music', keywords: ['audible'] },
    { text: 'Baby', value: 'mdi-baby-buggy', keywords: ['diapers'] },
    { text: 'Bank', value: 'mdi-bank', keywords: [] },
    { text: 'Bike', value: 'mdi-bike', keywords: ['bicycle', 'cycling'] },
    { text: 'Book', value: 'mdi-book-open-variant', keywords: ['books'] },
    { text: 'Bug', value: 'mdi-bug', keywords: [] },
    { text: 'Camera', value: 'mdi-camera', keywords: ['photo'] },
    { text: 'Car', value: 'mdi-car', keywords: ['auto'] },
    { text: 'Cart', value: 'mdi-cart', keywords: [] },
    { text: 'Cash', value: 'mdi-cash', keywords: [] },
    { text: 'Clothes', value: 'mdi-tshirt-crew', keywords: ['shirt', 'blouse'] },
    { text: 'Coffee', value: 'mdi-coffee', keywords: ['java'] },
    { text: 'Church', value: 'mdi-church', keywords: ['tithe'] },
    { text: 'Dollar', value: 'mdi-currency-usd', keywords: ['money', 'cost'] },
    { text: 'Tooth', value: 'mdi-tooth-outline', keywords: ['dentist', 'teeth', 'dental'] },
    { text: 'Electronics', value: 'mdi-raspberrypi', keywords: [] },
    { text: 'Fishing', value: 'mdi-fish', keywords: [] },
    { text: 'Food', value: 'mdi-food-fork-drink', keywords: ['drink', 'snack'] },
    { text: 'Fuel', value: 'mdi-fuel', keywords: [] },
    { text: 'Gas', value: 'mdi-gas-station', keywords: [] },
    { text: 'Golf', value: 'mdi-golf', keywords: ['putt putt'] },
    { text: 'Gift', value: 'mdi-gift', keywords: ['present', 'donation'] },
    { text: 'Glasses', value: 'mdi-glasses', keywords: [] },
    { text: 'Heart', value: 'mdi-heart-pulse', keywords: ['love'] },
    { text: 'House', value: 'mdi-home-variant', keywords: ['home'] },
    { text: 'Hulu', value: 'mdi-hulu', keywords: [] },
    { text: 'HVAC', value: 'mdi-air-conditioner', keywords: ['a/c', 'air conditioner'] },
    { text: 'Package', value: 'mdi-package-variant', keywords: ['amazon'] },
    { text: 'Phone', value: 'mdi-cellphone', keywords: ['cellphone', 'iphone'] },
    { text: 'Flower', value: 'mdi-flower', keywords: ['landscaping', 'gardening'] },
    { text: 'Light', value: 'mdi-lightbulb-on', keywords: [] },
    { text: 'Medical', value: 'mdi-medical-bag', keywords: [] },
    { text: 'Medicine', value: 'mdi-pill', keywords: [] },
    { text: 'Misc', value: 'mdi-dots-horizontal', keywords: [] },
    { text: 'Music', value: 'mdi-music', keywords: [] },
    { text: 'Needle', value: 'mdi-needle', keywords: [] },
    { text: 'Netflix', value: 'mdi-netflix', keywords: [] },
    { text: 'Network', value: 'mdi-lan-connect', keywords: ['internet'] },
    { text: 'Pets', value: 'mdi-paw', keywords: ['cat', 'dog'] },
    { text: 'Playstation', value: 'mdi-sony-playstation', keywords: ['psn', 'ps1', 'ps2', 'ps3', 'ps4'] },
    { text: 'Radiator', value: 'mdi-radiator', keywords: ['heat'] },
    { text: 'RV', value: 'mdi-caravan', keywords: ['camper', 'caravan'] },
    { text: 'Spotify', value: 'mdi-spotify', keywords: [] },
    { text: 'Store', value: 'mdi-store', keywords: [] },
    { text: 'Storm', value: 'mdi-weather-lightning-rainy', keywords: ['rain'] },
    { text: 'Sports Car', value: 'mdi-car-sports', keywords: [] },
    { text: 'Tax', value: 'mdi-currency-usd-off', keywords: [] },
    { text: 'TV', value: 'mdi-television-classic', keywords: ['television'] },
    { text: 'Towing', value: 'mdi-tow-truck', keywords: ['tow truck'] },
    { text: 'Toys', value: 'mdi-duck', keywords: [] },
    { text: 'Transfer', value: 'mdi-transfer', keywords: [] },
    { text: 'Video Games', value: 'mdi-gamepad-variant', keywords: [] },
    { text: 'Water', value: 'mdi-water', keywords: [] }
  ],

  _SKIP_WORDS: [
    'a', 'the', 'but', 'and', 'or', 'then', 'for'
  ],

  superSearch: function (terms, sep = ' ', rev = false) {
    let parts = null
    if (typeof (terms) === 'string') {
      parts = terms.split(sep)
    } else {
      parts = terms
    }

    if (rev) {
      parts.reverse()
    }

    let foundIcon = null
    for (let i = 0; i < parts.length; i++) {
      foundIcon = this.search(parts[i])

      if (foundIcon) {
        break
      }
    }

    return foundIcon
  },

  search: function (keyword) {
    let foundIcon = null

    if (keyword.length <= 2 || this._SKIP_WORDS.includes(keyword)) {
      return null
    }

    const pattern = new RegExp(keyword, 'i')
    foundIcon = this.ICONS.find(function (iconData) {
      if (iconData.text.match(pattern)) {
        return true
      } else {
        let foundInKw = false
        for (let j = 0; j < iconData.keywords.length; j++) {
          const keyword = iconData.keywords[j]
          if (keyword.match(pattern)) {
            foundInKw = true
            break
          }
        }
        return foundInKw
      }
    })

    return foundIcon
  }
}
