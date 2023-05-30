// Config Instance
// -----------------------------------------------------------------------------
import fs from 'fs'
import settings from './settings'

import Config from '../../shared/Config'
// -----------------------------------------------------------------------------
const METADATA = {
  backup: {
    keep: {
      type: 'NUMBER',
      icon: 'mdi-counter',
      desc: 'The number of backup files to keep',
      default: 5
    },
    path: {
      type: 'FILE',
      icon: 'mdi-folder',
      desc: 'Directory where backup files are stored',
      default: `${settings.dataPath}/backups`
    }
  }
}

const DEFAULTS = {
  backup: {
    keep: METADATA.backup.keep.default,
    path: METADATA.backup.path.default
  }
}

// -----------------------------------------------------------------------------
function load (filePath) {
  let data = null
  if (fs.existsSync(filePath)) {
    const contents = fs.readFileSync(filePath)
    const jsonData = JSON.parse(contents)

    data = Object.assign({}, {}, jsonData)
  } else {
    data = DEFAULTS
  }

  data.__transient = {}
  return data
}
// -----------------------------------------------------------------------------
// function save (filePath, data) {
//   const json = JSON.stringify(data)
//   fs.writeFileSync(filePath, json)
// }
// -----------------------------------------------------------------------------
const suffix = process.env.NODE_ENV === 'development' ? '-dev' : ''
const configFile = `${settings.dataPath}/SixpenceCfg${suffix}.json`
const configData = load(configFile)
const configInstance = new Config(configData, METADATA)
// -----------------------------------------------------------------------------
export default configInstance
