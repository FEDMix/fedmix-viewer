<template>
  <v-container>
    <v-alert text type="info">Drag your dataset files into '/../..'</v-alert>
    <datasets :datasets="datasets" />
  </v-container>
</template>

<script>
import Datasets from '@/pages/Datasets'

export default {
  name: 'Home',
  components: { Datasets },
  data: () => ({
    selected: [2],
    datasets: [
      {
        action: '15 min',
        headline: 'Brunch this weekend?',
        subtitle:
          "I'll be in your neighborhood doing errands this weekend. Do you want to hang out?",
        title: 'Ali Connors',
      },
      {
        action: '2 hr',
        headline: 'Summer BBQ',
        subtitle: "Wish I could come, but I'm out of town this weekend.",
        title: 'me, Scrott, Jennifer',
      },
      {
        action: '6 hr',
        headline: 'Oui oui',
        subtitle: 'Do you have Paris recommendations? Have you ever been?',
        title: 'Sandra Adams',
      },
      {
        action: '12 hr',
        headline: 'Birthday gift',
        subtitle: 'Have any ideas about what we should get Heidi for her birthday?',
        title: 'Trevor Hansen',
      },
      {
        action: '18hr',
        headline: 'Recipe to try',
        subtitle: 'We should eat this: Grate, Squash, Corn, and tomatillo Tacos.',
        title: 'Britta Holt',
      },
    ],
  }),
}
</script>
