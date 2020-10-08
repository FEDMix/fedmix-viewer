const manifestParser = {
  methods: {
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

export default manifestParser
