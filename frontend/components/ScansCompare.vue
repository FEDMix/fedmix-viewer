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
      type: Object,
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
      return 'comparisionView-' + this.caseNo + this.sliceNo
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
      const imageLoadPromises = []
      const backgroundFilePath = this.getFile()
      const backgroundScan = this.loadImage(backgroundFilePath)
      imageLoadPromises.push(backgroundScan)
      this.selectedAlgorithms.map((algorithm) => {
        const filePath = this.getFile(algorithm)
        const scan = this.loadImage(filePath)
        imageLoadPromises.push(scan)
      })

      this.multiSample(imageLoadPromises)
    },
    multiSample(inputScans) {
      const cv = this.$cv
      let targetImage = null
      let cols = 0
      let rows = 0

      Promise.all(inputScans).then((results) => {
        const [bg_image, algorithm1, algorithm2] = results
        targetImage = new cv.imread(bg_image)
        cols = targetImage.cols
        rows = targetImage.rows
        this.drawScans(cv, targetImage, [algorithm1, algorithm2], cols, rows)
      })
    },
    drawScans(cv, targetImage, scans, cols, rows) {
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
    getFile(algorithm) {
      if (algorithm) {
        return (
          '/mocked-data/data_artificial/' +
          this.cases[this.caseNo]['algorithms'][algorithm]['predicted_masks'][this.sliceNo]
        )
      }
      return '/mocked-data/data_artificial/' + this.cases[this.caseNo]['scans'][this.sliceNo]
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
