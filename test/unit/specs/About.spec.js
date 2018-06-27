import Vue from 'vue'
import About from '@/components/About'

const pkgJson = require(`../../../package.json`)

describe('About.vue', () => {
  it('should render correct contents', () => {
    const vm = new Vue({
      el: document.createElement('div'),
      render: h => h(About)
    }).$mount()

    expect(vm.$el.querySelector('#about-title').textContent.trim()).to.equal(pkgJson.name + ' v' + pkgJson.version)

    expect(vm.$el.querySelector('#about-tech-electron').textContent).to.equal('2.0.2')
    expect(vm.$el.querySelector('#about-tech-nodejs').textContent).to.equal('8.9.3')
    expect(vm.$el.querySelector('#about-tech-chrome').textContent).to.equal('61.0.3163.100')
    expect(vm.$el.querySelector('#about-tech-platform').textContent).to.equal('darwin')
    expect(vm.$el.querySelector('#about-tech-vueversion').textContent).to.equal('2.5.16')
  })
})
