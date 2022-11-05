# ToDo

* [ ] Menu example using About
* [x] FontAwesome icons not working in built app -- shows a black square
* [x] Main Window
    - [x] Context Menu
      - [x] Copy
      - [x] Paste
      - [x] Dev Tools
* [x] Sub-Windows
    - [x] Hide Main Menu
    - [x] Context Menu
      - [x] Back
      - [x] Reload
      - [x] Copy
      - [x] Paste
* [x] Rename `window.js` to `windowHelper.js`
* [x] IPC import to lowercase
* [x] The `new-window` event is deprecated and will be removed.
      Please use contents.setWindowOpenHandler() instead.
* [-] ~~Fix "quit" events: 1 quit handler, then window events call `app.quit()`~~
    app.on('quit', () => {
      logger.debug('App Event: quit')
      quitApp()
    })
* [x] Node Module updates
