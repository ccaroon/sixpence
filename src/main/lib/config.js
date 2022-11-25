// Config Instance
// -----------------------------------------------------------------------------
import fs from 'fs'
import settings from './settings'

import Config from '../../shared/Config'
// -----------------------------------------------------------------------------
const DEFAULTS = {
  backup: {
    keep: 5,
    path: `${settings.dataPath}/backups`
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
const configInstance = new Config(configData)
// -----------------------------------------------------------------------------
export default configInstance
