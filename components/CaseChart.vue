<template>
  <v-row no-gutters>
    <v-col xs="12" sm="12" lg="6">
      <VegaLite
        :chart-data="onFormatCases()"
        chart-title="Dice vs Cases"
        mark="point"
        :encoding="getEncoding('Dice')"
        chart-container="dice-case"
      ></VegaLite
    ></v-col>

    <v-col xs="12" sm="12" lg="6">
      <VegaLite
        :chart-data="onFormatCases('SDSC_2mm')"
        chart-title="Surface Dice vs Cases"
        mark="point"
        :encoding="getEncoding('Surface Dice')"
        chart-container="surface-dice-case"
      ></VegaLite>
    </v-col>
  </v-row>
</template>
<script>
import VegaLite from './VegaLite'
export default {
  name: 'CaseChart',
  components: { VegaLite },
  props: {
    formatData: {
      type: Function,
    },
  },
  methods: {
    onFormatCases(diceType = 'DSC') {
      return this.formatData(diceType)
    },
    getEncoding(chartTitle) {
      return {
        x: {
          field: 'caseNumber',
          title: 'Cases',
          type: 'quantitative',
          titleBaseline: 'top',
        },
        y: {
          field: 'value',
          type: 'quantitative',
          title: chartTitle,
          scale: { domain: [0.0, 1.0] },
        },
        color: {
          field: 'algorithm',
          legend: {
            orient: 'bottom',
            direction: 'horizontal',
          },
        },
        tooltip: [
          { field: 'caseNumber', title: 'case' },
          { field: 'value', title: 'value' },
        ],
      }
    },
  },
}
</script>
