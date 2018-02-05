<template>
  <div>
    <!-- <SystemInformation></SystemInformation> -->
    <hr>
    <DBTest></DBTest>
</div>
</template>

<script>
  import SystemInformation from './LandingPage/SystemInformation'
  import DBTest from './DBTest'

  export default {
    name: 'landing-page',
    components: { SystemInformation, DBTest },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    }
  }
</script>
