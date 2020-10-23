<template>
  <div>
    <h2>Data sets</h2>
    <v-card>
      <v-list two-line>
        <v-list-item-group>
          <template v-for="(item, index) in datasets">
            <v-list-item :key="item.id" :to="'/researcher-view/algorithm'">
              <v-list-item-content>
                <v-list-item-title v-text="item.title"></v-list-item-title>
                <v-list-item-subtitle class="text--primary">
                  Clusters: {{item.clusters.length}}
                </v-list-item-subtitle>
                <v-list-item-subtitle v-text="item.subtitle"></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-divider v-if="index < datasets.length - 1" :key="index"></v-divider>
          </template>
        </v-list-item-group>
      </v-list>
    </v-card>
  </div>
</template>
<script>
export default {
  name: 'Datasets',
  props: {
    datasets: {},
  },
}
</script>
