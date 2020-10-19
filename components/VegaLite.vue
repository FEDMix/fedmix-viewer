<template>
  <div :id="chartContainer" class="chart-container"></div>
</template>
<script>
import embed from 'vega-embed'
export default {
  props: {
    chartTitle: { type: String, default: '' },
    chartData: { type: Array, default: () => [] },
    mark: { type: String, default: 'point' },
    encoding: { type: Object, default: () => ({}) },
    chartContainer: { type: String, default: '' },
  },
  data() {
    return {
      def: {
        $schema: 'https://vega.github.io/schema/vega-lite/v4.0.json',
        title: this.chartTitle,
        data: {
          name: 'myData',
        },
        mark: this.mark,
        encoding: this.encoding,
        width: 'container',
        height: 300,
        autosize: {
          type: 'fit',
          resize: true,
          contains: 'padding',
        },
      },
    }
  },
  mounted() {
    this.draw()
  },
  watch: {
    chartData(newValue) {
      this.draw()
    },
  },

  methods: {
    draw() {
      embed('#' + this.chartContainer, this.def, { actions: false })
        .then((res) => res.view.insert('myData', this.chartData).run())
        .catch((err) => console.log(err))
    },
  },
}
</script>
<style>
.chart-container {
  width: 80%;
}
</style>
