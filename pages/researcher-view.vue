<template>
  <div>
    <DiceChart :cases="cases" />
  </div>
</template>

<script>
import manifestParser from '../mixins/manifestParser'
import DiceChart from '../components/DiceChart'
export default {
  name: 'ResearcherView',
  components: { DiceChart },
  mixins: [manifestParser],
  data() {
    return {
      manifest: File,
      scan_files: [],
      result: {},
      cases: {},
    }
  },

  created() {
    const fileName = this.$route.query.name
    const selectedFolder = this.$route.params.selected_folders[fileName]
    this.manifest = selectedFolder.manifest
    this.scan_files = selectedFolder.images
  },
  mounted() {
    this.getManifestText().then((manifestText) => {
      this.manifest = this.parseManifest(manifestText, this.scan_files)
      this.result = { ...manifestText }
      this.cases = manifestText.cases
      this.scan_files.map((file) => {
        this.filterScans(file)
      })
    })
  },

  methods: {
    async getManifestText() {
      const text = await this.manifest.text()
      return JSON.parse(text)
    },
  },
}
</script>
