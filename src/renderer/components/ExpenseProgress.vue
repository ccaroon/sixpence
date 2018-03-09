<template>
  <div>
    <v-progress-linear value="75" height="20" color="red accent-1"></v-progress-linear>
  </div>
</template>

<script>
export default {
  name: 'ExpenseProgress',

  props: ['entry']
}
</script>
