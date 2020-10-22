<template>
  <div class="d-flex flex-column align-center">
    <span class="text-center">{{ algorithm }}</span>
    <canvas :id="canvasId" :ref="canvasId" class="scan"></canvas>
  </div>
</template>
<script>
export default {
  name: 'ScansGrid',
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
    algorithm: {
      type: String,
      default: '',
    },
  },
  computed: {
    canvasId() {
      return 'scan-' + (this.algorithm !== '' ? this.algorithm : 'ground-truth')
    },
  },
  watch: {
    caseNo(newValue) {
      this.loadData()
    },
    sliceNo() {
      this.loadData()
    },
    distanceThreshold() {
      this.loadData()
    },
  },
  mounted() {
    this.loadData()
  },
  methods: {
    loadData() {
      if (this.cases === undefined || this.cases.metadata === undefined) {
        return
      }
      const backgroundFile = this.getFile('scans')
      const groundTruthFile = this.getFile('ground_truth_masks')
      const predictedFile = this.getFile('predicted_masks')
      if (!predictedFile) {
        this.processImages(backgroundFile, groundTruthFile)
      } else {
        this.processImages(backgroundFile, predictedFile, groundTruthFile)
      }
    },

    getFile(type) {
      if (type === 'predicted_masks') {
        if (this.algorithm !== 'ground_truth') {
          return (
            '/mocked-data/data_artificial/' +
            this.cases.cases[this.caseNo]['algorithms'][this.algorithm][type][this.sliceNo]
          )
        }
        return
      } else {
        return '/mocked-data/data_artificial/' + this.cases.cases[this.caseNo][type][this.sliceNo]
      }
    },

    processImages(backgroundFile, predictedMaskFile, groundTruthFile) {
      const cv = this.$cv
      const that = this
      const imageLoadPromises = [
        this.loadImage(backgroundFile),
        this.loadImage(predictedMaskFile),
        ...(groundTruthFile ? [this.loadImage(groundTruthFile)] : []),
      ]

      Promise.all(imageLoadPromises).then((results) => {
        const [bg_image, image, imgGroundTruth] = results

        const contour_src = new cv.imread(image)
        const ct_scan = new cv.imread(bg_image)
        const cols = ct_scan.cols
        const rows = ct_scan.rows
        cv.imshow(that.canvasId, ct_scan)

        // Convert to binary
        cv.cvtColor(contour_src, contour_src, cv.COLOR_RGBA2GRAY, 0)
        cv.threshold(contour_src, contour_src, 120, 200, cv.THRESH_BINARY)

        // Find contours
        const contours = new cv.MatVector()
        const hierarchy = new cv.Mat()
        cv.findContours(contour_src, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

        // Draw contours on destination image
        const matContour = cv.Mat.zeros(contour_src.cols, contour_src.rows, cv.CV_8UC1)
        const color = new cv.Scalar(255)
        cv.drawContours(matContour, contours, -1, color, 1, cv.LINE_8, hierarchy, 32)

        if (groundTruthFile) {
          // Ring overlap
          const matMask = that.getGroundTruthMask(imgGroundTruth)
          const green = new cv.Mat(
            matMask.cols,
            matMask.rows,
            cv.CV_8UC4,
            new cv.Scalar(0, 255, 0, 255)
          )
          const greenMask = cv.Mat.zeros(cols, rows, cv.CV_8UC1)
          cv.bitwise_and(matMask, matContour, greenMask)
          green.copyTo(ct_scan, greenMask)

          // Not ring overlap
          const matInvMask = new cv.Mat()
          cv.bitwise_not(matMask, matInvMask)
          const red = new cv.Mat(
            matMask.cols,
            matMask.rows,
            cv.CV_8UC4,
            new cv.Scalar(255, 0, 0, 255)
          )
          const redMask = cv.Mat.zeros(cols, rows, cv.CV_8UC1)
          cv.bitwise_and(matInvMask, matContour, redMask)
          red.copyTo(ct_scan, redMask)

          // Show result and clean up
          cv.imshow(that.canvasId, ct_scan)
        } else {
          // Draw contours on destination image
          for (let i = 0; i < contours.size(); ++i) {
            const color = new cv.Scalar(0, 255, 0, 255)
            cv.drawContours(ct_scan, contours, i, color, 1, cv.LINE_8, hierarchy, 160)
          }
          cv.imshow(that.canvasId, ct_scan)
        }

        contour_src.delete()
        ct_scan.delete()
        contours.delete()
        hierarchy.delete()
      })
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

    getGroundTruthMask(imgGroundTruth) {
      const cv = this.$cv

      const matGroundTruth = new cv.imread(imgGroundTruth)

      // Convert to binary
      cv.cvtColor(matGroundTruth, matGroundTruth, cv.COLOR_RGBA2GRAY, 0)
      cv.threshold(matGroundTruth, matGroundTruth, 120, 200, cv.THRESH_BINARY)

      // Find contours
      const contours = new cv.MatVector()
      const hierarchy = new cv.Mat()
      cv.findContours(matGroundTruth, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

      // Draw contours on destination image
      const matContours = cv.Mat.ones(matGroundTruth.cols, matGroundTruth.rows, cv.CV_8U)
      const color2 = new cv.Scalar(0)
      cv.drawContours(matContours, contours, -1, color2, 1, cv.LINE_8, hierarchy, 160)

      // Calculate distance transform
      const matDist = new cv.Mat()
      cv.distanceTransform(matContours, matDist, cv.DIST_L2, 3)

      // Threshold (range 0 .. 1)
      const matThreshold = new cv.Mat()
      cv.threshold(matDist, matThreshold, this.distanceThreshold, 1, cv.THRESH_BINARY_INV)

      // Convert to 8U, range 0 .. 255
      const matConvert = new cv.Mat()
      matThreshold.convertTo(matConvert, cv.CV_8U, 255, 0)

      return matConvert
    },
  },
}
</script>
<style scoped>
.scan {
  width: 240px;
  height: 240px;
}
</style>
