<template>
  <v-container>
    <v-row>
      <v-col cols="2">
        <v-icon size="128" color="black">mdi-map-marker</v-icon>
      </v-col>
      <v-col>
        <div class="text-h1">{{ $route.name }}</div>
        {{ $route.params.icon }}
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'placeholder-main',

  methods: { },

  data: () => ({})
}
</script>
