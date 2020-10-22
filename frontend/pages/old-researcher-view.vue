<template>
  <div>
    <div class="container">
      <div v-for="algorithm in algorithms" :key="algorithm">
        <OldScanCanvas
          :multi-file-dict="multiFileDict"
          :case="caseNo"
          :slice="sliceNo"
          :algorithm="algorithm"
        />
        <div class="name">{{ algorithm }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import manifestParser from '../mixins/manifestParser'
import OldScanCanvas from '../components/OldScanCanvas'
export default {
  name: 'ResearcherView',
  components: { OldScanCanvas },
  mixins: [manifestParser],
  data() {
    return {
      manifest: File,
      multiFileDict: {},
      scan_files: [],
      result: {},
      cases: {},
      algorithms: ['ground_truth'],
      distance_threshold: 1,
      caseNo: 0,
      sliceNo: 10,
    }
  },

  created() {
    const fileName = this.$route.query.name
    const selectedFolder = this.$route.params.selected_folders[fileName]
    console.log('Selected Folders', selectedFolder)
    this.manifest = selectedFolder.manifest
    this.scan_files = selectedFolder.images
  },
  mounted() {
    this.getManifestText().then((manifestText) => {
      this.multiFileDict = this.parseManifest(manifestText, this.scan_files)
      this.result = { ...manifestText }
      this.cases = manifestText.cases

      for (const algorithm of this.multiFileDict.metadata.clusters) {
        this.algorithms.push(algorithm.name)
      }
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
<style scoped>
div.container {
  display: grid;
}
</style>
