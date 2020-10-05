<template>
  <div></div>
</template>

<script>
export default {
  name: 'PCA',
  computed: {},
  mounted() {
    console.log('hiaa')
    console.log(this.$cv)
    const cv = this.$cv
    const M = cv.Mat.ones(5, 5, cv.CV_8U)
    console.log(M)
  },
}
</script>
