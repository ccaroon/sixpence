<template>
<div>
  <v-jumbotron color="green lighten-1">
    <v-container fill-height>
      <v-layout align-center row>
        <v-flex xs1>
          <img src="../assets/logo.png"></img>
        </v-flex>
        <v-flex text-xs-center>
          <h3 class="display-3">Sixpence</h3>
          A Simple Budget Manager
        </v-flex>
      </v-layout>
    </v-container>
  </v-jumbotron>
  <v-container>
    <v-layout align-center row>
      <v-flex text-xs-center>
        <v-btn large color="green" @click="$router.push(`/budget`)">
          <v-icon>mdi-format-list-checks</v-icon>&nbsp;&nbsp;Budget
        </v-btn>
        <v-btn large color="red" @click="$router.push(`/expenses`)">
          <v-icon>mdi-currency-usd</v-icon> Expenses
        </v-btn>
      </v-flex>
    </v-layout>
  </v-container>
  <v-divider></v-divider>
  <div text-xs-center>This space intentionally left blank.</div>
</div>
</template>

<script>
export default {
  name: 'Main',

  data () {
    return {}
  }
}
</script>
