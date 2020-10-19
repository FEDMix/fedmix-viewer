<template>
  <v-row no-gutters>
    <v-col cols="12" sm="12" md="6">
      <VegaLite
        :chart-data="onFormatData()"
        chart-title="Dice vs Case Slice"
        mark="point"
        :encoding="getEncoding('Dice')"
        chart-container="dice-slice"
      >
      </VegaLite>
    </v-col>
    <v-col cols="12" sm="12" md="6">
      <VegaLite
        :chart-data="onFormatData()"
        chart-title="Surface Dice vs Case Slice"
        mark="point"
        :encoding="getEncoding('Surface Dice')"
        chart-container="surface-dice-slice"
      >
      </VegaLite>
    </v-col>
  </v-row>
</template>
<script>
import VegaLite from './VegaLite'
export default {
  name: 'SliceChart',
  components: { VegaLite },
  props: {
    formatData: {
      type: Function,
    },
  },

  methods: {
    onFormatData(diceType = 'DSC') {
      return this.formatData()
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
