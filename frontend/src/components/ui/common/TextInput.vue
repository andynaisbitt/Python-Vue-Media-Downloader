# frontend/src/components/ui/common/TextInput.vue
<template>
  <div>
    <!-- Label -->
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-300 mb-2"
    >
      {{ label }}
    </label>

    <!-- Input Container -->
    <div class="relative">
      <!-- Leading Icon -->
      <div
        v-if="leadingIcon"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <component
          :is="leadingIcon"
          class="h-5 w-5 text-gray-400"
        />
      </div>

      <!-- Input -->
      <input
        :id="id"
        v-model="innerValue"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :class="[
          'w-full bg-gray-800/50 border border-gray-700 rounded-lg text-white',
          'placeholder-gray-500 focus:outline-none focus:ring-2',
          'focus:ring-purple-500/50 focus:border-purple-500',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          leadingIcon ? 'pl-10' : 'pl-4',
          trailingIcon ? 'pr-10' : 'pr-4',
          'py-2',
          error ? 'border-red-500' : '',
          className
        ]"
        v-bind="$attrs"
      />

      <!-- Trailing Icon -->
      <div
        v-if="trailingIcon"
        class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none"
      >
        <component
          :is="trailingIcon"
          class="h-5 w-5 text-gray-400"
        />
      </div>
    </div>

    <!-- Error Message -->
    <p 
      v-if="error" 
      class="mt-1 text-sm text-red-500"
    >
      {{ error }}
    </p>

    <!-- Help Text -->
    <p 
      v-if="helpText && !error" 
      class="mt-1 text-sm text-gray-400"
    >
      {{ helpText }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  leadingIcon: {
    type: [Object, Function],
    default: null
  },
  trailingIcon: {
    type: [Object, Function],
    default: null
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const innerValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>