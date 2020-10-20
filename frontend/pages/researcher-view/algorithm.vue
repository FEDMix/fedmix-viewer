<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12" md="6" align-self="center">
        <v-select
          v-model="selectedAlgorithm"
          :items="getAlgorithms()"
          item-text="state"
          label="Select Algorithm"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="12" md="6" align-self="center">
        <v-subheader>Case No: {{ sliderData[sliderValue] }}</v-subheader>
        <v-slider
          v-if="sliderData.length"
          v-model="sliderValue"
          :max="sliderData.length - 1"
          :thumb-size="20"
        >
          <template v-slot:thumb-label>
            {{ sliderData[sliderValue] }}
          </template>
        </v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <CaseChart :format-data="formatCases" />
      </v-col>
      <v-col cols="12" md="6">
        <SliceChart :format-data="formatSliceChartData" />
      </v-col>
    </v-row>
  </v-container>
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
  methods: {
    formatCases(diceType) {
      const formattedCases = []
      Object.entries(this.cases).map((caseArray) => {
        Object.entries(caseArray[1].algorithms).map((algorithm) => {
          if (algorithm[0] === this.selectedAlgorithm) {
            formattedCases.push({
              caseNumber: caseArray[0],
              value: algorithm[1].metrics[diceType].value_for_patient,
              algorithm: algorithm[0],
            })
          } else if (this.selectedAlgorithm === 'all') {
            formattedCases.push({
              caseNumber: caseArray[0],
              value: algorithm[1].metrics[diceType].value_for_patient,
              algorithm: algorithm[0],
            })
          }
        })
      })
      return formattedCases
    },
    formatSliceChartData(diceType) {
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
