import Moment from 'moment'
import Config from './config'

const fs = require('fs')
const zipLib = require('zip-lib')

function cleanup () {
  var backupPath = Config.get('backup:path')
  var numToKeep = Config.get('backup:keep')

  var allFiles = fs.readdirSync(backupPath)
  var zipFiles = allFiles.filter(filename => filename.endsWith('.zip'))

  if (zipFiles.length > numToKeep) {
    zipFiles.sort()

    var delFiles = zipFiles.slice(0, -1 * numToKeep)
    delFiles.forEach(filename => {
      fs.unlinkSync(`${backupPath}/${filename}`)
    })
  }
}

export default {
  backup: function () {
    var promise = null

    Config.load()

    if (!fs.existsSync(Config.get('backup:path'))) {
      fs.mkdirSync(Config.get('backup:path'), '0750')
    }

    // Clean up old backups
    cleanup()

    // Backup Data Files
    var suffix = Moment().format('YYYYMMDD-HHmm')
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
