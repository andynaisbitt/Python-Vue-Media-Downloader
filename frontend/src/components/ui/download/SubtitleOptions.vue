# frontend/src/components/ui/download/QueueList.vue
<template>
  <div class="bg-gray-900/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-800">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 class="text-lg font-medium text-white">Download Queue</h3>
        <p class="text-sm text-gray-400">{{ queueStatus }}</p>
      </div>
      
      <!-- Queue Controls -->
      <div class="flex items-center gap-2">
        <button
          v-if="hasActive"
          @click="$emit('pause-all')"
          :class="[
            'inline-flex items-center px-3 py-1.5 rounded-lg text-sm transition',
            isPaused ? 'text-purple-400 hover:text-purple-300' : 'text-gray-400 hover:text-gray-300'
          ]"
        >
          <component :is="isPaused ? Play : Pause" class="w-4 h-4 mr-1" />
          {{ isPaused ? 'Resume All' : 'Pause All' }}
        </button>

        <button
          v-if="hasActive"
          @click="$emit('cancel-all')"
          class="inline-flex items-center px-3 py-1.5 text-red-400 hover:text-red-300 rounded-lg text-sm transition"
        >
          <X class="w-4 h-4 mr-1" />
          Cancel All
        </button>
      </div>
    </div>

    <!-- Queue Items -->
    <div class="space-y-4">
      <TransitionGroup name="queue">
        <div
          v-for="item in queue"
          :key="item.id"
          class="bg-gray-800/50 rounded-lg p-4"
        >
          <div class="flex items-start justify-between">
            <!-- Title and Info -->
            <div class="flex-1 min-w-0 mr-4">
              <h4 class="text-white font-medium truncate">{{ item.title }}</h4>
              <div class="mt-1 flex items-center text-sm text-gray-400">
                <span>{{ formatFileSize(item.downloaded) }} / {{ formatFileSize(item.size) }}</span>
                <span class="mx-2">•</span>
                <span>{{ formatSpeed(item.speed) }}</span>
                <span class="mx-2">•</span>
                <span>{{ formatTimeRemaining(item.timeRemaining) }}</span>
              </div>
              
              <!-- Progress Bar -->
              <div class="mt-2 relative">
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div
                    class="h-full bg-purple-600 transition-all duration-300"
                    :style="{ width: `${item.progress}%` }"
                  ></div>
                </div>
                <span class="mt-1 text-xs text-gray-400">{{ item.progress.toFixed(1) }}%</span>
              </div>

              <!-- Status Messages -->
              <p v-if="item.status === 'processing'" class="mt-1 text-sm text-yellow-400">
                {{ item.statusMessage }}
              </p>
              <p v-if="item.error" class="mt-1 text-sm text-red-400">
                {{ item.error }}
              </p>
            </div>

            <!-- Item Controls -->
            <div class="flex items-start gap-2">
              <button
                @click="$emit('toggle-pause', item)"
                class="p-1.5 text-gray-400 hover:text-gray-300 rounded-lg transition"
                :title="item.paused ? 'Resume' : 'Pause'"
              >
                <component :is="item.paused ? Play : Pause" class="w-4 h-4" />
              </button>

              <button
                @click="$emit('cancel', item)"
                class="p-1.5 text-red-400 hover:text-red-300 rounded-lg transition"
                title="Cancel"
              >
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </TransitionGroup>

      <!-- Empty State -->
      <div 
        v-if="queue.length === 0" 
        class="text-center py-8 text-gray-400"
      >
        <Inbox class="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No active downloads</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Play, Pause, X, Inbox } from 'lucide-vue-next'

const props = defineProps({
  queue: {
    type: Array,
    required: true,
    default: () => []
  },
  isPaused: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['pause-all', 'cancel-all', 'toggle-pause', 'cancel'])

// Computed Properties
const hasActive = computed(() => props.queue.length > 0)

const queueStatus = computed(() => {
  const activeCount = props.queue.filter(item => !item.paused).length
  const totalCount = props.queue.length
  
  if (totalCount === 0) return 'No active downloads'
  if (props.isPaused) return 'Queue paused'
  return `${activeCount} of ${totalCount} downloads active`
})

// Utility Functions
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

function formatSpeed(bytesPerSecond) {
  if (!bytesPerSecond) return '0 KB/s'
  if (bytesPerSecond >= 1024 * 1024) {
    return `${(bytesPerSecond / (1024 * 1024)).toFixed(1)} MB/s`
  }
  return `${(bytesPerSecond / 1024).toFixed(1)} KB/s`
}

function formatTimeRemaining(seconds) {
  if (!seconds) return 'Calculating...'
  if (seconds === Infinity) return 'Unknown'

  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours}h ${minutes}m remaining`
  }
  if (minutes > 0) {
    return `${minutes}m ${secs}s remaining`
  }
  return `${secs}s remaining`
}
</script>

<style scoped>
.queue-enter-active,
.queue-leave-active {
  transition: all 0.3s ease;
}

.queue-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.queue-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.queue-move {
  transition: transform 0.3s ease;
}
</style>