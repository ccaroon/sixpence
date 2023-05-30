// https://www.electronjs.org/docs/latest/api/menu
import { BrowserWindow, Menu, MenuItem } from 'electron'

const isMac = process.platform === 'darwin'
const mainMetaKey = isMac ? 'Cmd' : 'Ctrl'
// -----------------------------------------------------------------------------
const aboutMenu = {
  label: 'About',
  click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
}

const settingsMenu = {
  label: 'Settings...',
  accelerator: mainMetaKey + '+,',
  click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-file-settings')
}

const macApp = [
  {
    label: 'Sixpence',
    submenu: [
      aboutMenu,
      { type: 'separator' },
      settingsMenu,
      { type: 'separator' },
      { role: 'hide' },
      { role: 'hideOthers' },
      { role: 'unhide' },
      { type: 'separator' },
      { role: 'quit' }
    ]
  }
]
// -----------------------------------------------------------------------------
// https://www.electronjs.org/docs/latest/api/menu#menuitems
const template = [
  ...(isMac ? macApp : []),
  {
    label: 'File',
    submenu: [
      ...(isMac ? [] : [settingsMenu]),
      { type: 'separator' },
      ...(isMac ? [] : [{ role: 'quit' }])
    ]
  },

  { role: 'editMenu' },

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
  { role: 'windowMenu' },
  {
    role: 'help',
    submenu: [
      ...(isMac ? [] : [aboutMenu]),
      {
        label: 'View on GitHub',
        click () { require('electron').shell.openExternal('https://github.com/ccaroon/sixpence') }
      },
      { role: 'toggleDevTools' }
    ]
  }
]

// -----------------------------------------------------------------------------
export default {
  setApplicationMenu: function () {
    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
  },
  addContext: function (window) {
    const ctxMenu = new Menu()
    ctxMenu.append(new MenuItem({
      label: 'Copy',
      role: 'copy'
    }))
    ctxMenu.append(new MenuItem({
      label: 'Paste',
      role: 'paste'
    }))
    ctxMenu.append(new MenuItem({
      type: 'separator'
    }))
    ctxMenu.append(new MenuItem({
      label: 'Dev Tools',
      role: 'toggleDevTools'
    }))

    window.webContents.on('context-menu',
      (event, click) => {
        event.preventDefault()
        ctxMenu.popup(window.webContents)
      },
      false
    )
  }
}
