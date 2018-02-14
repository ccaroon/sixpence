<template>
  <div>
    <v-text-field
      name="name"
      label="What's Your Name"
      id="your_name"
      v-model="name">
    </v-text-field>
    <v-text-field
      name="age"
      label="How Old Are You"
      id="your_age"
      v-model="age">
    </v-text-field>
    <v-text-field
      name="job"
      label="What's Your Job Title"
      id="your_title"
      v-model="title">
    </v-text-field>
    <v-btn color="primary" @click="saveRecord()">Save</v-btn>
  </div>
</template>

<script>
import Datastore from 'nedb'

export default {
  name: 'DBTest',

  mounted () {
    // this.db = new Datastore({
    //   filename: '/Users/ccaroon/Downloads/budget.spx',
    //   autoload: true,
    //   timestampData: true
    // })
  },

  methods: {
    saveRecord: function () {
      var doc = {
        name: this.name,
        age: this.age,
        job: this.title
      }
      this.db.insert(doc, function (err, newDoc) {
        if (err) {
          console.log(err)
        } else {
          console.log(doc.name + '|' + newDoc._id)
        }
      })

      // ----------------
      var doc2 = {
        budget: [
          {
            category: 'Auto:Loan',
            note: '2017 Honda Civic Sport',
            frequency: 1, // in months
            amount: 235.17
          }
        ]
      }

      this.db.insert(doc2, function (err, newDoc) {
        if (err) {
          console.log(err)
        } else {
          console.log(newDoc)
        }
      })
    }
  },

  data () {
    return {
      db: null,
      name: null,
      age: null,
      title: null
    }
  }
}
</script>
