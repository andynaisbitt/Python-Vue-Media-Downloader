# frontend/src/components/ui/common/Select.vue
<template>
  <div class="relative">
    <!-- Label -->
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-300 mb-2"
    >
      {{ label }}
    </label>

    <!-- Select Container -->
    <div class="relative">
      <select
        :id="id"
        v-model="innerValue"
        :disabled="disabled"
        class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
        :class="{ 'border-red-500 focus:ring-red-500': error }"
      >
        <!-- Placeholder Option -->
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>

        <!-- Option Groups -->
        <template v-if="hasGroups">
          <optgroup
            v-for="group in options"
            :key="group.label"
            :label="group.label"
          >
            <option
              v-for="option in group.options"
              :key="getOptionValue(option)"
              :value="getOptionValue(option)"
            >
              {{ getOptionLabel(option) }}
            </option>
          </optgroup>
        </template>

        <!-- Regular Options -->
        <template v-else>
          <option
            v-for="option in options"
            :key="getOptionValue(option)"
            :value="getOptionValue(option)"
          >
            {{ getOptionLabel(option) }}
          </option>
        </template>
      </select>

      <!-- Custom Arrow -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
        <ChevronDown class="h-4 w-4 text-gray-400" />
      </div>
    </div>

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-sm text-red-500">{{ error }}</p>

    <!-- Help Text -->
    <p v-else-if="helpText" class="mt-1 text-sm text-gray-400">{{ helpText }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean, Object],
    default: ''
  },
  options: {
    type: Array,
    required: true
  },
  label: {
    type: String,
    default: ''
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
  valueKey: {
    type: String,
    default: 'value'
  },
  labelKey: {
    type: String,
    default: 'label'
  },
  id: {
    type: String,
    default: () => `select-${Math.random().toString(36).substr(2, 9)}`
  }
})

const emit = defineEmits(['update:modelValue'])

// Internal value for v-model
const innerValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Check if options are grouped
const hasGroups = computed(() => {
  return props.options.length > 0 && 'options' in props.options[0]
})

// Helper functions for getting option values and labels
function getOptionValue(option) {
  return typeof option === 'object' ? option[props.valueKey] : option
}

function getOptionLabel(option) {
  return typeof option === 'object' ? option[props.labelKey] : option
}
</script>