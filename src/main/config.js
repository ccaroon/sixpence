
var app
if (process.type === 'renderer') {
  app = require('electron').remote.app
} else {
  app = require('electron').app
}

const fs = require('fs')
const path = require('path')

const dataPath = path.join(app.getPath('documents'), 'Sixpence')
const configFile = `${dataPath}/SixpenceCfg.json`

var configData = {}

// Basic Layout
// - Every option is assumed to be in a "group"
// - Groups are assumed to be only 1 level deep
// -------
// group: {
//   option1: null,
//   option2: null,
// }
const DEFAULTS = {
  backup: {
    keep: 5,
    path: `${dataPath}/backups`
  }
}
// -----------------------------------------------------------------------------
export default {
  // NOT user configurable
  configFile: configFile,
  dataPath: dataPath,

  get: function (path = null) {
    var value = configData

    if (path !== null) {
      var pathParts = path.split(':')

      pathParts.forEach((key) => {
        value = value[key]
      })
    }

    return value
  },

  set: function (path, value) {
    console.log(`SET: Not yet implemented- [${path}] -> [${value}]`)
  },

  load: function () {
    if (fs.existsSync(configFile)) {
      var contents = fs.readFileSync(configFile)
      var data = JSON.parse(contents)

      configData = Object.assign({}, DEFAULTS, data)
    } else {
      // Config file does not exist...
      // 1. Set to defaults
      // 2. Create it.
      configData = DEFAULTS
      this.save()
    }
  },

  save: function () {
    var json = JSON.stringify(configData)
    fs.writeFileSync(configFile, json)
  }
}
