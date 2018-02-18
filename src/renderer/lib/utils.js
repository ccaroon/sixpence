export default {
  formatFrequency: function (freq) {
    var freqStr = null

    switch (freq) {
      case 1:
        freqStr = 'Monthly'
        break
      case 2:
        freqStr = 'Bi-Montly'
        break
      case 3:
        freqStr = 'Quarterly'
        break
      case 6:
        freqStr = 'Bi-Yearly'
        break
      case 12:
        freqStr = 'Yearly'
        break
      default:
        freqStr = 'Every ' + this.entry.frequency + ' Months'
        break
    }

    return (freqStr)
  },

  formatMoney: function (amount) {
    return (amount.toLocaleString('en-US', {style: 'currency', currency: 'USD'}))
  },

  monthNumberToName: function (monthNumber) {
    var d = new Date()
    d.setMonth(monthNumber)
    return (d.toLocaleDateString('en-US', {month: 'long'}))
  }

}