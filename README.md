# daikon
An example [Electron] + [VueJS] + [Vuetify] application.

Created using:
* [vue-cli]
* [vue-cli-plugin-electron-builder]
  - [electron-builder]
* [vue-cli-plugin-vuetify]

## Usage
Copy/Fork; Rename; Update; Make Something Great; Profit!

## Features
* [Electron] App
* [VueJS]
* [Vuetify] for UI
* [MDI Icons]
* [FontAwesome] Free Icons
* [mousetrap]


## Getting Started
This project is built and developed using NodeJS v16.

### Project setup
```
npm install
```

### Compile with hot-reloads for development
```
npm run electron:serve
```

### Build Electron App (for current OS)
```
npm run electron:build
```

## Choices
### Context Isolation vs Node Integration
This app is set up to use [**Context Isolation**](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
by default in Electron. This is the most secure way of having the Renderer process
communicate with the Main process.

The "Transmogrify" button on the app's main screen is an example of using **Context
Isolation**.

See the `src/main/preload.js`, `src/main/ipc.js`, `src/main/main.js` and
`src/main/Napiform.js` code for how that is set up.

-----

The other option is to enable **Node Integration** in the Renderer process. This allows
code in the Renderer process to access NodeJS APIs.

**Context Isolation** and **Node Integration** do not work together. It's one or the other.

More Security information [here](https://www.electronjs.org/docs/latest/tutorial/security)


## Things You Might Want to Update
* `README.md`
* `package.json` (`name`, `author`, `description`, etc)
* Icons in `build/`
* Images and `favicon.ico` in `public/`
* Logo images in `src/renderer/assets`
* `src/renderer/Components/*`
* Routes in `src/renderer/router/index.js`
* `src/renderer/App.vue` -- Application container


[Electron]: https://www.electronjs.org/docs/latest/
[VueJS]: https://v2.vuejs.org/v2/guide/index.html
[Vuetify]: https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
[MDI Icons]: https://materialdesignicons.com/
[FontAwesome]: https://fontawesome.com/icons
[vue-cli]: https://cli.vuejs.org/
[electron-builder]: https://www.electron.build/
[vue-cli-plugin-electron-builder]: https://nklayman.github.io/vue-cli-plugin-electron-builder/
[vue-cli-plugin-vuetify]: https://github.com/vuetifyjs/vue-cli-plugins/tree/master/packages/vue-cli-plugin-vuetify
[mousetrap]: https://craig.is/killing/mice
