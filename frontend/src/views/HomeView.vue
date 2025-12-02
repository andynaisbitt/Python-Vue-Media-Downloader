<template>
  <div class="relative overflow-hidden py-16">
    <!-- Background patterns -->
    <div class="absolute inset-0 -z-10 opacity-10">
      <div class="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl">
        <div class="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30"></div>
      </div>
    </div>

    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <!-- Hero Section -->
      <div class="text-center"
        v-motion
        :initial="{ opacity: 0, y: 100 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 800 } }"
      >
        <!-- Version Badge -->
        <div class="mb-6 inline-flex items-center gap-2 px-4 py-2 bg-purple-500/10 border border-purple-500/30 rounded-full">
          <span class="inline-flex h-2 w-2 rounded-full bg-purple-400 animate-pulse"></span>
          <span class="text-sm font-medium text-purple-300">Version 1.0 Released!</span>
        </div>

        <h1 class="text-4xl font-bold tracking-tight sm:text-6xl bg-gradient-to-r from-white via-purple-300 to-white bg-clip-text text-transparent">
          Download YouTube Videos
          <span class="block text-2xl sm:text-4xl mt-4 text-purple-400">Faster & Smarter</span>
        </h1>
        <p class="mt-6 text-lg leading-8 text-gray-400 max-w-3xl mx-auto">
          Experience the next generation of YouTube downloading with beautiful previews, batch support, and real-time progress tracking. Built with modern web technologies for an exceptional user experience.
        </p>
        <div class="mt-10 flex items-center justify-center gap-x-6">
          <router-link
            to="/download"
            class="group relative inline-flex items-center gap-x-2 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-purple-500/25 transition hover:from-purple-500 hover:to-pink-500 hover:shadow-purple-500/50 focus:outline-none focus:ring-2 focus:ring-purple-400/50 focus:ring-offset-2 focus:ring-offset-gray-900"
          >
            Start Downloading
            <Download class="h-5 w-5 transition group-hover:translate-x-1" />
          </router-link>
          <a href="#features" class="text-sm font-semibold leading-6 text-white hover:text-purple-400 transition">
            Learn more <span aria-hidden="true">→</span>
          </a>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="mt-20 grid grid-cols-2 gap-8 md:grid-cols-4"
        v-motion
        :initial="{ opacity: 0, y: 50 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 400 } }"
      >
        <div v-for="stat in stats" :key="stat.label" class="text-center">
          <div class="text-3xl font-bold text-purple-400">{{ stat.value }}</div>
          <div class="mt-2 text-sm text-gray-400">{{ stat.label }}</div>
        </div>
      </div>

      <!-- Features -->
      <div id="features" class="mt-32">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
          <div class="mx-auto max-w-2xl text-center">
            <h2 class="text-base font-semibold leading-7 text-purple-400">Powerful Features</h2>
            <p class="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">Everything you need</p>
            <p class="mt-6 text-lg leading-8 text-gray-400">
              The most comprehensive YouTube downloader with cutting-edge v1.0 features.
            </p>
          </div>
          <div class="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl class="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              <div v-for="(feature, idx) in features" :key="feature.name"
                v-motion
                :initial="{ opacity: 0, y: 50 }"
                :enter="{ opacity: 1, y: 0, transition: { delay: 200 * idx } }"
                class="group relative bg-gray-900/50 backdrop-blur-sm p-8 rounded-2xl border border-gray-800 hover:border-purple-500/50 transition duration-300"
              >
                <dt class="text-base font-semibold leading-7 text-white">
                  <div class="absolute left-4 top-4 flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 group-hover:from-purple-500 group-hover:to-pink-500 transition">
                    <component :is="feature.icon" class="h-6 w-6 text-white" aria-hidden="true" />
                  </div>
                  <div class="ml-16">{{ feature.name }}</div>
                </dt>
                <dd class="mt-2 ml-16 text-base leading-7 text-gray-400">{{ feature.description }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      <!-- Tech Stack Section -->
      <div class="mt-32">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
          <div class="mx-auto max-w-2xl text-center">
            <h2 class="text-base font-semibold leading-7 text-purple-400">Built With Modern Tech</h2>
            <p class="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">Powerful Stack</p>
            <p class="mt-6 text-lg leading-8 text-gray-400">
              Leveraging the best technologies for performance, reliability, and user experience.
            </p>
          </div>

          <div class="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <!-- Frontend Technologies -->
            <div class="bg-gray-900/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-800">
              <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Code class="w-5 h-5 text-purple-400" />
                Frontend
              </h3>
              <div class="space-y-3">
                <div v-for="tech in frontendTech" :key="tech.name" class="flex items-center gap-3">
                  <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-gray-800">
                    <component :is="tech.icon" class="h-4 w-4 text-purple-400" />
                  </div>
                  <div>
                    <div class="text-sm font-medium text-white">{{ tech.name }}</div>
                    <div class="text-xs text-gray-500">{{ tech.version }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Backend Technologies -->
            <div class="bg-gray-900/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-800">
              <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Server class="w-5 h-5 text-pink-400" />
                Backend
              </h3>
              <div class="space-y-3">
                <div v-for="tech in backendTech" :key="tech.name" class="flex items-center gap-3">
                  <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-gray-800">
                    <component :is="tech.icon" class="h-4 w-4 text-pink-400" />
                  </div>
                  <div>
                    <div class="text-sm font-medium text-white">{{ tech.name }}</div>
                    <div class="text-xs text-gray-500">{{ tech.version }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tools & Libraries -->
            <div class="bg-gray-900/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-800">
              <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Package class="w-5 h-5 text-blue-400" />
                Tools
              </h3>
              <div class="space-y-3">
                <div v-for="tech in toolsTech" :key="tech.name" class="flex items-center gap-3">
                  <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-gray-800">
                    <component :is="tech.icon" class="h-4 w-4 text-blue-400" />
                  </div>
                  <div>
                    <div class="text-sm font-medium text-white">{{ tech.name }}</div>
                    <div class="text-xs text-gray-500">{{ tech.version }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="mt-32 mb-16">
        <div class="relative isolate overflow-hidden bg-gray-900/50 backdrop-blur-sm px-6 py-24 text-center border border-gray-800 rounded-3xl sm:px-16">
          <h2 class="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Ready to start downloading?
          </h2>
          <p class="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-400">
            Experience the smoothest YouTube downloading experience with preview modals, batch support, and real-time progress tracking.
          </p>
          <div class="mt-10 flex items-center justify-center gap-x-6">
            <router-link
              to="/download"
              class="inline-flex items-center gap-x-2 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-purple-500/25 transition hover:from-purple-500 hover:to-pink-500"
            >
              Get Started Now
              <ArrowRight class="h-5 w-5" />
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Download, Video, AudioLines, Settings, Subtitles, Share2, Eye, Zap, CheckCircle, Package, Code, Server, ArrowRight } from 'lucide-vue-next'

const stats = [
  { value: '6+', label: 'Video Formats' },
  { value: '3+', label: 'Audio Formats' },
  { value: 'Unlimited', label: 'Downloads' },
  { value: '100%', label: 'Free & Open' }
]

const features = [
  {
    name: 'Video Preview',
    description: 'See thumbnail, title, and details before downloading. Beautiful preview modal with all video information.',
    icon: Eye
  },
  {
    name: 'Batch Downloads',
    description: 'Paste multiple URLs at once and download them sequentially with smart queue management.',
    icon: Share2
  },
  {
    name: 'Real-Time Progress',
    description: 'Live speed, ETA, and byte-level tracking with gradient progress bars and smooth animations.',
    icon: Zap
  },
  {
    name: 'Multiple Formats',
    description: 'Download videos in MP4, AVI, MKV, or extract audio in MP3, AAC, WAV with quality presets.',
    icon: Video
  },
  {
    name: 'Completion Notifications',
    description: 'Beautiful success modals with animated checkmarks and quick download buttons. No more guessing!',
    icon: CheckCircle
  },
  {
    name: 'Advanced Options',
    description: 'Subtitle download, time ranges, network settings, and AI-powered transcription support.',
    icon: Settings
  }
]

const frontendTech = [
  { name: 'Vue.js', version: '3.x', icon: Code },
  { name: 'Vite', version: '5.x', icon: Zap },
  { name: 'Tailwind CSS', version: '3.x', icon: Package },
  { name: 'Pinia', version: '2.x', icon: Package }
]

const backendTech = [
  { name: 'Python', version: '3.8+', icon: Server },
  { name: 'Flask', version: '3.x', icon: Server },
  { name: 'yt-dlp', version: 'Latest', icon: Download }
]

const toolsTech = [
  { name: 'FFmpeg', version: 'Latest', icon: Video },
  { name: 'Axios', version: '1.x', icon: Package },
  { name: 'Lucide Icons', version: 'Latest', icon: Package }
]
</script>
