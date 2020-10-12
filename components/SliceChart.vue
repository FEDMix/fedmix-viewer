<template>
  <v-col>
    <v-row no-gutters>
      <v-col cols="12" sm="12" md="6">
        <v-slider
          v-model="sliderValue"
          label="Cases"
          :max="sliderData.length - 1"
          thumb-label="always"
        >
          <template v-slot:thumb-label>
            {{ sliderData[sliderValue] }}
          </template></v-slider
        >
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
    <v-row no-gutters>
      <v-col cols="12" sm="12" md="6">
        <VegaLite
          :chart-data="formatData()"
          chart-title="Dice vs Case Slice"
          mark="point"
          :encoding="getEncoding('Dice')"
          chart-container="dice-slice"
        >
        </VegaLite>
      </v-col>
      <v-col cols="12" sm="12" md="6">
        <VegaLite
          :chart-data="formatData('SDSC_2mm')"
          chart-title="Surface Dice vs Case Slice"
          mark="point"
          :encoding="getEncoding('Surface Dice')"
          chart-container="surface-dice-slice"
        >
        </VegaLite>
      </v-col>
    </v-row>
  </v-col>
</template>
<script>
import VegaLite from './VegaLite'
export default {
  name: 'SliceChart',
  components: { VegaLite },
  props: {
    cases: {
      type: Object,
      default() {
        return {}
      },
    },
  },
  data() {
    return {
      selectedAlgorithm: 'all',
      sliderValue: 5,
      caseNo: 0,
    }
  },
  computed: {
    sliderData() {
      return Object.keys(this.cases)
    },
  },
  watch: {
    sliderValue(newValue) {
      this.caseNo = this.sliderData[this.sliderValue]
    },
  },
  mounted() {
    this.sliderValue = 1
  },
  methods: {
    formatData(diceType = 'DSC') {
      const formattedData = []
      if (Object.keys(this.cases).length > 0 && this.caseNo) {
        Object.entries(this.cases[this.caseNo].algorithms).map(
          (algorithm, i) => {
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
          }
        )
      }
      return formattedData
    },
    getAlgorithms() {
      if (Object.keys(this.cases).length > 0) {
        const algorithms = Array.from(Object.keys(this.cases[10].algorithms))
        algorithms.push('all')
        return algorithms
      }
    },
    getEncoding(chartTitle) {
      return {
        x: {
          field: 'slice',
          title: 'Slice',
          type: 'quantitative',
        },
        y: {
          field: 'dice',
          type: 'quantitative',
          title: chartTitle,
          scale: { domain: [0.0, 1.0] },
        },
        color: { field: 'algorithm' },
        tooltip: [
          { field: 'slice', title: 'Slice' },
          { field: 'dice', title: 'Dice' },
        ],
      }
    },
  },
}
</script>
