<template>
  <div class="min-h-screen bg-gray-950">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-sm border-b border-gray-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <router-link to="/" class="flex items-center">
            <span class="text-2xl font-bold">
              <span class="text-purple-500">You</span>
              <span class="text-white">Tube</span>
            </span>
          </router-link>

          <div class="flex items-center gap-4">
            <router-link 
              to="/download"
              class="text-gray-300 hover:text-white px-3 py-2 rounded-lg text-sm font-medium transition"
              active-class="bg-gray-800"
            >
              Download
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-16">
      <router-view v-slot="{ Component }">
        <transition 
          name="page" 
          mode="out-in"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
