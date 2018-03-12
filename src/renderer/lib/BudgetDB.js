import Datastore from 'nedb'

const {app} = require('electron').remote

export default {

  db: new Datastore({
    filename: app.getPath('documents') + '/Sixpence/budget.sxp',
    autoload: true,
    timestampData: true
  }),

  loadData: function (cb) {
    this.db.find({}).sort({type: 1, category: 1, amount: -1}).exec(cb)
  },

  loadCategories: function (cb) {
    this.db.find({}, {_id: 0, category: 1}).sort({category: 1}).exec(function (err, docs) {
      if (err) {
        cb(err, null)
      } else {
        var allCats = docs.map(function (doc) {
          return (doc.category)
        })
        var uniqueCats = Array.from(new Set(allCats))

        cb(null, uniqueCats)
      }
    })
  },

  search: function (searchTerms, sort, cb) {
    if (!sort) {
      sort = {type: 1, category: 1, amount: -1}
    }

    this.db.find(searchTerms).sort(sort).exec(cb)
  },

  delete: function (id, cb) {
    this.db.remove({ _id: id }, {}, cb)
  },

  save: function (entry, cb) {
    this.db.update({_id: entry._id}, entry, { upsert: true }, cb)
  }

}
