<template>
  <div :id="chartContainer"></div>
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
  computed: {
    def() {
      return {
        $schema: 'https://vega.github.io/schema/vega-lite/v4.0.json',
        title: this.chartTitle,
        data: {
          name: 'myData',
        },
        mark: this.mark,
        encoding: this.encoding,
        width: 400,
        height: 300,
        autosize: 'pad',
        padding: 5,
      }
    },
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
      embed('#' + this.chartContainer, this.def, 'vega-lite')
        .then((res) => res.view.insert('myData', this.chartData).run())
        .catch((err) => console.log(err))
    },
  },
}
</script>
