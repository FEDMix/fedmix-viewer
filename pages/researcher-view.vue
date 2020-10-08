<template>
  <div></div>
</template>

<script>
import manifestParser from '../mixins/manifestParser'
export default {
  name: 'ResearcherView',
  mixins: [manifestParser],
  data() {
    return {
      manifest: File,
      scan_files: [],
      result: {},
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
