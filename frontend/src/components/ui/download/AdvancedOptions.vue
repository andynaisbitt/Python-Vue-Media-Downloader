# frontend/src/components/ui/download/AdvancedOptions.vue
<template>
  <div class="space-y-6">
    <!-- Toggle Button -->
    <button 
      type="button"
      @click="isOpen = !isOpen"
      class="flex items-center text-sm text-purple-400 hover:text-purple-300 focus:outline-none"
    >
      <ChevronRight 
        class="h-4 w-4 mr-1 transition-transform duration-200"
        :class="{ 'rotate-90': isOpen }"
      />
      Advanced Options
    </button>

    <!-- Options Panel -->
    <div v-show="isOpen" class="space-y-6 animate-fadeIn">
      <!-- Time Range -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-300">Time Range</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Start Time (HH:MM:SS)</label>
            <input 
              type="text" 
              v-model="timeRange.start"
              placeholder="00:00:00"
              class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
              :disabled="props.disabled"
              @input="validateTimeFormat"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-2">End Time (HH:MM:SS)</label>
            <input 
              type="text" 
              v-model="timeRange.end"
              placeholder="00:00:00"
              class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
              :disabled="props.disabled"
              @input="validateTimeFormat"
            />
          </div>
        </div>
      </div>

      <!-- Network Settings -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-300">Network Settings</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Concurrent Downloads</label>
            <select 
              v-model="networkSettings.concurrent"
              class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
              :disabled="props.disabled"
            >
              <option value="1">1 (Recommended)</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-2">Segment Size (MB)</label>
            <input 
              type="number" 
              v-model="networkSettings.segmentSize"
              min="1"
              max="100"
              class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
              :disabled="props.disabled"
            />
          </div>
        </div>
      </div>

      <!-- Advanced Subtitle Options -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-300">Advanced Subtitle Options</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Language</label>
            <select 
              v-model="subtitleOptions.language"
              class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
              :disabled="!subtitleOptions.enabled || props.disabled"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="ja">Japanese</option>
              <option value="ko">Korean</option>
              <option value="auto">Auto-detect</option>
            </select>
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-2">Format</label>
            <select 
              v-model="subtitleOptions.format"
              class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
              :disabled="!subtitleOptions.enabled || props.disabled"
            >
              <option value="srt">SRT</option>
              <option value="vtt">VTT (Web)</option>
              <option value="ass">ASS (Advanced)</option>
            </select>
          </div>
        </div>
        <div class="space-y-2">
          <label class="inline-flex items-center">
            <input 
              type="checkbox" 
              v-model="subtitleOptions.enabled"
              class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded"
              :disabled="props.disabled"
            />
            <span class="ml-2 text-sm text-gray-300">Enable Advanced Subtitle Options</span>
          </label>
          <label class="inline-flex items-center" v-if="subtitleOptions.enabled">
            <input 
              type="checkbox" 
              v-model="subtitleOptions.translate"
              class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded"
              :disabled="props.disabled"
            />
            <span class="ml-2 text-sm text-gray-300">Auto-translate to selected language</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:options'])

const isOpen = ref(false)

const timeRange = ref({
  start: '',
  end: ''
})

const networkSettings = ref({
  concurrent: '1',
  segmentSize: 10
})

const subtitleOptions = ref({
  enabled: false,
  language: 'en',
  format: 'srt',
  translate: false
})

// Validate time format (HH:MM:SS)
function validateTimeFormat(event) {
  const timePattern = /^([0-9]{0,2}:)?[0-5]?[0-9]:[0-5]?[0-9]$/
  const value = event.target.value

  if (value && !timePattern.test(value)) {
    event.target.classList.add('border-red-500')
  } else {
    event.target.classList.remove('border-red-500')
  }
}

// Watch for changes and emit updated options
watch([timeRange, networkSettings, subtitleOptions], () => {
  emit('update:options', {
    timeRange: timeRange.value,
    networkSettings: networkSettings.value,
    subtitleOptions: subtitleOptions.value
  })
}, { deep: true })
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>