<template>
  <header
    class="glass sticky top-0 z-30 border-b border-white/75 dark:border-white/[0.07]"
  >
    <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3.5 sm:px-6">
      <!-- 左:站点 logo + 名称 -->
      <div class="flex min-w-0 items-center gap-3">
        <template v-if="settings">
          <span
            class="flex h-10 w-10 flex-shrink-0 items-center justify-center overflow-hidden rounded-[14px] bg-white/90 p-0.5 shadow-glow ring-1 ring-primary-500/20 dark:bg-dark-800/90 dark:ring-white/15"
          >
            <img :src="siteLogo || '/logo.svg'" alt="Logo" class="h-full w-full rounded-[12px] object-contain" />
          </span>
          <span class="truncate text-base font-bold tracking-tight text-gray-950 dark:text-white">
            {{ siteName }}
          </span>
        </template>
        <template v-else>
          <span class="h-10 w-10 flex-shrink-0 animate-pulse rounded-[14px] bg-gray-200 dark:bg-dark-700" aria-hidden="true"></span>
          <span class="h-5 w-28 animate-pulse rounded bg-gray-200 dark:bg-dark-700" aria-hidden="true"></span>
        </template>
      </div>

      <!-- 右:登录 / 回到后台 -->
      <RouterLink
        v-if="isAuthenticated"
        :to="backTarget"
        class="btn btn-primary flex-shrink-0 rounded-2xl px-4 py-2 text-sm font-semibold"
      >
        {{ t('modelPlaza.nav.backToDashboard') }}
      </RouterLink>
      <RouterLink
        v-else
        :to="{ path: '/login', query: { redirect: '/model-plaza' } }"
        class="btn btn-primary flex-shrink-0 rounded-2xl px-4 py-2 text-sm font-semibold"
      >
        {{ t('modelPlaza.nav.login') }}
      </RouterLink>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { resolveBrandName } from '@/utils/branding'
import { sanitizeUrl } from '@/utils/url'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const appStore = useAppStore()
const authStore = useAuthStore()

const settings = computed(() => appStore.cachedPublicSettings)
const siteName = computed(() => resolveBrandName(settings.value?.site_name))
const siteLogo = computed(() =>
  sanitizeUrl(settings.value?.site_logo || '', { allowRelative: true, allowDataUrl: true })
)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const backTarget = computed(() => (authStore.isAdmin ? '/admin/dashboard' : '/dashboard'))
</script>
