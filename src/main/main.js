'use strict'

import { app, protocol, screen, BrowserWindow, Menu, MenuItem } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'
import path from 'path'

import ipc from './lib/ipc'
import windowHelper from './lib/windowHelper'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow () {
  const display = screen.getPrimaryDisplay()

  // Create the browser window.
  const win = new BrowserWindow({
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

  // Add Context Menu
  const menu = new Menu()
  menu.append(new MenuItem({
    label: 'Copy',
    role: 'copy'
  }))
  menu.append(new MenuItem({
    label: 'Paste',
    role: 'paste'
  }))
  menu.append(new MenuItem({
    type: 'separator'
  }))
  menu.append(new MenuItem({
    label: 'Dev Tools',
    role: 'toggleDevTools'
  }))

  win.webContents.on('context-menu',
    (event, click) => {
      event.preventDefault()
      menu.popup(win.webContents)
    },
    false
  )

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    // if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }

  // Links that open new windows on target="_blank" use this
  win.webContents.setWindowOpenHandler((details) => {
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
  createWindow()
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
