# frontend/src/components/ui/download/DownloadItem.vue
<template>
  <div class="bg-gray-900/50 backdrop-blur-sm p-4 rounded-xl border border-gray-800">
    <div class="flex items-start gap-4">
      <!-- Thumbnail -->
      <div class="w-40 h-24 bg-gray-800 rounded-lg overflow-hidden flex-shrink-0">
        <img 
          v-if="download.thumbnail_url"
          :src="download.thumbnail_url"
          :alt="download.title"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full flex items-center justify-center">
          <Video class="w-8 h-8 text-gray-600" />
        </div>
      </div>

      <!-- Info and Controls -->
      <div class="flex-1 min-w-0">
        <!-- Title and Basic Info -->
        <h4 class="text-white font-medium truncate">{{ download.title }}</h4>
        <div class="mt-1 flex items-center text-sm text-gray-400">
          <span>{{ formatFileSize }}</span>
          <span class="mx-2">•</span>
          <span>{{ formatDuration }}</span>
          <span class="mx-2">•</span>
          <span>{{ download.format.toUpperCase() }}</span>
        </div>

        <!-- Progress Bar (if downloading, processing, or starting) -->
        <div v-if="isActiveDownload" class="mt-3 space-y-3">
          <!-- Preparing State -->
          <div v-if="download.status === 'preparing'" class="space-y-2">
            <div class="h-2 bg-gray-800 rounded-full overflow-hidden">
              <div class="h-full w-1/3 bg-gradient-to-r from-blue-600 to-purple-600 animate-pulse-slow"></div>
            </div>
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span class="animate-pulse">Preparing download...</span>
            </div>
          </div>

          <!-- Starting/Queued State -->
          <div v-else-if="download.status === 'starting' || download.status === 'queued'" class="space-y-2">
            <div class="h-2 bg-gray-800 rounded-full overflow-hidden">
              <div class="h-full w-1/2 bg-gradient-to-r from-purple-600 to-pink-600 animate-pulse-slow"></div>
            </div>
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span class="animate-pulse">{{ download.status === 'queued' ? 'Waiting in queue...' : 'Initializing download...' }}</span>
            </div>
          </div>

          <!-- Active Download State -->
          <div v-else class="space-y-3">
            <!-- Progress Bar with ULTRA smooth transitions -->
            <div class="relative group">
              <!-- Main progress bar container with glow -->
              <div class="h-3 bg-gradient-to-r from-gray-800 to-gray-900 rounded-full overflow-hidden shadow-lg border border-gray-700/50 relative">
                <!-- Background particles effect -->
                <div class="absolute inset-0 bg-gradient-to-r from-purple-900/20 to-pink-900/20"></div>

                <!-- Actual progress bar -->
                <div
                  class="h-full bg-gradient-to-r from-purple-600 via-purple-500 to-pink-600 relative transition-all duration-500 ease-out"
                  :style="{ width: `${smoothProgress}%` }"
                >
                  <!-- Triple shimmer layers for depth -->
                  <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent animate-shimmer"></div>
                  <div class="absolute inset-0 bg-gradient-to-r from-transparent via-purple-300/30 to-transparent animate-shimmer-slow"></div>

                  <!-- Pulsing glow effect -->
                  <div class="absolute inset-0 bg-gradient-to-r from-purple-400/60 to-pink-400/60 blur-md animate-pulse-glow"></div>

                  <!-- Leading edge highlight -->
                  <div class="absolute right-0 top-0 bottom-0 w-1 bg-white/60 shadow-lg"></div>
                </div>

                <!-- Progress trail effect -->
                <div class="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/10 to-transparent pointer-events-none"></div>
              </div>

              <!-- Floating percentage indicator -->
              <div class="absolute -top-6 right-0">
                <div class="bg-gradient-to-r from-purple-600 to-pink-600 px-3 py-1 rounded-lg shadow-xl animate-float">
                  <span class="text-xs font-bold text-white drop-shadow-lg">
                    {{ Math.round(smoothProgress) }}%
                  </span>
                </div>
              </div>
            </div>

            <!-- Bytes Transferred Display with animated counter -->
            <div v-if="downloadedBytes !== null && totalBytes" class="relative">
              <div class="flex items-center justify-between bg-gradient-to-r from-gray-800/50 to-gray-900/50 px-4 py-2 rounded-lg border border-purple-500/20">
                <div class="flex items-center gap-3">
                  <!-- Animated data pulse -->
                  <div class="relative">
                    <div class="w-3 h-3 bg-purple-500 rounded-full animate-ping absolute"></div>
                    <div class="w-3 h-3 bg-purple-400 rounded-full"></div>
                  </div>

                  <!-- Byte counter with gradient -->
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 text-sm">
                      {{ formatBytesTransferred(downloadedBytes) }}
                    </span>
                    <span class="text-gray-500 text-xs">/</span>
                    <span class="font-medium text-gray-400 text-sm">
                      {{ formatBytesTransferred(totalBytes) }}
                    </span>
                  </div>
                </div>

                <!-- Download percentage ring -->
                <div class="text-purple-400 text-xs font-bold">
                  {{ Math.round((downloadedBytes / totalBytes) * 100) }}%
                </div>
              </div>
            </div>

            <!-- Speed, ETA, and Status with enhanced styling -->
            <div class="flex items-center gap-2 flex-wrap">
              <!-- Download Speed with animated icon -->
              <div v-if="download.speed && download.speed > 0" class="flex items-center gap-2 bg-gradient-to-r from-green-900/30 to-emerald-900/30 border border-green-500/30 px-3 py-2 rounded-lg group hover:scale-105 transition-transform">
                <svg class="w-4 h-4 text-green-400 animate-bounce-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path>
                </svg>
                <div class="flex flex-col">
                  <span class="text-[10px] text-green-300/60 uppercase tracking-wide">Speed</span>
                  <span class="font-bold text-green-400 text-sm">{{ formatSpeed(download.speed) }}</span>
                </div>
              </div>

              <!-- ETA with countdown animation -->
              <div v-if="download.eta" class="flex items-center gap-2 bg-gradient-to-r from-blue-900/30 to-cyan-900/30 border border-blue-500/30 px-3 py-2 rounded-lg group hover:scale-105 transition-transform">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="flex flex-col">
                  <span class="text-[10px] text-blue-300/60 uppercase tracking-wide">ETA</span>
                  <span class="font-bold text-blue-400 text-sm">{{ formatETA(download.eta) }}</span>
                </div>
              </div>

              <!-- Processing status -->
              <span v-if="download.status === 'processing'" class="flex items-center gap-1.5 text-yellow-400 bg-yellow-500/10 px-2 py-1 rounded-md">
                <svg class="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                <span class="font-medium">Processing...</span>
              </span>
            </div>

            <!-- SICK Speed Graph with glow effects -->
            <div v-if="download.speed && speedHistory.length > 1" class="relative mt-2">
              <div class="text-[10px] text-gray-500 uppercase tracking-wide mb-1">Network Speed</div>
              <div class="h-12 flex items-end gap-1 bg-gray-900/50 rounded-lg p-2 border border-purple-500/10">
                <div
                  v-for="(speed, index) in speedHistory"
                  :key="index"
                  class="flex-1 bg-gradient-to-t from-purple-600 via-purple-500 to-pink-500 rounded-t transition-all duration-500 relative group"
                  :style="{
                    height: `${Math.max((speed / maxSpeedInHistory) * 100, 5)}%`,
                    opacity: 0.4 + (index / speedHistory.length) * 0.6
                  }"
                >
                  <!-- Glow on hover -->
                  <div class="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity rounded-t"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Status and Actions -->
        <div class="mt-2 flex items-center gap-3">
          <!-- Status Badge -->
          <span 
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
            :class="statusClasses"
          >
            {{ download.status }}
          </span>

          <!-- Action Buttons -->
          <div class="flex items-center gap-2">
            <!-- Download Button (when completed) -->
            <button
              v-if="download.status === 'completed'"
              @click="handleDownload"
              class="inline-flex items-center px-2 py-1 text-sm text-white bg-purple-600 hover:bg-purple-500 rounded-lg transition"
            >
              <Download class="w-4 h-4 mr-1" />
              Download
            </button>

            <!-- Retry Button (when failed) -->
            <button
              v-if="download.status === 'failed'"
              @click="handleRetry"
              class="inline-flex items-center px-2 py-1 text-sm text-white bg-gray-700 hover:bg-gray-600 rounded-lg transition"
            >
              <RefreshCcw class="w-4 h-4 mr-1" />
              Retry
            </button>

            <!-- Cancel Button (when downloading) -->
            <button
              v-if="download.status === 'downloading'"
              @click="handleCancel"
              class="inline-flex items-center px-2 py-1 text-sm text-red-400 hover:text-red-300 transition"
            >
              <X class="w-4 h-4 mr-1" />
              Cancel
            </button>

            <!-- Delete Button -->
            <button
              @click="handleDelete"
              class="inline-flex items-center px-2 py-1 text-sm text-gray-400 hover:text-gray-300 transition"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Error Message (if failed) -->
        <p v-if="download.status === 'failed'" class="mt-2 text-sm text-red-400">
          {{ download.error }}
        </p>

        <!-- Additional Info (subtitles, etc.) -->
        <div v-if="hasAdditionalFiles" class="mt-2 flex flex-wrap gap-2">
          <button
            v-if="download.subtitles"
            @click="handleSubtitlesDownload"
            class="inline-flex items-center px-2 py-1 text-xs text-gray-400 hover:text-gray-300 bg-gray-800/50 rounded-lg transition"
          >
            <FileText class="w-3 h-3 mr-1" />
            Subtitles
          </button>
          <button
            v-if="download.transcript"
            @click="handleTranscriptDownload"
            class="inline-flex items-center px-2 py-1 text-xs text-gray-400 hover:text-gray-300 bg-gray-800/50 rounded-lg transition"
          >
            <FileText class="w-3 h-3 mr-1" />
            Transcript
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { Download, Video, RefreshCcw, X, Trash2, FileText } from 'lucide-vue-next'
import { formatBytes, formatSpeed, formatETA } from '@/stores/download'

const props = defineProps({
  download: {
    type: Object,
    required: true,
    validator(obj) {
      return ['title', 'status', 'format'].every(prop => prop in obj)
    }
  }
})

const emit = defineEmits([
  'download',
  'retry',
  'cancel',
  'delete',
  'download-subtitles',
  'download-transcript'
])

// Reactive state for smooth animations
const smoothProgress = ref(0)
const speedHistory = ref([])
const maxSpeedInHistory = ref(0)
const MAX_SPEED_HISTORY = 20 // Keep last 20 speed readings

// Watch for progress changes and smooth them out
watch(
  () => props.download.progress,
  (newProgress) => {
    if (newProgress !== undefined && newProgress !== null) {
      // Debug logging
      console.log('🎯 DownloadItem Progress Update:', {
        id: props.download.id,
        title: props.download.title,
        progress: newProgress,
        status: props.download.status,
        speed: props.download.speed,
        downloaded_bytes: props.download.downloaded_bytes,
        total_bytes: props.download.total_bytes
      });

      // Smooth transition to new progress value
      smoothProgress.value = newProgress
    }
  },
  { immediate: true }
)

// Watch for speed changes and track history
watch(
  () => props.download.speed,
  (newSpeed) => {
    if (newSpeed && newSpeed > 0) {
      speedHistory.value.push(newSpeed)

      // Keep only last N readings
      if (speedHistory.value.length > MAX_SPEED_HISTORY) {
        speedHistory.value.shift()
      }

      // Update max speed for graph scaling
      maxSpeedInHistory.value = Math.max(...speedHistory.value)
    }
  }
)

// Reset speed history when download status changes to non-downloading
watch(
  () => props.download.status,
  (newStatus) => {
    if (!['downloading', 'processing'].includes(newStatus)) {
      speedHistory.value = []
      maxSpeedInHistory.value = 0
    }
  }
)

// Computed Properties
const isActiveDownload = computed(() => {
  return ['preparing', 'queued', 'starting', 'downloading', 'processing'].includes(props.download.status)
})

const downloadedBytes = computed(() => {
  // Use real-time downloaded_bytes from backend if available
  if (props.download.downloaded_bytes !== undefined && props.download.downloaded_bytes !== null) {
    return props.download.downloaded_bytes
  }

  // Fallback: calculate from progress and size
  const progress = props.download.progress || 0
  const totalSize = props.download.size || props.download.total_bytes || 0

  if (totalSize && progress > 0) {
    return (totalSize * progress) / 100
  }

  return null
})

const totalBytes = computed(() => {
  // Use real-time total_bytes from backend if available
  if (props.download.total_bytes !== undefined && props.download.total_bytes !== null) {
    return props.download.total_bytes
  }

  // Fallback to size (for completed downloads)
  return props.download.size || null
})

const formatBytesTransferred = (bytes) => {
  if (!bytes) return '0 B'

  const units = ['B', 'KB', 'MB', 'GB']
  let unitIndex = 0
  let formattedSize = bytes

  while (formattedSize >= 1024 && unitIndex < units.length - 1) {
    formattedSize /= 1024
    unitIndex++
  }

  return `${formattedSize.toFixed(1)} ${units[unitIndex]}`
}

const formatFileSize = computed(() => {
  const size = props.download.size || 0
  const units = ['B', 'KB', 'MB', 'GB']
  let unitIndex = 0
  let formattedSize = size

  while (formattedSize >= 1024 && unitIndex < units.length - 1) {
    formattedSize /= 1024
    unitIndex++
  }

  return `${formattedSize.toFixed(1)} ${units[unitIndex]}`
})

const formatDuration = computed(() => {
  const duration = props.download.duration || 0
  const hours = Math.floor(duration / 3600)
  const minutes = Math.floor((duration % 3600) / 60)
  const seconds = duration % 60

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

const statusClasses = computed(() => ({
  'bg-purple-500/20 text-purple-400 border border-purple-500/30': props.download.status === 'downloading',
  'bg-green-500/20 text-green-400 border border-green-500/30': props.download.status === 'completed',
  'bg-red-500/20 text-red-400 border border-red-500/30': props.download.status === 'failed',
  'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30': props.download.status === 'processing',
  'bg-blue-500/20 text-blue-400 border border-blue-500/30': props.download.status === 'queued' || props.download.status === 'starting' || props.download.status === 'preparing'
}))

const hasAdditionalFiles = computed(() => {
  return props.download.subtitles || props.download.transcript
})

// Event Handlers
function handleDownload() {
  emit('download', props.download)
}

function handleRetry() {
  emit('retry', props.download)
}

function handleCancel() {
  emit('cancel', props.download)
}

function handleDelete() {
  emit('delete', props.download)
}

function handleSubtitlesDownload() {
  emit('download-subtitles', props.download)
}

function handleTranscriptDownload() {
  emit('download-transcript', props.download)
}
</script>

<style scoped>
/* Ultra smooth shimmer effect */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-shimmer {
  animation: shimmer 1.5s infinite ease-in-out;
}

/* Slower shimmer for depth */
@keyframes shimmer-slow {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-shimmer-slow {
  animation: shimmer-slow 3s infinite ease-in-out;
}

/* Pulsing glow effect */
@keyframes pulse-glow {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

/* Floating animation for percentage badge */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-4px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Slow pulse */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Slow bounce for download icon */
@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

.animate-bounce-slow {
  animation: bounce-slow 1.5s ease-in-out infinite;
}

/* Smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Status badge animations */
@keyframes badge-appear {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.inline-flex {
  animation: badge-appear 0.3s ease-out;
}

/* Gradient text animation */
@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* Ping animation for data pulse */
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}
</style>