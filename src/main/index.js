'use strict'

import { app, Menu, BrowserWindow } from 'electron'

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 928,
    useContentSize: true,
    width: 1280
  })

  // -------------
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Open...',
          click () { console.log(app.getPath('documents')) }
        }
      ]
    },
    {
      role: 'window',
      submenu: [
        {role: 'minimize'},
        {role: 'close'}
      ]
    },
    {
      role: 'help',
      submenu: [
        {
          label: 'About Sixpence',
          // click () { require('electron').shell.openExternal('https://electron.atom.io') }
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
        }
      ]
    }
  ]

  if (process.platform === 'darwin') {
    // Add Apple Menu
    template.unshift({
      label: 'Apple Menu',
      submenu: [
        // Other Apple Menu Worthy Item Go HERE
        { type: 'separator' },
        { role: 'quit' }
      ]
    })
  } else {
    //  Add Quit to File menu for all but MacOS
    template[0].submenu.push({ type: 'separator' })
    template[0].submenu.push({ role: 'quit' })
  }

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
  // -------------

  mainWindow.loadURL(winURL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  // if (process.platform !== 'darwin') {
  app.quit()
  // }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */
