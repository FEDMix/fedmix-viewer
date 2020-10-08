<template>
  <div></div>
</template>

<script>
import manifestParser from '../mixins/manifestParser'

export default {
  name: 'PCA',
  mixins: [manifestParser],
  created() {
    const fileName = this.$route.query.name
    const selectedFolder = this.$route.params.selected_folders[fileName]
    this.manifest = selectedFolder.manifest
    this.scan_files = selectedFolder.images
  },
  computed: {},
  mounted() {
    this.getManifestText().then((manifestText) => {
      this.result = manifestText
      this.scan_files.map((file) => {
        this.result = this.filterScans(this.result, file)
        console.log(this.result)
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
