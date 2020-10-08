<template>
  <div id="viz"></div>
</template>
<script>
import embed from 'vega-embed'
export default {
  props: {
    chartData: {
      type: Array,
      default() {
        return []
      },
    },
    mark: { type: String, default: 'point' },
    encoding: {
      type: Object,
      default() {
        return {}
      },
    },
  },
  data() {
    return {
      def: {
        $schema: 'https://vega.github.io/schema/vega-lite/v2.0.json',
        description: 'A simple bar chart with embedded data.',
        data: {
          values: this.chartData,
        },
        mark: this.mark,
        encoding: this.encoding,
      },
    }
  },
  async mounted() {
    await embed('#viz', this.def, { actions: false })
  },
}
</script>
