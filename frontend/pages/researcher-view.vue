<template>
  <v-container>
    <v-card>
      <v-toolbar color="cyan" dark flat>
        <v-toolbar-title>Researcher view</v-toolbar-title>

        <template v-slot:extension>
          <v-tabs v-model="tab" align-with-title>
            <v-tabs-slider color="yellow"></v-tabs-slider>

            <v-tab
              v-for="(item, i) in items"
              :key="i"
              :disabled="item.disabled"
              :to="item.to"
              nuxt
              class="d-flex flex-column"
              @click="tabclick(item)"
            >
              <div>
                {{ item.type }}
              </div>
              <div>
                {{ item.name }}
              </div>
            </v-tab>
          </v-tabs>
        </template>
      </v-toolbar>

      <v-tabs-items v-model="tab">
        <nuxt-child />
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'ResearcherView',

  data() {
    return {
      tab: null,
      items: [
        {
          name: 'View',
          type: 'Algorithm output',
          loading: false,
          disabled: false,
          to: '/researcher-view/algorithm',
        },
        {
          name: 'PCA',
          type: 'Data Clustering',
          loading: false,
          disabled: false,
          to: '/researcher-view/pca',
        },
        {
          name: 'SiameseNN',
          type: 'Data Clustering',
          loading: false,
          disabled: false,
          to: '/researcher-view/siamesenn',
        },
      ],
    }
  },
  methods: {
    tabclick(item) {
      console.log('🎹 Tab clicked', item)
    },
  },
}
</script>
