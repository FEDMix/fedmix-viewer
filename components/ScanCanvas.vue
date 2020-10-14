<template>
  <div>
    <canvas :id="canvasId" :ref="canvasId" class="scan"></canvas>
  </div>
</template>
<script>
export default {
  name: 'ScanCanvas',
  components: {},
  props: {
    distance_threshold: {
      type: Number,
      default: 1,
    },
    multiFileDict: {
      type: Object,
      default: () => undefined,
    },
    case: {
      type: Number,
      default: 0,
    },
    slice: {
      type: Number,
      default: 0,
    },
    algorithm: {
      type: String,
      default: '',
    },
  },
  mounted() {
    this.loadData()
  },
  watch: {
    multiFileDict() {
      this.loadData()
    },
  },
  computed: {
    canvasId() {
      return 'scan-' + (this.algorithm !== '' ? this.algorithm : 'ground-truth')
    },
  },
  methods: {
    loadData() {
      if (
        this.multiFileDict === undefined ||
        this.multiFileDict.metadata === undefined
      ) {
        return
      }

      const backgroundFile = this.getFile(
        this.multiFileDict,
        this.multiFileDict.metadata.subdir,
        'scans',
        this.case,
        this.slice
      )
      const groundTruthFile = this.getFile(
        this.multiFileDict,
        this.multiFileDict.metadata.subdir,
        'ground_truth',
        this.case,
        this.slice
      )
      const predictedMaskFile =
        this.algorithm !== ''
          ? this.getFile(
              this.multiFileDict,
              this.multiFileDict.metadata.subdir,
              'predicted_masks',
              this.case,
              this.slice,
              this.algorithm
            )
          : undefined
      if (!predictedMaskFile) {
        this.processImages(backgroundFile, groundTruthFile)
      } else {
        this.processImages(backgroundFile, predictedMaskFile, groundTruthFile)
      }
    },

    getFile(multiFileDict, subDir, type, caseNo, sliceNo, algorithm) {
      if (algorithm === undefined) {
        if (
          multiFileDict[subDir][type][caseNo] !== undefined &&
          multiFileDict[subDir][type][caseNo][sliceNo] !== undefined
        ) {
          return multiFileDict[subDir][type][caseNo][sliceNo].file
        }
      } else {
        if (
          multiFileDict[subDir][type][algorithm] !== undefined &&
          multiFileDict[subDir][type][algorithm][caseNo] !== undefined &&
          multiFileDict[subDir][type][algorithm][caseNo][sliceNo] !== undefined
        ) {
          return multiFileDict[subDir][type][algorithm][caseNo][sliceNo].file
        }
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

        console.log(that.canvasId)
        cv.imshow(that.canvasId, ct_scan)

        // Convert to binary
        cv.cvtColor(contour_src, contour_src, cv.COLOR_RGBA2GRAY, 0)
        cv.threshold(contour_src, contour_src, 120, 200, cv.THRESH_BINARY)

        // Find contours
        let contours = new cv.MatVector()
        let hierarchy = new cv.Mat()
        cv.findContours(
          contour_src,
          contours,
          hierarchy,
          cv.RETR_CCOMP,
          cv.CHAIN_APPROX_SIMPLE
        )

        // Draw contours on destination image
        const matContour = cv.Mat.zeros(
          contour_src.cols,
          contour_src.rows,
          cv.CV_8UC1
        )
        let color = new cv.Scalar(255)
        cv.drawContours(
          matContour,
          contours,
          -1,
          color,
          1,
          cv.LINE_8,
          hierarchy,
          32
        )

        if (groundTruthFile) {
          // Ring overlap
          let matMask = that.getGroundTruthMask(imgGroundTruth)
          let green = new cv.Mat(
            matMask.cols,
            matMask.rows,
            cv.CV_8UC4,
            new cv.Scalar(0, 255, 0, 255)
          )
          let greenMask = cv.Mat.zeros(cols, rows, cv.CV_8UC1)
          cv.bitwise_and(matMask, matContour, greenMask)
          green.copyTo(ct_scan, greenMask)

          // Not ring overlap
          let matInvMask = new cv.Mat()
          cv.bitwise_not(matMask, matInvMask)
          let red = new cv.Mat(
            matMask.cols,
            matMask.rows,
            cv.CV_8UC4,
            new cv.Scalar(255, 0, 0, 255)
          )
          let redMask = cv.Mat.zeros(cols, rows, cv.CV_8UC1)
          cv.bitwise_and(matInvMask, matContour, redMask)
          red.copyTo(ct_scan, redMask)

          // Show result and clean up
          cv.imshow(that.canvasId, ct_scan)
        } else {
          // Draw contours on destination image
          for (let i = 0; i < contours.size(); ++i) {
            let color = new cv.Scalar(0, 255, 0, 255)
            cv.drawContours(
              ct_scan,
              contours,
              i,
              color,
              1,
              cv.LINE_8,
              hierarchy,
              160
            )
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
        image.src = URL.createObjectURL(file)
      })
    },

    getGroundTruthMask(imgGroundTruth) {
      const cv = this.$cv

      const matGroundTruth = new cv.imread(imgGroundTruth)

      // Convert to binary
      cv.cvtColor(matGroundTruth, matGroundTruth, cv.COLOR_RGBA2GRAY, 0)
      cv.threshold(matGroundTruth, matGroundTruth, 120, 200, cv.THRESH_BINARY)

      // Find contours
      let contours = new cv.MatVector()
      let hierarchy = new cv.Mat()
      cv.findContours(
        matGroundTruth,
        contours,
        hierarchy,
        cv.RETR_CCOMP,
        cv.CHAIN_APPROX_SIMPLE
      )

      // Draw contours on destination image
      let matContours = cv.Mat.ones(
        matGroundTruth.cols,
        matGroundTruth.rows,
        cv.CV_8U
      )
      let color2 = new cv.Scalar(0)
      cv.drawContours(
        matContours,
        contours,
        -1,
        color2,
        1,
        cv.LINE_8,
        hierarchy,
        160
      )

      // Calculate distance transform
      let matDist = new cv.Mat()
      cv.distanceTransform(matContours, matDist, cv.DIST_L2, 3)

      // Threshold (range 0 .. 1)
      let matThreshold = new cv.Mat()
      cv.threshold(
        matDist,
        matThreshold,
        this.distance_threshold,
        1,
        cv.THRESH_BINARY_INV
      )

      // Convert to 8U, range 0 .. 255
      let matConvert = new cv.Mat()
      matThreshold.convertTo(matConvert, cv.CV_8U, 255, 0)

      return matConvert
    },
  },
}
</script>
