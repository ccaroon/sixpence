
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
//   option1: value1,
//   option2: value2,
// }
// METADATA describes the various groups and options.
// Used by the UI
const METADATA = {
  backup: {
    keep: { type: 'NUMBER', icon: 'mdi-counter', desc: 'The number of backup files to keep', default: 5 },
    path: { type: 'FILE', icon: 'mdi-folder', desc: 'Directory where backup files are stored', default: `${dataPath}/backups` }
  }
}

// Generate DEFAULTS from METADATA
var DEFAULTS = {}
for (let [group, options] of Object.entries(METADATA)) {
  DEFAULTS[group] = {}
  for (let [name, mdata] of Object.entries(options)) {
    DEFAULTS[group][name] = mdata.default
  }
}

// -----------------------------------------------------------------------------
export default {
  // NOT user configurable
  configFile: configFile,
  dataPath: dataPath,
  metaData: METADATA,

  get: function (path = null) {
    var option = configData

    if (path !== null) {
      var pathParts = path.split(':')

      pathParts.forEach((key) => {
        option = option[key]
      })
    }

    return option
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
