'use strict'

import { app, ipcMain, Menu, BrowserWindow } from 'electron'
import Backup from './backup'
import Config from './config'

const fs = require('fs')
const path = require('path')

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = path.join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function initApp () {
  // Create data directory
  if (!fs.existsSync(Config.dataPath)) {
    fs.mkdirSync(Config.dataPath, '0750')
  }
}

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 928,
    minWidth: 900,
    minHeight: 600,
    useContentSize: true
  })

  var mainMetaKey = process.platform === 'darwin' ? 'Cmd' : 'Ctrl'
  // -------------
  var aboutSubMenu = {
    label: 'About Sixpence',
    accelerator: mainMetaKey + '+?',
    click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
  }

  const template = [
    // 0
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
        },
        {
          label: 'Reports',
          accelerator: mainMetaKey + '+T',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-reports')
        }
      ]
    },
    // 1
    {
      role: 'window',
      submenu: [
        { role: 'minimize' }
      ]
    },
    // 2
    {
      role: 'help',
      submenu: [
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
        aboutSubMenu,
        // Other Apple Menu Worthy Item Go HERE
        { type: 'separator' },
        { role: 'quit' }
      ]
    })
  } else {
    // Add About to help menu
    template[2].submenu = template[2].submenu.concat([
      { type: 'separator' },
      aboutSubMenu
    ])

    // Add File Menu
    template.unshift({
      label: 'File',
      submenu: [
        { role: 'quit' }
      ]
    })
  }

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
  // -------------

  mainWindow.loadURL(winURL)

  mainWindow.on('close', (event) => {
    // Prevent closing the window...we still need it for a bit
    event.preventDefault()

    // Quit, to trigger the events in the 'before-quit' handler
    app.quit()
  })

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', () => {
  initApp()
  createWindow()
})

// app.on('window-all-closed', (event) => {
//   console.log('main:window-all-closed')
// })

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

app.on('before-quit', (event) => {
  if (mainWindow) {
    // Prevent the app from quitting...we need to handle clean up first
    event.preventDefault()

    // Send the cleanup event to the renderer
    // When it's done, it'll send back a cleanup event for the main process here
    mainWindow.webContents.send('sixpence-renderer-cleanup', 'before-quit')
  }
  // else - really quit
})

// This is necessary b/c in the `before-quit` handler we STOP the app from
// quiting so that we can send events...those events then respond by sending
// this event to do cleanup and actually exit.
ipcMain.on('sixpence-main-cleanup', (event, status, msg) => {
  Backup.backup()
    .then(() => {
      return true
    })
    .catch((err) => {
      console.log(`Backup Failed: ${err}`)
      return false
    })
    .finally(() => {
      app.exit(status)
    })
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
