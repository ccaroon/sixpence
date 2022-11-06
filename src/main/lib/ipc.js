import { ipcMain } from 'electron'

import windowHelper from './windowHelper'

export default {
  registerHandlers: function () {
    // Main Handlers
    ipcMain.handle('main:newWindow', (event, location, width, height) => {
      windowHelper.new(location, width, height)
    })

    // Other Handlers
  }
}
