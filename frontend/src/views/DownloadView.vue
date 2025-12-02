<template>
  <div class="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12" v-motion-slide-top>
        <h2 class="text-3xl font-bold text-white">Download Center</h2>
        <p class="mt-2 text-gray-400">Download videos and audio with advanced options</p>
      </div>

      <!-- Main Download Form -->
      <div class="bg-gray-900/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-800" v-motion-slide-bottom>
        <DownloadForm
          :loading="isProcessingMetadata"
          @submit="handleFormSubmit"
        />

        <AdvancedOptions
          v-model="advancedOptions"
          :disabled="downloadStore.isLoading"
          class="mt-6"
        />
      </div>

      <!-- Download Progress & Queue -->
      <div v-if="downloadStore.isLoading || downloadStore.queue.length > 0" class="mt-8">
        <QueueList
          :queue="combinedQueue"
          :is-paused="downloadStore.isPaused"
          @pause-all="handlePauseAll"
          @cancel="handleCancel"
        />
      </div>

      <!-- Downloads List (Completed/Failed) -->
      <DownloadList
        v-if="downloadStore.downloads.length > 0"
        :downloads="downloadStore.downloads"
        class="mt-8"
        @download="handleDownloadFile"
        @delete="handleDelete"
      />

      <!-- Video Preview Modal -->
      <VideoPreviewModal
        :show="showPreviewModal"
        :urls="previewUrls"
        :download-options="previewDownloadOptions"
        @close="handlePreviewClose"
        @confirm="handlePreviewConfirm"
      />

      <!-- Completion Notification -->
      <CompletionNotification
        :show="showCompletionNotification"
        :download="completedDownload"
        :auto-close="true"
        :auto-close-duration="8"
        @close="handleCompletionClose"
        @download="handleDownloadFile"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useDownloadStore } from '../stores/download'

// Import our custom components
import DownloadForm from '@/components/ui/download/DownloadForm.vue'
import AdvancedOptions from '@/components/ui/download/AdvancedOptions.vue'
import QueueList from '@/components/ui/download/QueueList.vue'
import DownloadList from '@/components/ui/download/DownloadList.vue'
import VideoPreviewModal from '@/components/ui/download/VideoPreviewModal.vue'
import CompletionNotification from '@/components/ui/download/CompletionNotification.vue'

const downloadStore = useDownloadStore()

// State
const isProcessingMetadata = ref(false)
const showPreviewModal = ref(false)
const previewUrls = ref([])
const previewDownloadOptions = ref({})
const showCompletionNotification = ref(false)
const completedDownload = ref(null)

// Combined queue for the UI
const combinedQueue = computed(() => {
  const queue = [];
  if (downloadStore.currentDownload) {
    queue.push(downloadStore.currentDownload);
  }
  return queue.concat(downloadStore.queue);
});

// Advanced options state
const advancedOptions = ref({
  subtitles: {
    enabled: false,
    language: 'en',
    format: 'srt'
  },
  timeRange: {
    start: '',
    end: ''
  }
})

// Watch for completed downloads to show notifications
watch(
  () => downloadStore.completedDownloadsToNotify.length,
  (newLength) => {
    if (newLength > 0 && !showCompletionNotification.value) {
      const download = downloadStore.getNextCompletedDownload()
      if (download) {
        completedDownload.value = download
        showCompletionNotification.value = true
      }
    }
  }
)

// Event handlers
async function handleFormSubmit(options) {
  // Store the options for the preview modal
  previewDownloadOptions.value = {
    format: options.format,
    quality: options.quality,
    subtitles: options.subtitles,
    transcribe: options.transcribe
  }

  // Store the URLs
  previewUrls.value = options.urls

  // Show preview modal
  showPreviewModal.value = true
}

function handlePreviewClose() {
  showPreviewModal.value = false
  previewUrls.value = []
}

async function handlePreviewConfirm(metadata) {
  // Close the preview modal
  showPreviewModal.value = false

  // Start downloading each video
  for (const video of metadata.videos) {
    const downloadOptions = {
      url: video.webpage_url || previewUrls.value[0], // Fallback to first URL if webpage_url not available
      format: previewDownloadOptions.value.format || 'mp4',
      quality: previewDownloadOptions.value.quality || 'best',
      subtitles: previewDownloadOptions.value.subtitles || false,
      transcribe: previewDownloadOptions.value.transcribe || false,
      advancedOptions: { ...advancedOptions.value },
      metadata: {
        title: video.title,
        thumbnail_url: video.thumbnail_url,
        duration: video.duration
      }
    }

    await downloadStore.startDownload(downloadOptions)
  }

  // Clear preview data
  previewUrls.value = []
  previewDownloadOptions.value = {}
}

function handlePauseAll() {
  downloadStore.setPaused(!downloadStore.isPaused)
}

function handleCancel(download) {
  downloadStore.cancelDownload(download.id)
}

function handleDelete(download) {
  downloadStore.removeDownload(download.id)
}

function handleDownloadFile(download) {
  downloadStore.downloadFile(download)
}

function handleCompletionClose() {
  showCompletionNotification.value = false

  // Wait for animation to finish, then check for next notification
  setTimeout(() => {
    const nextDownload = downloadStore.getNextCompletedDownload()
    if (nextDownload) {
      completedDownload.value = nextDownload
      showCompletionNotification.value = true
    }
  }, 300)
}
</script>
