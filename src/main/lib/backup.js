import Moment from 'moment'
import Config from './config'

const fs = require('fs')
const zipLib = require('zip-lib')

function cleanup () {
  const backupPath = Config.get('backup:path')
  const numToKeep = Config.get('backup:keep')

  const allFiles = fs.readdirSync(backupPath)
  const zipFiles = allFiles.filter(filename => filename.endsWith('.zip'))

  if (zipFiles.length > numToKeep) {
    zipFiles.sort()

    const delFiles = zipFiles.slice(0, -1 * numToKeep)
    delFiles.forEach(filename => {
      fs.unlinkSync(`${backupPath}/${filename}`)
    })
  }
}

export default {
  backup: function () {
    let promise = null

    Config.load()

    if (!fs.existsSync(Config.get('backup:path'))) {
      fs.mkdirSync(Config.get('backup:path'), '0750')
    }

    // Clean up old backups
    cleanup()

    // Backup Data Files
    const suffix = Moment().format('YYYYMMDD-HHmm')
    const zipFileName = `${Config.get('backup:path')}/Sixpence-${suffix}.zip`

    if (!fs.existsSync(zipFileName)) {
      const allFiles = fs.readdirSync(Config.dataPath)
      const dataFiles = allFiles.filter(filename => filename.endsWith('.sxp'))

      const zipFile = new zipLib.Zip()
      zipFile.addFile(Config.configFile)
      dataFiles.forEach(filename => zipFile.addFile(`${Config.dataPath}/${filename}`))

      promise = zipFile.archive(zipFileName)
    } else {
      promise = Promise.resolve(true)
    }

    return promise
  }
}
