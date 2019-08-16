#!/usr/bin/env node

const Datastore = require('nedb')
const Moment = require('moment')

const HOME = process.env.HOME
const DOCUMENTS = HOME + "/Documents"
// -----------------------------------------------------------------------------
// const dbFileName = (process.env.NODE_ENV === 'development') ? 'budget-dev.sxp' : 'budget.sxp'
const dbFileName = 'budget-dev.sxp'
var DB = new Datastore({
    filename: DOCUMENTS + '/Sixpence/' + dbFileName,
    autoload: true,
    timestampData: true
})
// -----------------------------------------------------------------------------
DB.find({ archivedAt: { $ne: null } }).exec((err, docs) => {
    if (err) console.error(err)
    else {
        // console.log(docs)
        console.log("Archived Entry Count: " + docs.length)
    }
})
// -----------------------------------------------------------------------------
// (isArchived == null) OR (archivedDate in CURR_MONTH)
var now = Moment()
var then = Moment("2019-07-17")
console.log(then.valueOf())
// console.log(now.toDate())
var startDate = now.startOf('month').toDate()
var endDate = now.endOf('month').toDate()
console.log(startDate + " | " + endDate)
var query = { $or: [{ archivedAt: null }, { $where: function () { return this.archivedAt >= startDate && this.archivedAt <= endDate } }] }
// var query = { archivedAt: null }
// { $where: function () { return this.date >= startDate && this.date <= endDate } }
DB.find(query)
    .sort({ type: 1, category: 1, amount: -1 })
    .exec(function (err, docs) {
        if (err) {
            console.error(err)
        } else {
            // console.log(docs)
            console.log("Active Entries: " + docs.length)
        }
    })
