import { ipcMain } from 'electron'

import BudgetDB from './BudgetDB'

import config from './config'
import DBMigrations from './DBMigrations'
import windowHelper from './windowHelper'

export default {
  registerHandlers: function () {
    // Main Handlers
    ipcMain.handle('main:newWindow', (event, location, width, height) => {
      windowHelper.new(location, width, height)
    })

    // BudgetDb
    ipcMain.handle('budget-db:count', (event, searchTerms) => {
      return BudgetDB.count(searchTerms)
    })

    // DBMigrations
    ipcMain.handle('db-migrations:check', (event) => {
      return DBMigrations.checkBudgetDb()
    })

    ipcMain.handle('db-migrations:execute', (event, name) => {
      return DBMigrations.execute(name)
    })

    // Config Handlers
    ipcMain.handle('config:data', (event) => {
      return config.data
    })

    // Other Handlers
  }
}
