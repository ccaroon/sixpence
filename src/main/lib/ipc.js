import { ipcMain } from 'electron'

import Napiform from './Napiform'
import windowHelper from './windowHelper'

function handleNapiformTransmogrify (event, msg1, msg2) {
  const napi = new Napiform(msg1, msg2)
  return napi.transmogrify()
}

export default {
  registerHandlers: function () {
    // Main Handlers
    ipcMain.handle('main:newWindow', (event, location, width, height) => {
      windowHelper.new(location, width, height)
    })

    // Other Handlers
    ipcMain.handle('napiform:transmogrify', handleNapiformTransmogrify)
  }
}
