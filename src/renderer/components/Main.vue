<template>
  <div>
    <About></About>
    <Budget></Budget>
</div>
</template>

<script>
  import About from './About'
  import Budget from './Budget'

  export default {
    name: 'Main',
    components: { About, Budget },

    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    },

    data () {
      return {}
    }
  }
</script>