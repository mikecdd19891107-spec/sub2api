<template>
  <!-- VisionOS 悬浮双栏玻璃画廊卡片 -->
  <div
    class="relative flex min-h-screen items-center justify-center overflow-hidden p-4 sm:p-6"
  >
    <!-- Background -->
    <div
      class="absolute inset-0 bg-gradient-to-br from-[#FAF8F5] via-primary-50/40 to-[#F3EFEA] dark:from-dark-950 dark:via-dark-900 dark:to-dark-950"
    ></div>

    <!-- Decorative Apple Spatial Glass Orbs & Grid -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div
        class="absolute -right-36 -top-36 h-96 w-96 rounded-full bg-primary-400/25 blur-3xl dark:bg-primary-500/15"
      ></div>
      <div
        class="absolute -bottom-36 -left-36 h-96 w-96 rounded-full bg-orange-500/15 blur-3xl dark:bg-orange-600/12"
      ></div>
      <div
        class="absolute inset-0 bg-[linear-gradient(rgba(245,158,11,0.035)_1px,transparent_1px),linear-gradient(90deg,rgba(245,158,11,0.035)_1px,transparent_1px)] bg-[size:64px_64px]"
      ></div>
    </div>

    <!-- Wide Dual-Column Spatial Glass Gallery Card -->
    <div
      class="relative z-10 grid w-full max-w-4xl grid-cols-1 overflow-hidden rounded-3xl border border-white/80 bg-white/75 shadow-glass backdrop-blur-2xl lg:grid-cols-12 dark:border-white/10 dark:bg-dark-900/80"
    >
      <!-- Left 5 Cols: Warm Obsidian-Amber Brand Showcase Panel -->
      <div
        class="relative flex flex-col justify-between overflow-hidden bg-gradient-to-br from-dark-900 via-dark-800 to-dark-950 p-8 text-white lg:col-span-5"
      >
        <div class="pointer-events-none absolute -right-12 -top-12 h-44 w-44 rounded-full bg-amber-500/25 blur-3xl"></div>
        <div class="pointer-events-none absolute -bottom-12 -left-12 h-40 w-40 rounded-full bg-orange-500/20 blur-3xl"></div>

        <div class="relative z-10">
          <router-link to="/home" class="inline-flex items-center gap-3 group">
            <div
              class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-2xl bg-white/95 p-0.5 shadow-lg shadow-amber-500/25 ring-1 ring-white/80 transition-transform group-hover:scale-105"
            >
              <img :src="siteLogo || '/logo.svg'" alt="Logo" class="h-full w-full rounded-[14px] object-contain" />
            </div>
            <div>
              <span class="block text-xl font-extrabold tracking-tight text-white">{{ siteName }}</span>
              <span class="block text-[11px] font-medium text-amber-300/90">AI Agent Gateway</span>
            </div>
          </router-link>

          <div v-if="settingsLoaded" class="mt-8">
            <h2 class="text-2xl font-extrabold leading-snug tracking-tight text-white">
              统一智能路由，<br />
              <span class="bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">
                极速连接全球模型
              </span>
            </h2>
            <p class="mt-3 text-xs leading-relaxed text-gray-300/85">
              {{ siteSubtitle }}
            </p>
          </div>
        </div>

        <!-- Bottom Feature Highlights -->
        <div class="relative z-10 mt-8 space-y-2.5 border-t border-white/10 pt-5 text-xs text-gray-300">
          <div class="flex items-center gap-2">
            <span class="h-1.5 w-1.5 rounded-full bg-amber-400"></span>
            <span>多模态主流模型统一密钥接入</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="h-1.5 w-1.5 rounded-full bg-orange-400"></span>
            <span>高并发智能负载均衡与粘性会话</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
            <span>Token 级实时精细化账单与配额</span>
          </div>
        </div>
      </div>

      <!-- Right 7 Cols: Frosted Glass Auth Form Studio -->
      <div class="flex flex-col justify-between p-7 sm:p-10 lg:col-span-7">
        <div>
          <slot />
        </div>

        <div class="mt-6 space-y-4">
          <div class="text-center text-sm">
            <slot name="footer" />
          </div>
          <div class="text-center text-xs text-gray-400 dark:text-dark-500">
            &copy; {{ currentYear }} {{ siteName }}. All rights reserved.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAppStore } from '@/stores'
import { resolveBrandName } from '@/utils/branding'
import { sanitizeUrl } from '@/utils/url'

const appStore = useAppStore()

const siteName = computed(() => resolveBrandName(appStore.siteName))
const siteLogo = computed(() => sanitizeUrl(appStore.siteLogo || '', { allowRelative: true, allowDataUrl: true }))
const siteSubtitle = computed(() => appStore.cachedPublicSettings?.site_subtitle || 'Intelligent AI Agent & API Gateway')
const settingsLoaded = computed(() => appStore.publicSettingsLoaded)

const currentYear = computed(() => new Date().getFullYear())

onMounted(() => {
  appStore.fetchPublicSettings()
})
</script>

<style scoped>
.text-gradient {
  @apply bg-gradient-to-r from-primary-600 via-primary-500 to-amber-500 bg-clip-text text-transparent dark:from-amber-300 dark:via-primary-400 dark:to-orange-400;
}
</style>
