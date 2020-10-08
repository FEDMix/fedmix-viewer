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
export default {
  name: 'PCA',
  computed: {},
  mounted() {},
  methods: {
    onChangeFiles(event) {
      const cv = this.$cv

      const input = this.$refs.fileInput
      if (input.files.length > 0) {
        const image = new Image()
        image.src = URL.createObjectURL(input.files[0])

        image.onload = function () {
          const matImage = cv.imread(image)
          cv.imshow('target', matImage)
        }
      }
    },
  },
}
</script>
