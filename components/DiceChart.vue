<template>
  <div>
    Cases: {{ Object.entries(cases).length }}
    <br />
    <VegaLite
      :chart-data="formatCases()"
      :encoding="getEncoding('Dice')"
      chart-title="Dice vs Cases"
      mark="point"
      chart-container="dice"
    ></VegaLite>
    <!---->
    <VegaLite
      :chart-data="formatCases('SDSC_2mm')"
      :encoding="getEncoding('Surface Dice')"
      chart-title="Surface Dice vs Cases"
      mark="point"
      chart-container="surface-dice"
    ></VegaLite>
  </div>
</template>
<script>
import VegaLite from './VegaLite'
export default {
  name: 'DiceChart',
  components: { VegaLite },
  props: {
    cases: {
      type: Object,
      default() {
        return {}
      },
    },
  },
  watch: {
    cases() {
      console.log('Foo Changed!')
    },
  },
  methods: {
    formatCases(diceType = 'DSC') {
      const formattedCases = []
      Object.entries(this.cases).map((caseArray) => {
        Object.entries(caseArray[1].algorithms).map((algorithm) => {
          formattedCases.push({
            caseNumber: caseArray[0],
            value: algorithm[1].metrics[diceType].value_for_patient,
            algorithm: algorithm[0],
          })
        })
      })
      return formattedCases
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
        color: { field: 'algorithm' },
        tooltip: [
          { field: 'caseNumber', title: 'case' },
          { field: 'value', title: 'value' },
        ],
      }
    },
  },
}
</script>
