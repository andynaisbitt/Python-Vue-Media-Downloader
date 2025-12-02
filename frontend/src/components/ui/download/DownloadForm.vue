<template>
  <div class="bg-gray-900/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-800">
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- URL Input - Now with textarea for batch support -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <label class="block text-sm font-medium text-gray-300">YouTube URL(s)</label>
          <button
            type="button"
            @click="toggleBatchMode"
            class="text-xs text-purple-400 hover:text-purple-300 transition"
          >
            {{ isBatchMode ? 'Single URL' : 'Batch Mode' }}
          </button>
        </div>

        <!-- Single URL Input -->
        <input
          v-if="!isBatchMode"
          v-model="formData.url"
          type="text"
          class="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
          placeholder="https://www.youtube.com/watch?v=..."
          :disabled="loading"
        />

        <!-- Batch URL Input -->
        <textarea
          v-else
          v-model="formData.urls"
          rows="4"
          class="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 font-mono text-sm"
          placeholder="Paste multiple URLs (one per line)&#10;https://www.youtube.com/watch?v=...&#10;https://www.youtube.com/watch?v=...&#10;https://www.youtube.com/watch?v=..."
          :disabled="loading"
        ></textarea>

        <p v-if="isBatchMode && urlCount > 0" class="mt-2 text-xs text-gray-400">
          {{ urlCount }} URL{{ urlCount > 1 ? 's' : '' }} detected
        </p>
      </div>

      <!-- Format and Quality Selection -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Format -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Format</label>
          <select
            v-model="formData.format"
            class="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
            :disabled="loading"
            @change="handleFormatChange"
          >
            <optgroup label="Video">
              <option value="mp4">MP4</option>
              <option value="mkv">MKV</option>
              <option value="avi">AVI</option>
            </optgroup>
            <optgroup label="Audio">
              <option value="mp3">MP3 (Audio)</option>
              <option value="aac">AAC (Audio)</option>
              <option value="wav">WAV (Audio)</option>
            </optgroup>
          </select>
        </div>

        <!-- Quality -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            {{ isAudioFormat ? 'Quality (bitrate)' : 'Video Quality' }}
          </label>
          <select
            v-model="formData.quality"
            class="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500"
            :disabled="loading"
          >
            <template v-if="isAudioFormat">
              <option value="320">320 kbps</option>
              <option value="256">256 kbps</option>
              <option value="192">192 kbps</option>
              <option value="128">128 kbps</option>
            </template>
            <template v-else>
              <option value="best">Best Quality</option>
              <option value="1080p">1080p</option>
              <option value="720p">720p</option>
              <option value="480p">480p</option>
            </template>
          </select>
        </div>
      </div>

      <!-- Additional Options -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-300">Additional Options</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label class="inline-flex items-center">
            <input
              type="checkbox"
              v-model="formData.subtitles"
              class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded focus:ring-purple-500/50"
              :disabled="loading"
            />
            <span class="ml-2 text-gray-300">Download Subtitles</span>
          </label>
          <label class="inline-flex items-center">
            <input
              type="checkbox"
              v-model="formData.transcribe"
              class="form-checkbox h-4 w-4 text-purple-500 bg-gray-800 border-gray-700 rounded focus:ring-purple-500/50"
              :disabled="loading"
            />
            <span class="ml-2 text-gray-300">Transcribe Audio</span>
          </label>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="flex justify-center">
        <button
          type="submit"
          :disabled="!isValid || loading"
          class="inline-flex items-center px-6 py-3 rounded-lg text-white bg-purple-600 hover:bg-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:ring-offset-2 focus:ring-offset-gray-900 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="!loading">{{ isBatchMode && urlCount > 1 ? `Preview ${urlCount} Videos` : 'Preview & Download' }}</span>
          <div v-else class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Fetching info...
          </div>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'update:loading'])

const isBatchMode = ref(false)

const formData = ref({
  url: '',
  urls: '', // For batch mode
  format: 'mp4',
  quality: 'best',
  subtitles: false,
  transcribe: false
})

const isAudioFormat = computed(() => {
  return ['mp3', 'aac', 'wav'].includes(formData.value.format)
})

const urlCount = computed(() => {
  if (!isBatchMode.value) return 0
  const urls = formData.value.urls
    .split('\n')
    .map(u => u.trim())
    .filter(u => u.length > 0)
  return urls.length
})

const isValid = computed(() => {
  if (isBatchMode.value) {
    return urlCount.value > 0
  }
  return formData.value.url.trim() !== ''
})

function toggleBatchMode() {
  isBatchMode.value = !isBatchMode.value

  // Transfer data between modes
  if (isBatchMode.value && formData.value.url.trim()) {
    formData.value.urls = formData.value.url
    formData.value.url = ''
  } else if (!isBatchMode.value && formData.value.urls.trim()) {
    const urls = formData.value.urls.split('\n').map(u => u.trim()).filter(u => u.length > 0)
    formData.value.url = urls[0] || ''
    formData.value.urls = ''
  }
}

function handleFormatChange() {
  // Reset quality when switching between audio/video formats
  if (isAudioFormat.value) {
    formData.value.quality = '320'
  } else {
    formData.value.quality = 'best'
  }
}

function handleSubmit() {
  if (!isValid.value) return

  // Collect URLs (single or batch)
  let urls = []
  if (isBatchMode.value) {
    urls = formData.value.urls
      .split('\n')
      .map(u => u.trim())
      .filter(u => u.length > 0)
  } else {
    urls = [formData.value.url.trim()]
  }

  const downloadOptions = {
    urls,
    format: formData.value.format,
    quality: formData.value.quality,
    subtitles: formData.value.subtitles,
    transcribe: formData.value.transcribe,
    isBatch: isBatchMode.value
  }

  console.log('Form submitting with options:', downloadOptions)

  emit('submit', downloadOptions)
}
</script>
