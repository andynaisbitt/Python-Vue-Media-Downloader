# frontend/src/components/ui/common/Button.vue
<template>
  <button
    :type="type"
    :class="[
      'inline-flex items-center justify-center rounded-lg font-medium transition',
      'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900',
      variantClasses,
      sizeClasses,
      disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
      className
    ]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <!-- Loading Spinner -->
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>

    <!-- Icon (if provided) -->
    <component
      :is="icon"
      v-if="icon && !loading"
      class="h-4 w-4"
      :class="{ 'mr-2': $slots.default }"
    />

    <!-- Button Content -->
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  type: {
    type: String,
    default: 'button'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  icon: {
    type: [Object, Function],
    default: null
  },
  className: {
    type: String,
    default: ''
  }
})

const variantClasses = computed(() => ({
  'bg-purple-600 text-white hover:bg-purple-500 focus:ring-purple-500': props.variant === 'primary',
  'bg-gray-800 text-gray-100 hover:bg-gray-700 focus:ring-gray-500': props.variant === 'secondary',
  'bg-red-600 text-white hover:bg-red-500 focus:ring-red-500': props.variant === 'danger',
  'bg-transparent text-gray-300 hover:bg-gray-800 focus:ring-gray-500': props.variant === 'ghost'
}))

const sizeClasses = computed(() => ({
  'px-2.5 py-1.5 text-sm': props.size === 'sm',
  'px-4 py-2 text-base': props.size === 'md',
  'px-6 py-3 text-lg': props.size === 'lg'
}))
</script>