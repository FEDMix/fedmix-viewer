<template>
  <div>
    <CaseChart :cases="cases" />
    <SliceChart :cases="cases" />
  </div>
</template>

<script>
export default {
  name: 'Algorithm',
  async asyncData({ $axios }) {
    // API - '/datasets/{id}'
    const cases = await $axios.$get('/mocked-data/cases.json')
    return { cases }
  },
}
</script>

<style scoped></style>
