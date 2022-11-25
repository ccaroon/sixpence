// Config
// -----------------------------------------------------------------------------
class Config {
  constructor (data) {
    this.__data = data
  }

  get data () {
    return this.__data
  }

  get (path, defValue = null, isTransient = false) {
    const pathParts = path.split(':')
    let value = this.__data
    if (isTransient) {
      value = this.__data.__transient
    }

    pathParts.forEach((key) => {
      value = value[key]
    })

    if (value === undefined || value === null) {
      value = defValue
    }

    return value
  }

  getTransient (path, defValue = null) {
    return this.get(path, defValue, true)
  }

  set (path, value, isTransient = false) {
    const pathParts = path.split(':')
    const key = pathParts.pop()
    let data = this.__data
    if (isTransient) {
      data = this.__data.__transient
    }

    pathParts.forEach((item) => {
      data = data[item]
    })
    data[key] = value
  }

  setTransient (path, value) {
    this.set(path, value, true)
  }
}
// -----------------------------------------------------------------------------
export default Config
