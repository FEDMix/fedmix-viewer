<template>
  <div>
    <DiceChart :cases="cases" />
    <div class="container">
      <div v-for="canvas in canvases" :key="canvas">
        <canvas :id="canvas" class="scan"></canvas>
        <div class="name">{{ canvas }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import manifestParser from '../mixins/manifestParser'
import DiceChart from '../components/DiceChart'
export default {
  name: 'ResearcherView',
  components: { DiceChart },
  mixins: [manifestParser],
  data() {
    return {
      manifest: File,
      scan_files: [],
      result: {},
      cases: {},
      canvases: ['ground_truth'],
      distance_threshold: 1,
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
      const multiFileDict = this.manifest
      this.result = { ...manifestText }
      this.cases = manifestText.cases

      this.processImages(
        this.getFile(
          multiFileDict,
          multiFileDict.metadata.subdir,
          'scans',
          0,
          0
        ),
        this.getFile(
          multiFileDict,
          multiFileDict.metadata.subdir,
          'ground_truth',
          0,
          0
        ),
        null,
        'ground_truth'
      )

      for (const algorithm of this.manifest.metadata.clusters) {
        this.canvases.push(algorithm.name)
        console.log(this.manifest)
        this.processImages(
          this.getFile(
            multiFileDict,
            multiFileDict.metadata.subdir,
            'scans',
            0,
            0
          ),
          this.getFile(
            multiFileDict,
            multiFileDict.metadata.subdir,
            'predicted_masks',
            0,
            0,
            algorithm.name
          ),
          this.getFile(
            multiFileDict,
            multiFileDict.metadata.subdir,
            'ground_truth',
            0,
            0
          ),
          algorithm.name
        )
      }
    })
  },

  methods: {
    async getManifestText() {
      const text = await this.manifest.text()
      return JSON.parse(text)
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

    processImages(background, input, groundTruth, targetId) {
      const cv = this.$cv

      const bg_image = new Image()
      bg_image.src = URL.createObjectURL(background)

      const image = new Image()
      image.src = URL.createObjectURL(input)

      const imgGroundTruth = new Image()
      if (groundTruth) {
        imgGroundTruth.src = URL.createObjectURL(groundTruth)
      }

      const that = this

      image.onload = function () {
        // Source and destination images
        const contour_src = new cv.imread(image)
        const ct_scan = new cv.imread(bg_image)
        const cols = ct_scan.cols
        const rows = ct_scan.rows

        cv.imshow(targetId, ct_scan)

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

        if (groundTruth) {
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
          cv.imshow(targetId, ct_scan)
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
          cv.imshow(targetId, ct_scan)
        }

        contour_src.delete()
        ct_scan.delete()
        contours.delete()
        hierarchy.delete()
      }
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
<style scoped>
div.container {
  display: grid;
}
</style>
