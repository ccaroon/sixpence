import Datastore from 'nedb'

const {app} = require('electron').remote

// -----------------------------------------------------------------------------
var _DB = new Datastore({
  filename: app.getPath('documents') + '/Sixpence/budget.sxp',
  autoload: true,
  timestampData: true
})
// -----------------------------------------------------------------------------
function computePeriod (freq, firstDue) {
  var due = []
  var willGet = (12 - firstDue) + 1
  var moreNeeded = 12 - willGet

  for (var m = firstDue; m <= 12 + moreNeeded; m += freq) {
  // for (var m = firstDue; m <= 12; m += freq) {
    var dueInMonth = m <= 12 ? m : m - 12
    due.push(dueInMonth)
  }

  return due
}
// -----------------------------------------------------------------------------
function due (month, freq, firstDue) {
  var isDue = false

  var dueMonths = computePeriod(freq, firstDue)
  isDue = dueMonths.includes(month)

  return isDue
}
// -----------------------------------------------------------------------------
export default {

  loadData: function (cb) {
    _DB.find({}).sort({type: 1, category: 1, amount: -1}).exec(cb)
  },

  // Load Budget entries for categories that are due in the given `month` based
  // on each entry's frequency and firstDue.
  // Arrange as look-up table by category
  loadCategoryDataByMonth: function (month, cb) {
    // db.find({ planet: { $in: ['Earth', 'Jupiter'] }}, function (err, docs) {
    //   // docs contains Earth and Jupiter
    // });

    _DB.find({}, {_id: 0, frequency: 1, firstDue: 1, category: 1, amount: 1})
      .sort({category: 1}).exec(function (err, docs) {
        if (err) {
          cb(err, null)
        } else {
          var entries = docs.filter(entry => due(month + 1, entry.frequency, entry.firstDue))
          var catMap = {}

          entries.forEach(function (entry) {
            if (!catMap.hasOwnProperty(entry.category)) {
              catMap[entry.category] = 0.0
            }

            catMap[entry.category] += entry.amount
          })

          cb(null, catMap)
        }
      })
  },

  loadCategories: function (cb) {
    var fields = {
      _id: 0,
      icon: 1,
      category: 1
    }

    _DB.find({}, fields).sort({category: 1}).exec(function (err, docs) {
      if (err) {
        cb(err, null)
      } else {
        var uniqueCats = {}
        docs.forEach(function (doc) {
          uniqueCats[doc.category] = doc.icon
        })
        cb(null, uniqueCats)
      }
    })
  },

  search: function (searchTerms, sort, cb) {
    if (!sort) {
      sort = {type: 1, category: 1, amount: -1}
    }

    _DB.find(searchTerms).sort(sort).exec(cb)
  },

  delete: function (id, cb) {
    _DB.remove({ _id: id }, {}, cb)
  },

  save: function (entry, cb) {
    _DB.update({_id: entry._id}, entry, { upsert: true }, cb)
  }
}
