'use strict'

import { app, Menu, BrowserWindow } from 'electron'
const fs = require('fs')
const path = require('path')

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

function initApp () {
  // Open and read settings; create if necessary
  // TODO: ^^^^^^^^^

  // Create app documents directory
  var docPath = path.join(app.getPath('documents'), 'Sixpence')
  if (!fs.existsSync(docPath)) {
    fs.mkdirSync(docPath, '0750')
  }
}

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 928,
    useContentSize: true,
    width: 1280
  })

  var mainMetaKey = process.platform === 'darwin' ? 'Cmd' : 'Ctrl'
  // -------------
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New',
          click () { console.log('New... (not yet implemented)') }
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        {
          label: 'Main',
          accelerator: mainMetaKey + '+H',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-main')
        },
        {
          label: 'Budget',
          accelerator: mainMetaKey + '+B',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-budget')
        },
        {
          label: 'Expenses',
          accelerator: mainMetaKey + '+E',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-expenses')
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
          accelerator: mainMetaKey + '+?',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
        },
        {
          label: 'View on GitHub',
          click () { require('electron').shell.openExternal('https://github.com/ccaroon/sixpence') }
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

app.on('ready', () => {
  initApp()
  createWindow()
})

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
