# ToDo

## Modernization

## Where Am I?
* Working on DBMigrations
  - unresolved promise in migration list `needsApplying` field causing "object annot be cloned" error

### Main
* [x] Config
  - [x] dataPath - moved to `settings.js`
  - [x] re-write like Cartaro's
  - [x] support DEV config file
* [ ] Backup
* [ ] Cleanup Handler
* [x] Menu
  - [x] About - Mac vs Others
  - [x] Settings - Mac vs Others
  - [x] View Options
  - [-] Relies on ipcRender, i.e. nodeIntegration (found another way)

### Renderer
* [ ] Cleanup Handler
* [ ] DBMigrations
* [ ] Home Screen
* [ ] Budget Screen
* [ ] Expenses Screen
* [ ] Settings Screen
  * [x] UI
  * [ ] save

### Misc
* [ ] node integration on or off?
* [ ] Move DB code to main process
  1. Move BudgetDB & ExpenseDB modules to main
  2. Connect to Renderer process via IPC/ContextIsolation
