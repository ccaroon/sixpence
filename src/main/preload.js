const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('Main', {
  newWindow: (location, width, height) => {
    ipcRenderer.invoke('main:newWindow', location, width, height)
  }
})

contextBridge.exposeInMainWorld('BudgetDB', {
  count: (searchTerms) => {
    return ipcRenderer.invoke('budget-db:count', searchTerms)
  }
})

contextBridge.exposeInMainWorld('Config', {
  data: () => {
    return ipcRenderer.invoke('config:data')
  }
})

contextBridge.exposeInMainWorld('DBMigrations', {
  check: () => {
    return ipcRenderer.invoke('db-migrations:check')
  },

  execute: (migName) => {
    return ipcRenderer.invoke('db-migrations:execute', migName)
  }
})

contextBridge.exposeInMainWorld('NodeJS', { process })

contextBridge.exposeInMainWorld('Modules', {
  vuejs: {
    version: require('vue/package.json').version
  }
})

// Menu Action Handler Registration
contextBridge.exposeInMainWorld('Menu', {
  registerHandler: (menuId, callback) => ipcRenderer.on(menuId, callback)
})
