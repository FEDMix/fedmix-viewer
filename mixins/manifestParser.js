const manifestParser = {
  methods: {
    parseManifest(manifestText, scan_files) {
      let manifest = manifestText
      scan_files.map((file) => {
        manifest = this.filterScans(manifest, file)
      })
      return manifest
    },
    filterScans(manifest, file) {
      if (
        file.webkitRelativePath.match(/(.*)\/(.*)\/scans\/(.*)\/(.*)\.png/i)
      ) {
        const scan = file.webkitRelativePath.match(
          /(.*)\/(.*)\/scans\/(.*)\/(.*)\.png/i
        )
        return this.parseScans(manifest, file, scan, 'scans')
      }
      if (
        file.webkitRelativePath.match(
          /(.*)\/(.*)\/predicted_masks\/(.*)\/(.*)\.png/i
        )
      ) {
        const predictions = file.webkitRelativePath.match(
          /(.*)\/(.*)\/predicted_masks\/(.*)\/(.*)\/(.*)\.png/i
        )
        return this.parseScans(manifest, file, predictions, 'predicted_masks')
      }
      if (
        file.webkitRelativePath.match(
          /(.*)\/(.*)\/ground_truth_masks\/(.*)\/(.*)\.png/i
        )
      ) {
        const groundtruth = file.webkitRelativePath.match(
          /(.*)\/(.*)\/ground_truth_masks\/(.*)\/(.*)\.png/i
        )
        return this.parseScans(manifest, file, groundtruth, 'ground_truth')
      }
    },
    parseScans(manifest, file, filePath, type) {
      let result = { ...manifest }
      if (filePath && type === 'predicted_masks') {
        const subdir = filePath[1]
        const other_dirs = filePath[2]
        const algorithm = filePath[3]
        const caseNr = parseInt(filePath[4])
        const slice = parseInt(filePath[5])
        result = this.ensureDirs(result, subdir, type, caseNr, algorithm)
        result[subdir][type][algorithm][caseNr][slice] = {
          name: file.name,
          path: subdir + '/' + other_dirs,
          file,
        }
      } else {
        const subdir = filePath[1]
        const other_dirs = filePath[2]
        const caseNr = parseInt(filePath[3])
        const slice = parseInt(filePath[4])
        result = this.ensureDirs(result, subdir, type, caseNr)
        result[subdir][type][caseNr][slice] = {
          name: file.name,
          path: subdir + '/' + other_dirs,
          file,
        }
      }
      return result
    },
    ensureDirs(result, subdir, type, caseNr, algorithm) {
      result.metadata.subdir = subdir
      if (result[subdir] === undefined) {
        result[subdir] = {}
      }
      if (result[subdir][type] === undefined) {
        result[subdir][type] = {}
      }
      if (algorithm === undefined) {
        if (result[subdir][type][caseNr] === undefined) {
          result[subdir][type][caseNr] = {}
        }
      } else {
        if (result[subdir][type][algorithm] === undefined) {
          result[subdir][type][algorithm] = {}
        }
        if (result[subdir][type][algorithm][caseNr] === undefined) {
          result[subdir][type][algorithm][caseNr] = {}
        }
      }
      return result
    },
  },
}

export default manifestParser
