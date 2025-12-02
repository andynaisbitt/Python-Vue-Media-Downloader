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
      <TransitionGroup name="queue" tag="div" class="space-y-4">
        <DownloadItem
          v-for="item in queue"
          :key="item.id"
          :download="item"
          @cancel="$emit('cancel', item)"
        />

        <!-- Empty State -->
        <div
          v-if="queue.length === 0"
          :key="'empty'"
          class="text-center py-8 text-gray-400"
        >
          <Inbox class="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No active downloads</p>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Play, Pause, X, Inbox } from 'lucide-vue-next'
import DownloadItem from './DownloadItem.vue'

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