import { ipcMain } from 'electron'

import BudgetDB from './BudgetDB'

import config from './config'
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

    // Config Handlers
    ipcMain.handle('config:data', (event) => {
      return config.data
    })

    // Other Handlers
  }
}
