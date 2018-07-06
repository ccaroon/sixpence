import Vue from 'vue'
import Budget from '@/components/Budget'

describe('Budget.vue', () => {
  it('should render correct contents', () => {
    const vm = new Vue({
      el: document.createElement('div'),
      render: h => h(Budget)
    }).$mount()

    expect(vm.$el.querySelector('#budget-toolbar-title').textContent).to.equal('Budget')

    /* eslint-disable no-unused-expressions */
    expect(vm.$el.querySelector('#budget-freq-filter')).to.exist
  })
})
