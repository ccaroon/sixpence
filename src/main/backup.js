import Moment from 'moment'
import Config from './config'

const fs = require('fs')
const zipLib = require('zip-lib')

export default {
  backup: function () {
    var promise = null

    Config.load()

    if (!fs.existsSync(Config.get('backup:path'))) {
      fs.mkdirSync(Config.get('backup:path'), '0750')
    }

    // Backup Data Files
    var suffix = Moment().format('YYYYMMDD-hhmm')
    var zipFileName = `${Config.get('backup:path')}/Sixpence-${suffix}.zip`

    if (!fs.existsSync(zipFileName)) {
      var allFiles = fs.readdirSync(Config.dataPath)
      var dataFiles = allFiles.filter(filename => filename.endsWith('.sxp'))

      var zipFile = new zipLib.Zip()
      zipFile.addFile(Config.configFile)
      dataFiles.forEach(filename => zipFile.addFile(`${Config.dataPath}/${filename}`))

      promise = zipFile.archive(zipFileName)
    } else {
      promise = Promise.resolve(true)
    }

    return promise
  }
}
