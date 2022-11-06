import { app } from 'electron'
import path from 'path'

export default {
  dataPath: path.join(app.getPath('documents'), 'Sixpence')
}
