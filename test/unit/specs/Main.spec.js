import Vue from 'vue'
import Main from '@/components/Main'

describe('Main.vue', () => {
  it('should render correct contents', () => {
    const vm = new Vue({
      el: document.createElement('div'),
      render: h => h(Main)
    }).$mount()

    expect(vm.$el.querySelector('#app_name').textContent).to.contain('Sixpence')
  })
})
