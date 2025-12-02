# frontend/src/components/ui/common/ProgressBar.vue
<template>
  <div class="w-full">
    <!-- Label -->
    <div v-if="label || showPercentage" class="flex justify-between mb-1">
      <span class="text-sm font-medium text-gray-300">{{ label }}</span>
      <span v-if="showPercentage" class="text-sm text-gray-400">{{ progress }}%</span>
    </div>

    <!-- Progress Bar -->
    <div class="relative">
      <div
        class="w-full h-2 bg-gray-800 rounded-full overflow-hidden"
        :class="{ 'animate-pulse': indeterminate }"
      >
        <div
          class="h-full transition-all duration-300 rounded-full"
          :class="[
            indeterminate ? 'animate-indeterminate' : '',
            variantClasses
          ]"
          :style="indeterminate ? {} : { width: `${progress}%` }"
        ></div>
      </div>

      <!-- Status Text -->
      <div v-if="status" class="mt-1 text-xs text-gray-400">
        {{ status }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  progress: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  label: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    default: ''
  },
  showPercentage: {
    type: Boolean,
    default: false
  },
  indeterminate: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger'].includes(value)
  }
})

const variantClasses = computed(() => ({
  'bg-purple-600': props.variant === 'primary',
  'bg-green-500': props.variant === 'success',
  'bg-yellow-500': props.variant === 'warning',
  'bg-red-500': props.variant === 'danger'
}))
</script>

<style scoped>
.animate-indeterminate {
  animation: indeterminate 1.5s infinite linear;
  width: 30%;
}

@keyframes indeterminate {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(400%);
  }
}
</style>