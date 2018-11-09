import Datastore from 'nedb'

const { app } = require('electron').remote

// -----------------------------------------------------------------------------
const dbFileName = (process.env.NODE_ENV === 'development') ? 'budget-dev.sxp' : 'budget.sxp'
var _DB = new Datastore({
  filename: app.getPath('documents') + '/Sixpence/' + dbFileName,
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

  loadData: function () {
    var promise = new Promise(function (resolve, reject) {
      _DB.find({}).sort({ type: 1, category: 1, amount: -1 }).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          resolve(docs)
        }
      })
    })

    return promise
  },

  // Load Budget entries for categories that are due in the given `month` based
  // on each entry's frequency and firstDue.
  // Arrange as look-up table by category
  loadCategoryDataByMonth: function (month) {
    var promise = new Promise(function (resolve, reject) {
      _DB.find({}, { _id: 0, frequency: 1, firstDue: 1, category: 1, amount: 1 })
        .sort({ category: 1 })
        .exec(function (err, docs) {
          if (err) {
            reject(err)
          } else {
            var entries = docs.filter(entry => due(month + 1, entry.frequency, entry.firstDue))
            var catMap = {}

            entries.forEach(function (entry) {
              if (!catMap.hasOwnProperty(entry.category)) {
                catMap[entry.category] = 0.0
              }

              catMap[entry.category] += entry.amount
            })

            resolve(catMap)
          }
        })
    })

    return promise
  },

  loadCategories: function () {
    var fields = {
      _id: 0,
      icon: 1,
      category: 1
    }

    var promise = new Promise(function (resolve, reject) {
      _DB.find({}, fields).sort({ category: 1 }).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          var uniqueCats = {}
          docs.forEach(function (doc) {
            uniqueCats[doc.category] = doc.icon
          })
          resolve(uniqueCats)
        }
      })
    })

    return promise
  },

  search: function (searchTerms, sort = { type: 1, category: 1, amount: -1 }) {
    var promise = new Promise(function (resolve, reject) {
      _DB.find(searchTerms).sort(sort).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          resolve(docs)
        }
      })
    })

    return promise
  },

  categoryType: function (catName) {
    var promise = new Promise(function (resolve, reject) {
      _DB.find({ category: catName }).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          if (docs.length > 0) {
            resolve(docs[0].type)
          } else {
            resolve(null)
          }
        }
      })
    })

    return promise
  },

  delete: function (id) {
    var promise = new Promise(function (resolve, reject) {
      _DB.remove({ _id: id }, {}, function (err, count) {
        if (err) {
          reject(err)
        } else {
          resolve(count)
        }
      })
    })

    return promise
  },

  save: function (entry) {
    var promise = new Promise(function (resolve, reject) {
      _DB.update({ _id: entry._id }, entry, { upsert: true }, function (err, numReplaced, upsert) {
        if (err) {
          reject(err)
        } else {
          resolve(numReplaced, upsert)
        }
      })
    })

    return promise
  },

  isDue: due
}
