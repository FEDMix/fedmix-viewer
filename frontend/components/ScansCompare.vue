<template>
  <canvas :id="canvasId" :ref="canvasId"></canvas>
</template>
<script>
export default {
  name: 'ScansCompare',
  props: {
    distanceThreshold: {
      type: Number,
      default: 1,
    },
    cases: {
      type: Array,
      default: () => undefined,
    },
    caseNo: {
      type: String,
      default: '0',
    },
    sliceNo: {
      type: String,
      default: '0',
    },
    selectedAlgorithms: {
      type: Array,
      default: [],
    },
  },
  computed: {
    canvasId() {
      return 'comparisonView-' + this.caseNo + '-' + this.sliceNo
    },
  },
  watch: {
    selectedAlgorithms() {
      this.loadData()
    },
    caseNo() {
      this.loadData()
    },
    sliceNo() {
      this.loadData()
    },
  },
  mounted() {
    this.loadData()
  },
  methods: {
    loadData() {
      if (this.cases === undefined || this.selectedAlgorithms === []) {
        return
      }

      const backgroundImageFile = this.getFile('scans', '')
      const maskImageFiles = this.selectedAlgorithms.map((algorithmName) =>
        this.getFile('predictedMasks', algorithmName)
      )
      this.multiSample(backgroundImageFile, maskImageFiles)
    },

    getFile(type, algorithmName) {
      const the_case = this.cases.find((cs) => cs.id === this.caseNo)
      if (type === 'predictedMasks') {
        if (algorithmName !== 'ground_truth') {
          const algorithm = the_case['algorithms'].find(
            (algorithm) => algorithm.name === algorithmName
          )
          return algorithm[type][this.sliceNo]
        }
        return
      } else {
        return the_case[type][this.sliceNo]
      }
    },

    multiSample(backgroundImageFile, maskImageFiles) {
      const imageLoadPromises = [
        this.loadImage(backgroundImageFile),
        ...maskImageFiles.map(this.loadImage),
      ]

      Promise.all(imageLoadPromises).then((results) => {
        const backgroundImage = results[0]
        const scanImages = results.slice(1)
        this.drawScans(backgroundImage, scanImages)
      })
    },

    drawScans(backgroundImage, scans) {
      const cv = this.$cv

      const colors = [
        [31, 120, 180, 255],
        [51, 160, 44, 255],
        [227, 26, 28, 255],
        [255, 127, 0, 255],
        [106, 61, 154, 255],
        [177, 89, 40, 255],
        [166, 206, 227, 255],
        [178, 223, 138, 255],
        [251, 154, 153, 255],
        [253, 191, 111, 255],
        [202, 178, 214, 255],
        [255, 255, 153, 255],
      ]

      const targetImage = new cv.imread(backgroundImage)
      const { cols, rows } = targetImage

      scans.map((scan, index) => {
        const contour_src = new cv.imread(scan)
        // Convert to binary
        cv.cvtColor(contour_src, contour_src, cv.COLOR_RGBA2GRAY, 0)
        cv.threshold(contour_src, contour_src, 120, 200, cv.THRESH_BINARY)

        // Find contours
        let contours = new cv.MatVector()
        let hierarchy = new cv.Mat()
        cv.findContours(contour_src, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

        // Draw contours on destination image
        let color = new cv.Scalar(
          colors[index][0],
          colors[index][1],
          colors[index][2],
          colors[index][3]
        )
        cv.drawContours(targetImage, contours, -1, color, 1, cv.LINE_8, hierarchy, 32)

        // Cleanup
        contour_src.delete()
        contours.delete()
        hierarchy.delete()
      })
      let dsize = new cv.Size(cols * 4, rows * 4)
      cv.resize(targetImage, targetImage, dsize, 4.0, 4.0, cv.INTER_AREA)
      cv.imshow(this.canvasId, targetImage)
      targetImage.delete()
    },

    /**
     * Load image as a promise
     */
    loadImage(file) {
      return new Promise((resolve) => {
        const image = new Image()
        image.onload = () => {
          resolve(image)
        }
        image.src = file
      })
    },
  },
}
</script>
