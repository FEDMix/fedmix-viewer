<template>
  <v-container>
    <CaseChart :cases="cases" />
    <SliceChart :cases="cases" />
  </v-container>
</template>

<script>
import CaseChart from '../components/CaseChart'
import SliceChart from '../components/SliceChart'
export default {
  name: 'ResearcherView',
  components: { CaseChart, SliceChart },
  async asyncData({ $axios }) {
    // API - '/datasets/{id}'
    const cases = await $axios.$get('/mocked-data/cases.json')
    return { cases }
  },
  data() {
    return {
      // manifest: File,
      // scan_files: [],
      // result: {},
    }
  },

  // created() {
  //   const fileName = this.$route.query.name
  //   const selectedFolder = this.$route.params.selected_folders[fileName]
  //   this.manifest = selectedFolder.manifest
  //   this.scan_files = selectedFolder.images
  // },
  //
  // mounted() {
  //   try {
  //     this.getManifestText().then((manifestText) => {
  //       this.manifest = this.parseManifest(manifestText, this.scan_files)
  //       this.result = { ...manifestText }
  //       this.cases = manifestText?.cases
  //       this.scan_files.map((file) => {
  //         this.filterScans(file)
  //       })
  //     })
  //   } catch (e) {
  //     console.log('🎹', e)
  //   }
  // },
  //
  // methods: {
  //   async getManifestText() {
  //     const text = await this.manifest.text()
  //     return JSON.parse(text)
  //   },
  // },
}
</script>
