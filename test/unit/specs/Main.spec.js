import Vue from 'vue'
import Main from '@/components/Main'

describe('Main.vue', () => {
  it('should render correct contents', () => {
    const vm = new Vue({
      el: document.createElement('div'),
      render: h => h(Main)
    }).$mount()

    expect(vm.$el.querySelector('#main-app-name').textContent).to.contain('Sixpence')

    /* eslint-disable no-unused-expressions */
    expect(vm.$el.querySelector('#main-budget-button')).to.exist
    expect(vm.$el.querySelector('#main-expense-button')).to.exist

    expect(vm.$el.querySelector('#main-bottom-space').textContent).to.contain('This space intentionally left blank.')
  })
})
