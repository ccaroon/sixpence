<template>
  <div>
    <v-row>
      <v-col>
        <v-text-field
          :label="name"
          :placeholder="value.toString()"
          outlined
          v-for="(value, name, index) in options"
          :key="index"
          v-model="options[name]"
        ></v-text-field>
      </v-col>
    </v-row>
  </div>
</template>
<script>
export default {
  name: 'SettingsOption',

  props: ['options']
}
</script>
