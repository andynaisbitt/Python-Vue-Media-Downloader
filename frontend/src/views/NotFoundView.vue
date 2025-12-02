# frontend/src/views/NotFoundView.vue
<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center">
      <div>
        <h2 class="mt-6 text-3xl font-extrabold text-white">
          404 - Page Not Found
        </h2>
        <p class="mt-2 text-sm text-gray-400">
          The page you're looking for doesn't exist or has been moved.
        </p>
      </div>
      <div class="mt-8">
        <router-link
          to="/"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          Return Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional setup needed
</script>