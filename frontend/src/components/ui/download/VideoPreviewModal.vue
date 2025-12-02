<template>
  <Transition name="modal">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
      @click.self="handleClose"
    >
      <div class="relative bg-gray-900 rounded-2xl border border-gray-800 w-full max-w-4xl max-h-[90vh] overflow-hidden shadow-2xl">
        <!-- Header -->
        <div class="sticky top-0 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800 px-6 py-4 flex items-center justify-between z-10">
          <div>
            <h2 class="text-xl font-bold text-white">
              {{ metadata.is_playlist ? 'Playlist Preview' : 'Video Preview' }}
            </h2>
            <p v-if="metadata.is_playlist" class="text-sm text-gray-400 mt-1">
              {{ metadata.playlist_title }} • {{ metadata.videos.length }} video{{ metadata.videos.length > 1 ? 's' : '' }}
            </p>
          </div>
          <button
            @click="handleClose"
            class="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-gray-800 transition"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="p-12 text-center">
          <div class="inline-block">
            <svg class="animate-spin h-12 w-12 text-purple-500 mx-auto" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="mt-4 text-gray-400">Fetching video information...</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="p-12 text-center">
          <div class="inline-block">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertCircle class="w-8 h-8 text-red-400" />
            </div>
            <h3 class="text-lg font-medium text-white mb-2">Failed to load video</h3>
            <p class="text-gray-400">{{ error }}</p>
            <button
              @click="handleClose"
              class="mt-6 px-6 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition"
            >
              Close
            </button>
          </div>
        </div>

        <!-- Content -->
        <div v-else class="overflow-y-auto max-h-[calc(90vh-140px)]">
          <!-- Video List -->
          <div class="p-6 space-y-4">
            <div
              v-for="(video, index) in metadata.videos"
              :key="index"
              class="bg-gray-800/50 rounded-xl border border-gray-700/50 p-4 hover:border-purple-500/30 transition"
            >
              <div class="flex gap-4">
                <!-- Thumbnail -->
                <div class="w-48 h-27 bg-gray-900 rounded-lg overflow-hidden flex-shrink-0">
                  <img
                    v-if="video.thumbnail_url"
                    :src="video.thumbnail_url"
                    :alt="video.title"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <Video class="w-12 h-12 text-gray-600" />
                  </div>

                  <!-- Duration overlay -->
                  <div v-if="video.duration" class="relative -mt-8 mb-2 ml-2">
                    <span class="inline-block bg-black/80 text-white text-xs px-2 py-0.5 rounded">
                      {{ formatDuration(video.duration) }}
                    </span>
                  </div>
                </div>

                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <h3 class="text-white font-medium text-lg mb-2 line-clamp-2">
                    {{ video.title }}
                  </h3>
                  <div class="flex flex-wrap items-center gap-4 text-sm text-gray-400 mb-2">
                    <span class="flex items-center gap-1">
                      <User class="w-4 h-4" />
                      {{ video.uploader }}
                    </span>
                    <span v-if="video.view_count" class="flex items-center gap-1">
                      <Eye class="w-4 h-4" />
                      {{ formatViews(video.view_count) }}
                    </span>
                    <span v-if="video.upload_date" class="flex items-center gap-1">
                      <Calendar class="w-4 h-4" />
                      {{ formatDate(video.upload_date) }}
                    </span>
                  </div>
                  <p v-if="video.description" class="text-gray-500 text-sm line-clamp-2">
                    {{ video.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Actions -->
        <div v-if="!loading && !error" class="sticky bottom-0 bg-gray-900/95 backdrop-blur-sm border-t border-gray-800 px-6 py-4 flex items-center justify-between z-10">
          <div class="text-sm text-gray-400">
            Format: <span class="text-white font-medium">{{ downloadOptions.format.toUpperCase() }}</span>
            • Quality: <span class="text-white font-medium">{{ downloadOptions.quality }}</span>
          </div>
          <div class="flex gap-3">
            <button
              @click="handleClose"
              class="px-6 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition"
            >
              Cancel
            </button>
            <button
              @click="handleConfirm"
              class="px-6 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-lg transition shadow-lg"
            >
              <span class="flex items-center gap-2">
                <Download class="w-4 h-4" />
                Download {{ metadata.videos.length > 1 ? `${metadata.videos.length} Videos` : 'Video' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, Video, Download, AlertCircle, User, Eye, Calendar } from 'lucide-vue-next'
import axios from 'axios'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  urls: {
    type: Array,
    required: true
  },
  downloadOptions: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'confirm'])

const loading = ref(false)
const error = ref(null)
const metadata = ref({
  videos: [],
  is_playlist: false,
  playlist_title: null
})

// Watch for show prop changes and fetch metadata
watch(() => props.show, async (newVal) => {
  if (newVal && props.urls.length > 0) {
    await fetchAllMetadata()
  }
})

async function fetchAllMetadata() {
  loading.value = true
  error.value = null
  metadata.value = { videos: [], is_playlist: false, playlist_title: null }

  try {
    // Fetch metadata for all URLs
    const promises = props.urls.map(url =>
      axios.post('/api/metadata', { url })
    )

    const responses = await Promise.all(promises)

    // Combine all videos from all responses
    let allVideos = []
    let isAnyPlaylist = false
    let playlistTitle = null

    responses.forEach(response => {
      const data = response.data
      if (data.success && data.videos) {
        allVideos = [...allVideos, ...data.videos]
        if (data.is_playlist) {
          isAnyPlaylist = true
          if (!playlistTitle) playlistTitle = data.playlist_title
        }
      }
    })

    if (allVideos.length === 0) {
      throw new Error('No videos found')
    }

    metadata.value = {
      videos: allVideos,
      is_playlist: isAnyPlaylist || props.urls.length > 1,
      playlist_title: playlistTitle || (props.urls.length > 1 ? `${props.urls.length} Videos` : null)
    }

  } catch (err) {
    console.error('Failed to fetch metadata:', err)
    error.value = err.response?.data?.error || err.message || 'Failed to load video information'
  } finally {
    loading.value = false
  }
}

function handleClose() {
  emit('close')
}

function handleConfirm() {
  emit('confirm', metadata.value)
}

function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`
}

function formatViews(views) {
  if (!views) return '0'
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M views`
  }
  if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K views`
  }
  return `${views} views`
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  // Format: YYYYMMDD
  const year = dateStr.substring(0, 4)
  const month = dateStr.substring(4, 6)
  const day = dateStr.substring(6, 8)
  return `${month}/${day}/${year}`
}

function handleImageError(event) {
  event.target.style.display = 'none'
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-gray-900,
.modal-leave-active .bg-gray-900 {
  transition: transform 0.3s ease;
}

.modal-enter-from .bg-gray-900,
.modal-leave-to .bg-gray-900 {
  transform: scale(0.95);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
