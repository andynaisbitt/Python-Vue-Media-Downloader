<template>
  <div class="space-y-4">
    <!-- Header with Controls -->
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-medium text-white">Downloads</h3>
      <div class="flex items-center gap-4">
        <!-- Filter -->
        <select 
          v-model="filter"
          class="px-3 py-1.5 bg-gray-800/50 border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
        >
          <option value="all">All</option>
          <option value="completed">Completed</option>
          <option value="downloading">Downloading</option>
          <option value="failed">Failed</option>
        </select>

        <!-- Sort -->
        <select 
          v-model="sortBy"
          class="px-3 py-1.5 bg-gray-800/50 border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
        >
          <option value="date">Date</option>
          <option value="name">Name</option>
          <option value="size">Size</option>
        </select>

        <!-- Clear All Button -->
        <button 
          v-if="filteredDownloads.length > 0"
          @click="handleClearAll"
          class="inline-flex items-center px-3 py-1.5 text-sm text-gray-400 hover:text-gray-300 transition"
        >
          <Trash2 class="w-4 h-4 mr-1" />
          Clear All
        </button>
      </div>
    </div>

    <!-- Downloads List -->
    <div class="space-y-4">
      <TransitionGroup 
        name="list"
        tag="div"
        class="space-y-4"
      >
        <template v-if="filteredDownloads.length > 0">
          <DownloadItem
            v-for="download in filteredDownloads"
            :key="download.id"
            :download="download"
            @download="handleDownload"
            @retry="handleRetry"
            @cancel="handleCancel"
            @delete="handleDelete"
            @download-subtitles="handleSubtitlesDownload"
            @download-transcript="handleTranscriptDownload"
          />
        </template>
        <div 
          v-else 
          class="text-center py-8 text-gray-400"
        >
          <Inbox class="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No downloads {{ filter !== 'all' ? `(${filter})` : '' }}</p>
        </div>
      </TransitionGroup>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-4">
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="p-1 text-gray-400 hover:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronLeft class="w-5 h-5" />
      </button>
      
      <span class="text-sm text-gray-400">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      
      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        class="p-1 text-gray-400 hover:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronRight class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue' // ADDED 'watch' import
import { Trash2, Inbox, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import DownloadItem from './DownloadItem.vue'

const props = defineProps({
  downloads: {
    type: Array,
    required: true,
    default: () => []
  },
  itemsPerPage: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits([
  'download',
  'retry',
  'cancel',
  'delete',
  'clear-all',
  'download-subtitles',
  'download-transcript'
])

// State
const filter = ref('all')
const sortBy = ref('date')
const currentPage = ref(1)

// Computed Properties
const filteredDownloads = computed(() => {
  let result = [...props.downloads]

  // Apply filter
  if (filter.value !== 'all') {
    result = result.filter(download => download.status === filter.value)
  }

  // Apply sorting
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        const titleA = a.title || a.filename || 'Unknown'
        const titleB = b.title || b.filename || 'Unknown'
        return titleA.localeCompare(titleB)
      case 'size':
        return (b.size || 0) - (a.size || 0)
      case 'date':
      default:
        return new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
    }
  })

  // Apply pagination
  const startIndex = (currentPage.value - 1) * props.itemsPerPage
  const endIndex = startIndex + props.itemsPerPage
  return result.slice(startIndex, endIndex)
})

const totalPages = computed(() => {
  const filtered = props.downloads.filter(download => {
    if (filter.value === 'all') return true
    return download.status === filter.value
  })
  return Math.ceil(filtered.length / props.itemsPerPage)
})

// Watch for filter changes to reset pagination
watch(filter, () => {
  currentPage.value = 1
}, { immediate: false })

// Event Handlers
function handleDownload(download) {
  emit('download', download)
}

function handleRetry(download) {
  emit('retry', download)
}

function handleCancel(download) {
  emit('cancel', download)
}

function handleDelete(download) {
  emit('delete', download)
}

function handleClearAll() {
  emit('clear-all')
}

function handleSubtitlesDownload(download) {
  emit('download-subtitles', download)
}

function handleTranscriptDownload(download) {
  emit('download-transcript', download)
}
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-move {
  transition: transform 0.3s ease;
}
</style>