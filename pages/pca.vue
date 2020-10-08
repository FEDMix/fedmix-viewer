<template>
  <div>
    <input
      id="fileInput"
      ref="fileInput"
      type="file"
      name="file"
      accept="image/*"
      @change="onChangeFiles"
    />
    <canvas id="target"></canvas>
  </div>
</template>

<script>
import manifestParser from '../mixins/manifestParser'

export default {
  name: 'PCA',
  mixins: [manifestParser],
  created() {
    // const fileName = this.$route.query.name
    // const selectedFolder = this.$route.params.selected_folders[fileName]
    // this.manifest = selectedFolder.manifest
    // this.scan_files = selectedFolder.images
  },
  mounted() {
    // this.getManifestText().then((manifestText) => {
    //   this.manifest = this.parseManifest(manifestText, this.scan_files)
    // })
  },
  methods: {
    async getManifestText() {
      const text = await this.manifest.text()
      return JSON.parse(text)
    },
    create_1d_image(image) {
      const cv = this.$cv
      const matImage = cv.imread(image)

      cv.cvtColor(matImage, matImage, cv.COLOR_RGBA2GRAY, 0)

      return matImage
    },
    onChangeFiles(event) {
      const cv = this.$cv
      const input = this.$refs.fileInput
      if (input.files.length > 0) {
        const image = new Image()
        image.src = URL.createObjectURL(input.files[0])
        image.onload = () => {
          cv.imshow('target', this.create_1d_image(image))
        }
      }
    },
  },
}
</script>
