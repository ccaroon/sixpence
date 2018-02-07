<template>
  <div>
    <About></About>
</div>
</template>

<script>
  import About from './About'
  // import DBTest from './DBTest'

  export default {
    name: 'Main',
    components: { About },

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
