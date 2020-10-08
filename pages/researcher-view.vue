<template>
  <div></div>
</template>

<script>
export default {
  name: 'ResearcherView',
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
      this.result = { ...manifestText }
      this.scan_files.map((file) => {
        this.filterScans(file)
      })
    })
  },
  methods: {
    async getManifestText() {
      const text = await this.manifest.text()
      return JSON.parse(text)
    },
    filterScans(file) {
      if (
        file.webkitRelativePath.match(/(.*)\/(.*)\/scans\/(.*)\/(.*)\.png/i)
      ) {
        const scan = file.webkitRelativePath.match(
          /(.*)\/(.*)\/scans\/(.*)\/(.*)\.png/i
        )
        this.parseScans(file, scan, 'scans')
      }
      if (
        file.webkitRelativePath.match(
          /(.*)\/(.*)\/predicted_masks\/(.*)\/(.*)\.png/i
        )
      ) {
        const predictions = file.webkitRelativePath.match(
          /(.*)\/(.*)\/predicted_masks\/(.*)\/(.*)\/(.*)\.png/i
        )
        this.parseScans(file, predictions, 'predicted_masks')
      }
      if (
        file.webkitRelativePath.match(
          /(.*)\/(.*)\/ground_truth_masks\/(.*)\/(.*)\.png/i
        )
      ) {
        const groundtruth = file.webkitRelativePath.match(
          /(.*)\/(.*)\/ground_truth_masks\/(.*)\/(.*)\.png/i
        )
        this.parseScans(file, groundtruth, 'ground_truth')
      }
    },
    parseScans(file, filePath, type) {
      if (filePath && type === 'predicted_masks') {
        const subdir = filePath[1]
        const other_dirs = filePath[2]
        const algorithm = filePath[3]
        const caseNr = parseInt(filePath[4])
        const slice = parseInt(filePath[5])
        this.ensureDirs(subdir, type, caseNr, algorithm)
        this.result[subdir][type][algorithm][caseNr][slice] = {
          name: file.name,
          path: subdir + '/' + other_dirs,
          file,
        }
      } else {
        const subdir = filePath[1]
        const other_dirs = filePath[2]
        const caseNr = parseInt(filePath[3])
        const slice = parseInt(filePath[4])
        this.ensureDirs(subdir, type, caseNr)
        this.result[subdir][type][caseNr][slice] = {
          name: file.name,
          path: subdir + '/' + other_dirs,
          file,
        }
      }
      console.log('result', this.result)
    },

    ensureDirs(subdir, type, caseNr, algorithm) {
      this.result.metadata.subdir = subdir
      if (this.result[subdir] === undefined) {
        this.result[subdir] = {}
      }
      if (this.result[subdir][type] === undefined) {
        this.result[subdir][type] = {}
      }
      if (algorithm === undefined) {
        if (this.result[subdir][type][caseNr] === undefined) {
          this.result[subdir][type][caseNr] = {}
        }
      } else {
        if (this.result[subdir][type][algorithm] === undefined) {
          this.result[subdir][type][algorithm] = {}
        }
        if (this.result[subdir][type][algorithm][caseNr] === undefined) {
          this.result[subdir][type][algorithm][caseNr] = {}
        }
      }
    },
  },
}
</script>
