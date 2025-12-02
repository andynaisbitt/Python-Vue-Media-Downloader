# frontend/src/components/ui/download/NetworkSettings.vue
<template>
  <div class="space-y-4">
    <h3 class="text-sm font-medium text-gray-300">Network Settings</h3>
    
    <!-- Concurrent Downloads -->
    <div>
      <label class="block text-sm text-gray-400 mb-2">
        Concurrent Downloads
        <span class="text-xs text-gray-500 ml-1">(Higher values may affect performance)</span>
      </label>
      <div class="grid grid-cols-4 gap-2">
        <button
          v-for="value in [1, 2, 3, 4]"
          :key="value"
          @click="handleConcurrentChange(value)"
          :class="[
            'px-4 py-2 text-sm rounded-lg transition',
            value === modelValue.concurrent
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800/50 text-gray-400 hover:bg-gray-700/50'
          ]"
          :disabled="disabled"
        >
          {{ value }}
        </button>
      </div>
    </div>

    <!-- Speed Limit -->
    <div>
      <label class="block text-sm text-gray-400 mb-2">
        Speed Limit
        <span class="text-xs text-gray-500 ml-1">(0 for unlimited)</span>
      </label>
      <div class="flex gap-2">
        <input 
          type="number"
          v-model.number="speedLimit"
          min="0"
          max="100000"
          step="100"
          class="flex-1 px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
          :disabled="disabled"
        />
        <select
          v-model="speedUnit"
          class="px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
          :disabled="disabled"
        >
          <option value="KB">KB/s</option>
          <option value="MB">MB/s</option>
        </select>
      </div>
    </div>

    <!-- Chunk Size -->
    <div>
      <label class="block text-sm text-gray-400 mb-2">
        Segment Size
        <span class="text-xs text-gray-500 ml-1">(Larger sizes may improve speed)</span>
      </label>
      <div class="relative">
        <input
          type="range"
          v-model.number="modelValue.segmentSize"
          min="1"
          max="32"
          step="1"
          class="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer"
          :disabled="disabled"
          @input="updateSegmentSize"
        />
        <div class="mt-2 text-sm text-gray-400">
          {{ modelValue.segmentSize }} MB
        </div>
      </div>
    </div>

    <!-- Connection Settings -->
    <div>
      <h4 class="text-sm font-medium text-gray-400 mb-2">Advanced Settings</h4>
      <div class="space-y-2">
        <label class="flex items-center">
          <input
            type="checkbox"
            v-model="modelValue.ipv6"
            class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded"
            :disabled="disabled"
            @change="updateSettings"
          />
          <span class="ml-2 text-sm text-gray-400">Enable IPv6</span>
        </label>

        <label class="flex items-center">
          <input
            type="checkbox"
            v-model="modelValue.resumeDownloads"
            class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded"
            :disabled="disabled"
            @change="updateSettings"
          />
          <span class="ml-2 text-sm text-gray-400">Resume interrupted downloads</span>
        </label>

        <label class="flex items-center">
          <input
            type="checkbox"
            v-model="modelValue.forceHttp"
            class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded"
            :disabled="disabled"
            @change="updateSettings"
          />
          <span class="ml-2 text-sm text-gray-400">Force HTTP connection</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: () => ({
      concurrent: 1,
      speedLimit: 0,
      segmentSize: 8,
      ipv6: false,
      resumeDownloads: true,
      forceHttp: false
    })
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

// Local state for speed limit handling
const speedLimit = ref(0)
const speedUnit = ref('MB')

// Convert speed limit when unit changes
watch([speedLimit, speedUnit], () => {
  let speedInBytes = speedLimit.value
  if (speedUnit.value === 'MB') {
    speedInBytes *= 1024
  }
  updateSettings({ speedLimit: speedInBytes })
}, { immediate: true })

// Methods
function handleConcurrentChange(value) {
  updateSettings({ concurrent: value })
}

function updateSegmentSize(event) {
  updateSettings({ segmentSize: parseInt(event.target.value) })
}

function updateSettings(newValues = {}) {
  emit('update:modelValue', {
    ...props.modelValue,
    ...newValues
  })
}

// Format speed for display
function formatSpeed(bytesPerSecond) {
  if (bytesPerSecond >= 1024 * 1024) {
    return `${(bytesPerSecond / (1024 * 1024)).toFixed(1)} MB/s`
  }
  return `${(bytesPerSecond / 1024).toFixed(1)} KB/s`
}
</script>

<style scoped>
/* Custom range input styling */
input[type="range"] {
  @apply appearance-none bg-gray-800 h-2 rounded-lg;
}

input[type="range"]::-webkit-slider-thumb {
  @apply appearance-none w-4 h-4 bg-purple-500 rounded-full cursor-pointer;
}

input[type="range"]::-moz-range-thumb {
  @apply w-4 h-4 bg-purple-500 border-none rounded-full cursor-pointer;
}

input[type="range"]:disabled {
  @apply opacity-50 cursor-not-allowed;
}

input[type="range"]:disabled::-webkit-slider-thumb {
  @apply cursor-not-allowed;
}

input[type="range"]:disabled::-moz-range-thumb {
  @apply cursor-not-allowed;
}
</style>