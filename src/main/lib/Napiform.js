// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------
class Napiform {
  constructor (msg1, msg2) {
    this.message1 = msg1
    this.message2 = msg2
  }

  transmogrify () {
    const data = `${this.message1}|${this.message2}`
    return data.replaceAll(/[a-zA-Z]/g, '1').replaceAll(/[^1a-zA-Z]/g, '0')
  }
}
// -----------------------------------------------------------------------------
export default Napiform
