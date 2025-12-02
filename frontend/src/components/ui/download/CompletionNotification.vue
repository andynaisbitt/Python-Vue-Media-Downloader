<template>
  <Transition name="notification">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      @click.self="handleClose"
    >
      <div class="relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl border border-gray-700 w-full max-w-2xl shadow-2xl overflow-hidden">
        <!-- Success Header with Animation -->
        <div class="relative bg-gradient-to-r from-green-600/20 to-emerald-600/20 border-b border-green-500/30 px-6 py-6">
          <div class="flex items-center gap-4">
            <!-- Animated Check Icon -->
            <div class="relative">
              <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center shadow-lg animate-scale-in">
                <CheckCircle class="w-10 h-10 text-white animate-check-draw" />
              </div>
              <!-- Glow effect -->
              <div class="absolute inset-0 bg-green-500 rounded-full blur-xl opacity-30 animate-pulse"></div>
            </div>

            <div class="flex-1">
              <h2 class="text-2xl font-bold text-white mb-1">
                Download Complete!
              </h2>
              <p class="text-green-300">
                {{ download.title || 'Your video' }} is ready
              </p>
            </div>

            <button
              @click="handleClose"
              class="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-gray-700/50 transition"
            >
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6">
          <!-- Thumbnail and Info -->
          <div class="flex gap-4 mb-6">
            <!-- Thumbnail -->
            <div class="w-48 h-27 bg-gray-800 rounded-lg overflow-hidden flex-shrink-0">
              <img
                v-if="download.thumbnail_url"
                :src="download.thumbnail_url"
                :alt="download.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <Video class="w-12 h-12 text-gray-600" />
              </div>
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="space-y-2">
                <div class="flex items-center gap-2 text-sm">
                  <FileVideo class="w-4 h-4 text-purple-400" />
                  <span class="text-gray-400">Format:</span>
                  <span class="text-white font-medium">{{ download.format?.toUpperCase() || 'MP4' }}</span>
                </div>
                <div v-if="download.size" class="flex items-center gap-2 text-sm">
                  <HardDrive class="w-4 h-4 text-purple-400" />
                  <span class="text-gray-400">Size:</span>
                  <span class="text-white font-medium">{{ formatFileSize(download.size) }}</span>
                </div>
                <div v-if="download.duration" class="flex items-center gap-2 text-sm">
                  <Clock class="w-4 h-4 text-purple-400" />
                  <span class="text-gray-400">Duration:</span>
                  <span class="text-white font-medium">{{ formatDuration(download.duration) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div class="bg-gray-800/50 rounded-lg p-4 text-center border border-gray-700/50">
              <div class="text-2xl font-bold text-green-400">100%</div>
              <div class="text-xs text-gray-400 mt-1">Downloaded</div>
            </div>
            <div class="bg-gray-800/50 rounded-lg p-4 text-center border border-gray-700/50">
              <div class="text-2xl font-bold text-purple-400">{{ download.quality || 'Best' }}</div>
              <div class="text-xs text-gray-400 mt-1">Quality</div>
            </div>
            <div class="bg-gray-800/50 rounded-lg p-4 text-center border border-gray-700/50">
              <div class="text-2xl font-bold text-blue-400">✓</div>
              <div class="text-xs text-gray-400 mt-1">Processed</div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex gap-3">
            <button
              @click="handleDownloadFile"
              class="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-lg transition shadow-lg flex items-center justify-center gap-2 font-medium"
            >
              <Download class="w-5 h-5" />
              Download File
            </button>
            <button
              @click="handleClose"
              class="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition flex items-center gap-2"
            >
              <span>Close</span>
            </button>
          </div>

          <!-- Additional Info -->
          <div class="mt-4 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <div class="flex items-start gap-2">
              <Info class="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
              <div class="text-sm">
                <p class="text-blue-300 font-medium">File saved to downloads folder</p>
                <p class="text-blue-400/70 mt-1">You can close this notification. Your file is ready to use.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Auto-close countdown -->
        <div v-if="autoCloseCountdown > 0" class="absolute bottom-0 left-0 right-0">
          <div class="h-1 bg-gray-800">
            <div
              class="h-full bg-gradient-to-r from-purple-600 to-pink-600 transition-all duration-1000"
              :style="{ width: `${(autoCloseCountdown / autoCloseDuration) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { CheckCircle, X, Video, Download, FileVideo, HardDrive, Clock, Info } from 'lucide-vue-next'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  download: {
    type: Object,
    required: true
  },
  autoClose: {
    type: Boolean,
    default: true
  },
  autoCloseDuration: {
    type: Number,
    default: 8 // 8 seconds
  }
})

const emit = defineEmits(['close', 'download'])

const autoCloseCountdown = ref(0)
let autoCloseTimer = null
let countdownInterval = null

// Watch for show changes to start auto-close
watch(() => props.show, (newVal) => {
  if (newVal && props.autoClose) {
    startAutoClose()
  } else {
    clearAutoClose()
  }
})

function startAutoClose() {
  autoCloseCountdown.value = props.autoCloseDuration

  countdownInterval = setInterval(() => {
    autoCloseCountdown.value -= 1
    if (autoCloseCountdown.value <= 0) {
      clearAutoClose()
      handleClose()
    }
  }, 1000)
}

function clearAutoClose() {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
  if (autoCloseTimer) {
    clearTimeout(autoCloseTimer)
    autoCloseTimer = null
  }
  autoCloseCountdown.value = 0
}

onUnmounted(() => {
  clearAutoClose()
})

function handleClose() {
  clearAutoClose()
  emit('close')
}

function handleDownloadFile() {
  emit('download', props.download)
  // Don't close automatically after download - let user close manually
  clearAutoClose()
}

function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let unitIndex = 0
  let size = bytes

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }

  return `${size.toFixed(1)} ${units[unitIndex]}`
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
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: opacity 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
}

.notification-enter-active > div,
.notification-leave-active > div {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.notification-enter-from > div,
.notification-leave-to > div {
  transform: scale(0.9) translateY(-20px);
}

@keyframes scale-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes check-draw {
  0% {
    stroke-dasharray: 0 100;
  }
  100% {
    stroke-dasharray: 100 100;
  }
}

.animate-check-draw {
  animation: check-draw 0.5s ease-out 0.2s forwards;
}
</style>
