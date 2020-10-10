<template>
  <div class="wrapper">
    <v-row>
      <v-btn @click="open">Open directory</v-btn>
      <v-btn v-if="Object.keys(tree).length !== 0" icon @click="cleanDB">
        <v-icon>{{ mdiClose }}</v-icon>
      </v-btn>
    </v-row>
    <div
      v-for="(item, key) in tree"
      :key="key"
      class="item"
      @click="fileClicked(item)"
    >
      {{ key }}
      <v-icon color="blue lighten-3">
        {{ item.handle.kind === 'file' ? mdiFileDocumentOutline : mdiFolder }}
      </v-icon>
      {{ item.name }}
    </div>
  </div>
</template>

<script>
import { mdiFileDocumentOutline, mdiFolder, mdiClose } from '@mdi/js'
import { openDB, deleteDB } from 'idb'

export default {
  name: 'OpenFiles',

  data() {
    return {
      db: null,
      arrayTree: [],
      tree: {},
      directoryHandle: null,
      mdiFolder,
      mdiFileDocumentOutline,
      mdiClose,
    }
  },
  async mounted() {
    // Create DB in indexDB
    this.db = await openDB('db', 1, {
      upgrade(db) {
        db.createObjectStore('store')
      },
    })
    const directoryHandle = await this.db.get('store', 'directory')
    console.log('🔌 directoryHandle', directoryHandle)

    /* Timeout to avoid user activation error. */
    setTimeout(async () => {
      if (directoryHandle) {
        await directoryHandle.requestPermission()
        await this.recursive(directoryHandle)
        console.log('🌲 tree:', this.tree)
      }
    }, 100)
  },
  // destroyed() {
  // close indexDb
  // this.db.close()
  // },

  methods: {
    async cleanDB() {
      // this.db.close()
      this.tree = {}
      await deleteDB('db')
    },

    async fileClicked(fileHandle) {
      try {
        if (fileHandle.handle.kind === 'file') {
          const file = await fileHandle.handle.getFile()
          console.log('🎹', file)
          let content = await file.text()
          if (file.type === 'application/json') {
            content = JSON.parse(content)
          }
          console.log('🎹', content)
          // console.log('🎹 file', file)
        }
      } catch (e) {}
    },

    async open() {
      try {
        this.tree = {}
        const directoryHandle = await window.showDirectoryPicker()
        this.db.put('store', directoryHandle, 'directory')
        await this.recursive(directoryHandle)
      } catch (e) {
        console.error(e)
      }
    },

    /**
     * Read recursively all files and subdirectories
     */
    async recursive(directoryHandle, path = '/') {
      try {
        for await (const [name, handle] of directoryHandle) {
          if (handle.kind === 'directory') {
            // if item is a directory enter to the folder
            await this.recursive(handle, path + name + '/')
          }
          // Make vue reactive when changing the object ==> this.tree[path + name] = { name, handle }
          this.$set(this.tree, path + name, { name, handle })
        }
      } catch (error) {
        console.error(error)
      }
    },
  },
}
</script>
<style scoped>
.wrapper {
  cursor: pointer;
}
.item {
  padding: 4px;
}
.item:hover {
  background-color: #eee;
}
</style>
