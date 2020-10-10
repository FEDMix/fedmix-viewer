<template>
  <v-container>
    <open-files />
    <v-row>
      <v-col cols="12">
        <v-card outlined>
          <v-card-title class="headline">Add Folders</v-card-title>
          <v-container>
            <v-row justify="center">
              <v-col cols="10">
                <v-file-input
                  id="filedir"
                  v-model="folders"
                  label="Folders"
                  counter
                  color="primary"
                  placeholder="Select your folders"
                  outlined
                  multiple
                  webkitdirectory
                />
              </v-col>
              <v-col cols="2">
                <v-btn color="primary" fab dark @click="addFolder()">
                  <v-icon dark x-large>{{ mdiPlus }}</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card id="folder-list" outlined>
          <v-card-title class="headline">Folders</v-card-title>
          <v-container v-if="selected_folders">
            <v-row
              v-for="(images, name) in selected_folders"
              :key="name"
              class="folders"
            >
              <v-col md="3" sm="4">
                {{ name }}
              </v-col>
              <v-col md="8" sm="6">
                <p>
                  Number of images: {{ selected_folders[name].images.length }}
                </p>
                <nuxt-link
                  :to="{
                    name: 'researcher-view',
                    query: { name },
                    params: { selected_folders },
                  }"
                >
                  <v-btn color="primary"> Analyze </v-btn>
                </nuxt-link>
                <nuxt-link
                  :to="{
                    name: 'pca',
                    query: { name },
                    params: { selected_folders },
                  }"
                >
                  <v-btn color="primary"> PCA </v-btn>
                </nuxt-link>
              </v-col>
              <v-col md="1" sm="2">
                <v-btn
                  color="error"
                  fab
                  dark
                  x-small
                  @click="removeFolder(name)"
                >
                  <v-icon dark small>{{ mdiDelete }}</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mdiPlus, mdiDelete } from '@mdi/js'

export default {
  name: 'Home',
  data() {
    return {
      mdiPlus,
      mdiDelete,
      selected_folders: {},
      folders: [],
    }
  },
  // mounted() {
  //   if (localStorage.selected_folders) {
  //     this.selected_folders = localStorage.getItem('selected_folders')
  //   }
  // },
  methods: {
    addFolder() {
      const manifests = this.folders.filter((value, index, array) => {
        return (
          value.name.startsWith('manifest') &&
          value.type.startsWith('application/json')
        )
      })
      for (const manifest of manifests) {
        const re = /(.*)\//
        const folder_regexresult = re.exec(manifest.webkitRelativePath)
        if (folder_regexresult[0].endsWith('/')) {
          const folder_name = folder_regexresult[1]
          const images = this.folders.filter((value, index, array) => {
            return (
              value.webkitRelativePath.startsWith(folder_name) &&
              value.type.startsWith('image')
            )
          })
          if (!(folder_name in this.selected_folders)) {
            this.selected_folders[folder_name] = {
              name: folder_name,
              manifest,
              images,
            }
          }
        } else {
          // TODO: NEEDS SOME ERROR POPUP
          console.log('No manifest file in uploaded folder')
        }
      }
      this.folders = []
      // localStorage.selected_folders = JSON.stringify(this.selected_folders)
      // localStorage.setItem(
      //   'selected_folders',
      //   JSON.stringify(this.selected_folders)
      // )
      // console.log('Selected', localStorage.getItem('selected_folders'))

      // console.log('class', this.selected_folders)
    },
    removeFolder(name) {
      if (name in this.selected_folders) {
        this.$delete(this.selected_folders, name)
        // localStorage.selected_folders = JSON.stringify(this.selected_folders)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
#folder-list {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: block;
}
</style>
