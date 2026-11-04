<template>
  <div class="min-h-screen bg-[#FAF8F5] dark:bg-dark-950">
    <!-- Apple Spatial Ambient Background Decoration -->
    <div class="pointer-events-none fixed inset-0 overflow-hidden bg-mesh-gradient">
      <div
        class="absolute -right-32 -top-32 h-96 w-96 rounded-full bg-primary-400/12 blur-3xl dark:bg-primary-500/8"
      ></div>
      <div
        class="absolute -bottom-32 left-1/4 h-96 w-96 rounded-full bg-orange-400/10 blur-3xl dark:bg-orange-600/6"
      ></div>
    </div>

    <!-- Sidebar (Floating Spatial Glass Dock) -->
    <AppSidebar />

    <!-- Main Content Area -->
    <div
      class="relative min-h-screen transition-all duration-300"
      :class="[sidebarCollapsed ? 'lg:ml-[96px]' : 'lg:ml-[276px]']"
    >
      <!-- Header (Floating Spatial Glass Island) -->
      <AppHeader />

      <!-- Main Content -->
      <main class="p-4 md:p-6 lg:px-8 lg:py-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import '@/styles/onboarding.css'
import { computed, onMounted } from 'vue'
import { useAppStore } from '@/stores'
import { useAuthStore } from '@/stores/auth'
import { useOnboardingTour } from '@/composables/useOnboardingTour'
import { useOnboardingStore } from '@/stores/onboarding'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'

const appStore = useAppStore()
const authStore = useAuthStore()
const sidebarCollapsed = computed(() => appStore.sidebarCollapsed)
const isAdmin = computed(() => authStore.user?.role === 'admin')

const { replayTour } = useOnboardingTour({
  storageKey: isAdmin.value ? 'admin_guide' : 'user_guide',
  autoStart: false
})

const onboardingStore = useOnboardingStore()

onMounted(() => {
  onboardingStore.setReplayCallback(replayTour)
})

defineExpose({ replayTour })
</script>
