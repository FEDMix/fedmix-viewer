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
      <v-col v-for="(algorithm, index) in algorithms" :key="algorithm" xs="12" sm="6" lg="3">
        <div class="d-flex flex-column align-center relative">
          <v-dialog width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="compare"
                v-on="on"
                v-bind="attrs"
                v-if="index === algorithms.length - 1"
                :disabled="selected.length < 2"
              >
                Compare
              </v-btn>
            </template>
            <div class="d-flex">
              <v-card>
                <ScansCompare
                  :cases="cases"
                  :selectedAlgorithms="selected"
                  :caseNo="caseNo"
                  :sliceNo="sliceNo"
                ></ScansCompare>
              </v-card>
            </div>
          </v-dialog>
          <v-checkbox
            v-model="selected"
            :label="algorithm"
            :value="algorithm"
            :disabled="algorithm === 'ground_truth'"
          ></v-checkbox>
          <ScansGrid
            :cases="scans"
            :algorithm="algorithm"
            :caseNo="caseNo"
            :sliceNo="sliceNo"
            :distanceThreshold="surfaceDice"
          ></ScansGrid>
        </div>
      </v-col>
      {{ selected }}
    </v-row>
  </v-container>
</template>

<script>
import scansData from '~/static/mocked-data/data_artificial/manifest'
import ScansGrid from '~/components/ScansGrid'
import ScansCompare from '~/components/ScansCompare'
export default {
  name: 'Algorithm',
  components: { ScansGrid, ScansCompare },
  data() {
    return {
      scans: scansData,
      cases: scansData.cases,
      selectedAlgorithm: 'all',
      caseValue: 0,
      sliceValue: 0,
      surfaceDice: 1,
      allAlgorithms: [],
      algorithms: ['ground_truth'],
      selected: [],
    }
  },
  computed: {
    caseNumbers() {
      return Object.keys(this.cases)
    },
    caseNo() {
      return this.caseNumbers[this.caseValue]
    },
    slicesNumbers() {
      return Object.keys(this.cases[this.caseNo]['scans'])
    },
    sliceNo() {
      return this.slicesNumbers[this.sliceValue]
    },
  },
  mounted() {
    this.getAlgorithms()
    this.allAlgorithms = [...this.algorithms]
    this.allAlgorithms.shift()
    this.allAlgorithms.push('all')
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
      for (const algorithm of this.scans.metadata.clusters) {
        this.algorithms.push(algorithm.name)
      }
      return this.algorithms
    },
  },
}
</script>

<style scoped>
.relative {
  position: relative;
}
.compare {
  position: absolute;
  right: 0px;
  top: -20px;
}
</style>
