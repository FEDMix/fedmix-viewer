<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12" md="3" align-self="center">
        <v-select
          v-model="selectedAlgorithm"
          :items="allAlgorithms"
          item-text="state"
          label="Select Algorithm"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="12" md="3" align-self="center">
        <v-subheader>Case No: {{ caseNumbers[caseValue] }}</v-subheader>
        <v-slider
          v-if="caseNumbers.length"
          v-model="caseValue"
          :max="caseNumbers.length - 1"
          :thumb-size="20"
        >
          <template v-slot:thumb-label>
            {{ caseNumbers[caseValue] }}
          </template>
        </v-slider>
      </v-col>
      <v-col cols="12" sm="12" md="3" align-self="center">
        <v-subheader>Slice No: {{ slicesNumbers[sliceValue] }}</v-subheader>
        <v-slider
          v-if="slicesNumbers.length"
          v-model="sliceValue"
          :max="slicesNumbers.length - 1"
          :thumb-size="20"
        >
          <template v-slot:thumb-label>
            {{ slicesNumbers[sliceValue] }}
          </template>
        </v-slider>
      </v-col>
      <v-col cols="12" sm="12" md="3" align-self="center">
        <v-subheader>Surface Dice: {{ surfaceDice }}</v-subheader>
        <v-slider v-model="surfaceDice" min="1" max="10" :thumb-size="20"> </v-slider>
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
    <v-row>
      <v-col v-for="algorithm in algorithms" :key="algorithm" xs="12" sm="6" lg="3">
        <ScansGrid
          :cases="cases"
          :algorithm="algorithm"
          :caseNo="caseNo"
          :sliceNo="sliceNo"
          :distanceThreshold="surfaceDice"
        ></ScansGrid>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import datasets_query from '~/apollo/datasets_select'
import ScansGrid from '~/components/ScansGrid'
export default {
  name: 'Algorithm',
  components: { ScansGrid },
  apollo: {
    datasets: {
      query: datasets_query,
      prefetch({ route }) {
        return {
          ids: [route.params.dataset_id],
        }
      },
      variables() {
        return {
          ids: [this.$route.params.dataset_id],
        }
      },
      result(data, key) {
        this.dataset = data.data.datasets[0]
        this.getAlgorithms()
        this.cases = this.dataset.cases
      },
      error(error) {
        console.log(JSON.stringify(error.message))
      },
    },
  },
  data() {
    return {
      cases: [],
      dataset: {},
      algorithms: [],
      selectedAlgorithm: 'all',
      caseValue: 0,
      sliceValue: 0,
      surfaceDice: 1,
      allAlgorithms: [],
    }
  },
  computed: {
    caseNumbers() {
      return this.cases.map((cs) => cs.id)
    },
    caseNo() {
      return this.caseNumbers[this.caseValue]
    },
    slicesNumbers() {
      if (this.caseNumbers.includes(this.caseNo)) {
        const the_case = this.cases.find((cs) => cs.id === this.caseNo)
        return Object.keys(the_case['scans'])
      } else {
        return []
      }
    },
    sliceNo() {
      return this.slicesNumbers[this.sliceValue]
    },
  },
  mounted() {},
  methods: {
    formatCases(diceType) {
      const formattedCases = []
      if (this.cases.length) {
        this.cases.map((the_case) => {
          the_case.algorithms.map((algorithm) => {
            if (algorithm.name === this.selectedAlgorithm || this.selectedAlgorithm === 'all') {
              const metric = algorithm.metrics.find((metric) => metric.name == diceType)
              formattedCases.push({
                caseNumber: the_case.id,
                value: metric.valueForCase,
                algorithm: algorithm.name,
              })
            }
          })
        })
      }
      return formattedCases
    },
    formatSliceChartData(diceType) {
      const formattedData = []
      const the_case = this.cases.find((cs) => cs.id === this.caseNo)
      if (the_case) {
        the_case.algorithms.map((algorithm) => {
          if (algorithm.name === this.selectedAlgorithm || this.selectedAlgorithm === 'all') {
            const metric = algorithm.metrics.find((metric) => metric.name == diceType)
            let formatted = metric.valuesPerSlice.map((dice, j) => {
              return {
                slice: j,
                dice,
                algorithm: algorithm.name,
              }
            })
            formattedData.push(...formatted)
          }
        })
      }
      return formattedData
    },
    getAlgorithms() {
      this.algorithms = ['ground_truth']
      this.allAlgorithms = []
      for (const algorithm of this.dataset.clusters) {
        this.algorithms.push(algorithm.name)
        this.allAlgorithms.push(algorithm.name)
      }
      this.allAlgorithms.push('all')
    },
  },
}
</script>

<style scoped></style>
