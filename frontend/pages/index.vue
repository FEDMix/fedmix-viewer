<template>
  <v-container>
    <v-alert text type="info">Drag your dataset files into '/../..'</v-alert>
    <datasets :datasets="datasets" />
  </v-container>
</template>

<script>
import Datasets from '~/pages/Datasets'
import datasets_query from '~/apollo/datasets'

export default {
  name: 'Home',
  components: { Datasets },
  apollo: {
    datasets: {
      query: datasets_query,
    },
  },

  data: () => ({
    selected: [2],
  }),
}
</script>
