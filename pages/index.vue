<template>
  <v-container>
    <v-layout row wrap>
      <v-flex md9>
        <v-card-title>
          <h1 style="font-weight: 900; text-shadow: 3px 2px #ddd">FEDMix</h1>
        </v-card-title>
        <v-card-text>
          <p>
            Automated Medical Image Analysis (MIA) has the potential to truly innovate clinical
            practice by offering solutions to routine, yet key tasks, such as segmentation (i.e.,
            delineating organs). Especially with recent advances in machine learning (ML), in
            particular in Deep Neural Networks (DNNs) that have led to an explosive growth of
            successful MIA studies reported in academic literature, the time appears right for such
            innovations to find widespread real-world uptake.
          </p>
          <p>
            Yet, labor-intensive manual performance of these tasks is still often daily clinical
            practice. In this proposal, we integrate DNNs with other state-of-the-art computational
            intelligence techniques, in particular evolutionary algorithms (EAs), to overcome 2 key
            obstacles in moving toward widespread clinical uptake of computationally intelligent MIA
            techniques: 1) observer variation in the definition of a ground truth, and 2) image
            quality variation due to different acquisition protocols and scanners at different
            institutes.
          </p></v-card-text
        >
      </v-flex>
      <v-flex md3>
        <v-img
          class="white--text align-end"
          height="250px"
          src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
        >
        </v-img>
      </v-flex>
    </v-layout>
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
