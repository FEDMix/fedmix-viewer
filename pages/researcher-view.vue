<template>
  <v-container>
    <CaseChart :cases="cases" />
    <SliceChart :cases="cases" />
  </v-container>
</template>

<script>
import manifestParser from '../mixins/manifestParser'
import CaseChart from '../components/CaseChart'
import SliceChart from '../components/SliceChart'
export default {
  name: 'ResearcherView',
  components: { CaseChart, SliceChart },
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
