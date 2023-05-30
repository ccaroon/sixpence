# ToDo

## Main
* [ ] Config
  - [x] dataPath - moved to `settings.js`
  - [x] re-write like Cartaro's
  - [x] support DEV config file
* [ ] Backup
* [ ] Cleanup Handler
* [ ] Menu
  - [ ] About - Mac vs Others
  - [ ] Settings - Mac vs Others
  - [x] View Options
  - [-] Relies on ipcRender, i.e. nodeIntegration (found another way)

## Renderer
* [ ] Cleanup Handler
* [ ] Home Screen
* [ ] Budget Screen
* [ ] Expenses Screen
* [ ]

## Misc
* [ ] node integration on or off?
* [ ] Move DB code to main process
  1. Move BudgetDB & ExpenseDB modules to main
  2. Connect to Renderer process via IPC/ContextIsolation
