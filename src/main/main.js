'use strict'

import { app, protocol, screen, ipcMain, BrowserWindow } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'
import fs from 'fs'
import path from 'path'

import backup from './lib/backup'
import ipc from './lib/ipc'
import menu from './lib/menu'
import settings from './lib/settings'
import windowHelper from './lib/windowHelper'

let mainWindow = null
const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

function initApp () {
  // Create data directory
  if (!fs.existsSync(settings.dataPath)) {
    fs.mkdirSync(settings.dataPath, '0750')
  }
}

async function createWindow () {
  const display = screen.getPrimaryDisplay()

  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: display.size.width * 0.70,
    height: display.size.height * 0.90,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),

      // Use vue.config.js#pluginOptions.nodeIntegration & leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    }
  })

  menu.setApplicationMenu()
  menu.addContext(mainWindow)

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await mainWindow.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    // if (!process.env.IS_TEST) mainWindow.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    mainWindow.loadURL('app://./index.html')
  }

  // Links that open new windows on target="_blank" use this
  mainWindow.webContents.setWindowOpenHandler((details) => {
    // Open a new window like **we** want
    windowHelper.new(details.url)
    // Prevent the default window from opening.
    return { action: 'deny' }
  })
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }

  ipc.registerHandlers()
  initApp()
  createWindow()
})

// TODO: Render Cleanup
// app.on('before-quit', (event) => {
//   if (mainWindow) {
//     // Prevent the app from quitting...we need to handle clean up first
//     event.preventDefault()

//     // Send the cleanup event to the renderer
//     // When it's done, it'll send back a cleanup event for the main process here
//     mainWindow.webContents.send('sixpence-renderer-cleanup', 'before-quit')
//   }
//   // else - really quit
// })

// TODO: Main Cleanup
// This is necessary b/c in the `before-quit` handler we STOP the app from
// quiting so that we can send events...those events then respond by sending
// this event to do cleanup and actually exit.
ipcMain.on('sixpence-main-cleanup', (event, status, msg) => {
  backup.backup()
    .then(() => {
      return true
    })
    .catch((err) => {
      console.log(`Backup Failed: ${err}`)
      return false
    })
    .finally(() => {
      app.exit(status)
      mainWindow = null
    })
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
