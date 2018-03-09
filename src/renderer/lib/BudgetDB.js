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
