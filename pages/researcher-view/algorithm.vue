<template>
  <div>
    <v-row no-gutters>
      <v-col cols="12" sm="12" md="6">
        <v-slider
          v-if="sliderData.length"
          v-model="sliderValue"
          label="Cases"
          :max="sliderData.length - 1"
          thumb-label="always"
        >
          <template v-slot:thumb-label>
            {{ sliderData[sliderValue] }}
          </template>
        </v-slider>
      </v-col>
      <v-col cols="12" sm="12" md="6">
        <v-select
          v-model="selectedAlgorithm"
          :items="getAlgorithms()"
          item-text="state"
          label="Select Algorithm"
        ></v-select>
      </v-col>
    </v-row>
    <!-- <CaseChart :cases="cases" /> -->
    <SliceChart :formatData="formatData" />
  </div>
</template>

<script>
import data from '~/static/mocked-data/cases'
export default {
  name: 'Algorithm',

  data() {
    return {
      cases: data,
      selectedAlgorithm: 'all',
      sliderValue: 0,
    }
  },
  computed: {
    sliderData() {
      return Object.keys(this.cases)
    },
    caseNo() {
      return this.sliderData[this.sliderValue]
    },
  },
  // async asyncData({ $axios }) {
  //   // API - '/datasets/{id}'
  //   // const cases = await $axios.$get('/mocked-data/cases.json')
  //   // return { cases }
  //   const { data } = await $axios.$get('/mocked-data/cases.json')
  //   console.log('data', data)
  //   return { data }
  // },
  methods: {
    formatData(diceType = 'DSC') {
      const formattedData = []
      Object.entries(this.cases[this.caseNo]?.algorithms).map((algorithm, i) => {
        algorithm[1].metrics[diceType].values_per_slice.map((dice, j) => {
          if (algorithm[0] === this.selectedAlgorithm) {
            formattedData.push({
              slice: j,
              dice,
              algorithm: algorithm[0],
            })
          } else if (this.selectedAlgorithm === 'all') {
            formattedData.push({
              slice: j,
              dice,
              algorithm: algorithm[0],
            })
          }
        })
      })
      return formattedData
    },
    getAlgorithms() {
      if (this.cases && Object.keys(this.cases).length > 0) {
        const algorithms = Array.from(Object.keys(this.cases[10].algorithms))
        algorithms.push('all')
        return algorithms
      }
    },
  },
}
</script>

<style scoped></style>
