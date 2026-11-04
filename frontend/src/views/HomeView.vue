<template>
  <!-- Custom Home Content: Full Page Mode -->
  <div v-if="hasHomeContent" class="min-h-screen">
    <!-- iframe mode -->
    <iframe
      v-if="isHomeContentUrl"
      :src="homeContent.trim()"
      class="h-screen w-full border-0"
      referrerpolicy="no-referrer"
      allowfullscreen
    ></iframe>
    <!-- HTML mode - SECURITY: sanitized with DOMPurify to prevent stored XSS -->
    <div v-else v-html="sanitizedHomeContent"></div>
  </div>

  <!-- Compact Home Page (Apple Glassmorphic Minimal Mode) -->
  <div
    v-else-if="compactHomeEnabled"
    data-testid="compact-home"
    class="relative flex min-h-screen flex-col overflow-hidden bg-gradient-to-br from-[#FAF8F5] via-primary-50/35 to-[#F3EFEA] text-gray-900 dark:from-dark-950 dark:via-dark-900 dark:to-dark-950 dark:text-white"
  >
    <!-- Ambient Orbs -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div class="absolute -right-32 -top-32 h-96 w-96 rounded-full bg-primary-400/20 blur-3xl dark:bg-primary-500/12"></div>
      <div class="absolute -bottom-32 -left-32 h-96 w-96 rounded-full bg-orange-400/15 blur-3xl dark:bg-orange-600/10"></div>
    </div>

    <header class="relative z-20 border-b border-white/70 bg-white/65 px-4 py-4 backdrop-blur-2xl sm:px-6 dark:border-white/[0.07] dark:bg-dark-900/65">
      <nav class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 sm:gap-4">
        <div class="flex min-w-0 flex-1 items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-[14px] bg-white/80 p-0.5 shadow-glow ring-1 ring-primary-500/20 dark:bg-dark-800/80 dark:ring-white/10">
            <img
              :src="siteLogo || '/logo.svg'"
              alt="Logo"
              class="h-full w-full rounded-[12px] object-contain"
            />
          </div>
          <span class="min-w-0 truncate text-base font-bold tracking-tight">{{ siteName }}</span>
        </div>
        <div class="flex max-w-full shrink-0 flex-wrap items-center justify-end gap-2">
          <LocaleSwitcher />
          <router-link
            v-if="showModelPlazaEntry"
            to="/model-plaza"
            class="flex h-10 shrink-0 items-center gap-1.5 rounded-xl px-3 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-200/50 hover:text-gray-900 dark:text-dark-300 dark:hover:bg-white/[0.06] dark:hover:text-white"
            :title="t('nav.modelPlaza')"
          >
            <Icon name="grid" size="md" />
            <span class="hidden sm:inline">{{ t('nav.modelPlaza') }}</span>
          </router-link>
          <button
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-gray-500 transition-colors hover:bg-gray-200/50 dark:text-dark-400 dark:hover:bg-white/[0.06]"
            :title="isDark ? t('home.switchToLight') : t('home.switchToDark')"
            @click="toggleTheme"
          >
            <Icon v-if="isDark" name="sun" size="md" />
            <Icon v-else name="moon" size="md" />
          </button>
          <router-link
            :to="isAuthenticated ? dashboardPath : '/login'"
            class="btn btn-primary min-h-10 shrink-0 rounded-2xl px-4 py-2 text-sm font-semibold"
          >
            {{ isAuthenticated ? t('home.dashboard') : t('home.login') }}
          </router-link>
        </div>
      </nav>
    </header>

    <main class="relative z-10 flex min-w-0 flex-1 items-center justify-center px-4 py-16 sm:px-6">
      <div class="card-glass min-w-0 max-w-xl rounded-3xl p-10 text-center shadow-glass sm:p-12">
        <div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center overflow-hidden rounded-[24px] bg-white/80 p-1 shadow-xl shadow-primary-500/25 ring-1 ring-white/80 dark:bg-dark-800/80 dark:ring-white/15">
          <img
            :src="siteLogo || '/logo.svg'"
            alt="Logo"
            class="h-full w-full rounded-[20px] object-contain"
          />
        </div>
        <h1 class="[overflow-wrap:anywhere] text-3xl font-bold tracking-tight md:text-4xl">{{ siteName }}</h1>
        <p class="mt-4 whitespace-pre-wrap [overflow-wrap:anywhere] text-base text-gray-600 dark:text-dark-300">{{ siteSubtitle }}</p>
        <router-link
          :to="isAuthenticated ? dashboardPath : '/login'"
          class="btn btn-primary mt-8 inline-flex min-h-11 items-center justify-center rounded-2xl px-7 py-3 text-sm font-semibold"
        >
          {{ isAuthenticated ? t('home.goToDashboard') : t('home.login') }}
        </router-link>
      </div>
    </main>

    <footer class="relative z-10 min-w-0 border-t border-white/60 px-4 py-5 text-center text-sm text-gray-500 [overflow-wrap:anywhere] sm:px-6 dark:border-white/[0.06] dark:text-dark-400">
      &copy; {{ currentYear }} {{ siteName }}
    </footer>
  </div>

  <!-- Default Home Page (Apple Spatial Glassmorphism + Warm Amber/Gold) -->
  <div
    v-else
    class="relative flex min-h-screen flex-col overflow-hidden bg-gradient-to-br from-[#FAF8F5] via-primary-50/35 to-[#F3EFEA] dark:from-dark-950 dark:via-dark-900 dark:to-dark-950"
  >
    <!-- Background Spatial Decorations -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div
        class="absolute -right-36 -top-36 h-[28rem] w-[28rem] rounded-full bg-primary-400/25 blur-3xl dark:bg-primary-500/15"
      ></div>
      <div
        class="absolute -bottom-36 -left-36 h-[28rem] w-[28rem] rounded-full bg-orange-500/18 blur-3xl dark:bg-orange-600/12"
      ></div>
      <div
        class="absolute left-1/3 top-1/4 h-80 w-80 rounded-full bg-amber-300/15 blur-3xl dark:bg-amber-500/10"
      ></div>
      <div
        class="absolute bottom-1/4 right-1/4 h-72 w-72 rounded-full bg-primary-400/12 blur-3xl"
      ></div>
      <div
        class="absolute inset-0 bg-[linear-gradient(rgba(245,158,11,0.035)_1px,transparent_1px),linear-gradient(90deg,rgba(245,158,11,0.035)_1px,transparent_1px)] bg-[size:64px_64px]"
      ></div>
    </div>

    <!-- Top Floating Spatial Glass Island Navbar -->
    <header class="relative z-20 px-4 pt-5 sm:px-6">
      <nav
        class="mx-auto flex max-w-6xl items-center justify-between rounded-3xl border border-white/80 bg-white/70 px-5 py-3 shadow-glass backdrop-blur-2xl dark:border-white/[0.08] dark:bg-dark-900/70"
      >
        <!-- Brand Logo & Name -->
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center overflow-hidden rounded-[14px] bg-white/90 p-0.5 shadow-glow ring-1 ring-primary-500/25 dark:bg-dark-800/90 dark:ring-white/15">
            <img :src="siteLogo || '/logo.svg'" alt="Logo" class="h-full w-full rounded-[12px] object-contain" />
          </div>
          <div class="flex items-center gap-2.5">
            <span class="text-lg font-bold tracking-tight text-gray-900 dark:text-white">
              {{ siteName }}
            </span>
            <span
              class="hidden rounded-full bg-amber-500/10 px-2.5 py-0.5 text-[11px] font-semibold text-amber-700 ring-1 ring-amber-500/20 sm:inline-block dark:bg-amber-500/15 dark:text-amber-300"
            >
              AI Gateway
            </span>
          </div>
        </div>

        <!-- Nav Actions -->
        <div class="flex items-center gap-2 sm:gap-3">
          <!-- Key Usage Quick Check -->
          <router-link
            to="/key-usage"
            class="inline-flex items-center gap-1.5 rounded-xl px-3 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-200/50 hover:text-gray-900 dark:text-dark-300 dark:hover:bg-white/[0.06] dark:hover:text-white"
          >
            <Icon name="key" size="sm" class="text-amber-500" />
            <span class="hidden sm:inline">{{ t('keyUsage.title') }}</span>
          </router-link>

          <!-- Model Plaza Link -->
          <router-link
            v-if="showModelPlazaEntry"
            to="/model-plaza"
            class="inline-flex items-center gap-1.5 rounded-xl px-3 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-200/50 hover:text-gray-900 dark:text-dark-300 dark:hover:bg-white/[0.06] dark:hover:text-white"
            :title="t('nav.modelPlaza')"
          >
            <Icon name="grid" size="md" />
            <span class="hidden sm:inline">{{ t('nav.modelPlaza') }}</span>
          </router-link>

          <!-- Language Switcher -->
          <LocaleSwitcher />

          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="rounded-xl p-2 text-gray-500 transition-colors hover:bg-gray-200/50 hover:text-gray-800 dark:text-dark-300 dark:hover:bg-white/[0.06] dark:hover:text-white"
            :title="isDark ? t('home.switchToLight') : t('home.switchToDark')"
          >
            <Icon v-if="isDark" name="sun" size="md" />
            <Icon v-else name="moon" size="md" />
          </button>

          <!-- Login / Dashboard Button -->
          <router-link
            v-if="isAuthenticated"
            :to="dashboardPath"
            class="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 py-1.5 pl-1.5 pr-3.5 text-white shadow-md shadow-primary-500/25 transition-all hover:shadow-lg hover:shadow-primary-500/35"
          >
            <span
              class="flex h-6 w-6 items-center justify-center rounded-full bg-white/20 text-xs font-bold text-white backdrop-blur-sm"
            >
              {{ userInitial }}
            </span>
            <span class="text-xs font-semibold text-white">{{ t('home.dashboard') }}</span>
          </router-link>
          <router-link
            v-else
            to="/login"
            class="inline-flex items-center rounded-full bg-gradient-to-r from-primary-500 to-primary-600 px-4 py-1.5 text-xs font-semibold text-white shadow-md shadow-primary-500/25 transition-all hover:shadow-lg hover:shadow-primary-500/35"
          >
            {{ t('home.login') }}
          </router-link>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 flex-1 px-6 py-10 sm:py-14">
      <!-- VisionOS 居中空间画廊 + Bento 便当盒展示 -->
      <div class="mx-auto max-w-6xl space-y-10">
        <!-- Centered Spatial Hero Header -->
        <div class="mx-auto max-w-3xl text-center">
          <div
            class="mb-4 inline-flex items-center gap-2 rounded-full border border-primary-300/60 bg-white/80 px-4 py-1.5 text-xs font-semibold text-primary-700 shadow-sm backdrop-blur-xl dark:border-primary-500/30 dark:bg-dark-800/80 dark:text-primary-300"
          >
            <span class="h-2 w-2 rounded-full bg-primary-500 animate-pulse"></span>
            <span>{{ siteName }} • Next-Gen AI Agent Gateway</span>
          </div>

          <h1
            class="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-5xl lg:text-6xl"
          >
            <span class="bg-gradient-to-r from-gray-900 via-gray-800 to-primary-600 bg-clip-text text-transparent dark:from-white dark:via-amber-100 dark:to-primary-400">
              {{ siteName }}
            </span>
          </h1>
          <p class="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-gray-600 dark:text-dark-300 sm:text-lg">
            {{ siteSubtitle }}
          </p>

          <!-- Centered Action Buttons -->
          <div class="mt-7 flex flex-wrap items-center justify-center gap-3.5">
            <router-link
              :to="isAuthenticated ? dashboardPath : '/login'"
              class="btn btn-primary rounded-2xl px-8 py-3.5 text-sm font-semibold shadow-xl shadow-primary-500/30"
            >
              {{ isAuthenticated ? t('home.goToDashboard') : t('home.getStarted') }}
              <Icon name="arrowRight" size="sm" class="ml-1.5" :stroke-width="2" />
            </router-link>
            <router-link
              to="/key-usage"
              class="btn btn-secondary rounded-2xl px-6 py-3.5 text-sm font-semibold"
            >
              <Icon name="key" size="sm" class="mr-1.5 text-amber-500" />
              {{ t('keyUsage.title') }}
            </router-link>
          </div>
        </div>

        <!-- Bento Showcase Grid (7 Cols Terminal + Providers | 5 Cols Core Capabilities) -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <!-- Left 7 Cols: Obsidian-Amber Terminal Bento Card -->
          <div
            class="relative flex flex-col justify-between overflow-hidden rounded-3xl border border-white/80 bg-white/70 p-6 shadow-glass backdrop-blur-2xl lg:col-span-7 sm:p-8 dark:border-white/10 dark:bg-dark-800/70"
          >
            <div class="mb-6 flex flex-wrap items-center justify-between gap-2">
              <div>
                <span class="text-xs font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400">
                  Unified Endpoint
                </span>
                <h2 class="mt-0.5 text-lg font-bold text-gray-900 dark:text-white">
                  {{ t('home.features.unifiedGateway') }}
                </h2>
              </div>
              <div class="flex flex-wrap gap-1.5">
                <span class="rounded-full bg-amber-500/10 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:bg-amber-500/15 dark:text-amber-300">
                  {{ t('home.tags.subscriptionToApi') }}
                </span>
                <span class="rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300">
                  {{ t('home.tags.stickySession') }}
                </span>
              </div>
            </div>

            <!-- Centered Terminal Inside Bento -->
            <div class="flex justify-center py-2">
              <div class="terminal-container w-full max-w-[460px]">
                <div class="terminal-window !w-full">
                  <div class="terminal-header">
                    <div class="terminal-buttons">
                      <span class="btn-close"></span>
                      <span class="btn-minimize"></span>
                      <span class="btn-maximize"></span>
                    </div>
                    <span class="terminal-title">agentbyte — gateway</span>
                  </div>
                  <div class="terminal-body">
                    <div class="code-line line-1">
                      <span class="code-prompt">$</span>
                      <span class="code-cmd">curl</span>
                      <span class="code-flag">-X POST</span>
                      <span class="code-url">/v1/messages</span>
                    </div>
                    <div class="code-line line-2">
                      <span class="code-comment"># AgentByte intelligent routing...</span>
                    </div>
                    <div class="code-line line-3">
                      <span class="code-success">200 OK</span>
                      <span class="code-response">{ "agent": "AgentByte", "status": "ready" }</span>
                    </div>
                    <div class="code-line line-4">
                      <span class="code-prompt">$</span>
                      <span class="cursor"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Supported Models Strip inside Bento -->
            <div class="mt-6 flex flex-wrap items-center justify-between gap-2 border-t border-black/[0.05] pt-4 dark:border-white/[0.06]">
              <span class="text-xs font-semibold text-gray-500 dark:text-dark-400">
                {{ t('home.providers.title') }}
              </span>
              <div class="flex flex-wrap items-center gap-2">
                <span class="inline-flex items-center gap-1.5 rounded-xl bg-orange-500/10 px-2.5 py-1 text-xs font-semibold text-orange-700 dark:text-orange-300">
                  <span class="h-2 w-2 rounded-full bg-orange-500"></span>{{ t('home.providers.claude') }}
                </span>
                <span class="inline-flex items-center gap-1.5 rounded-xl bg-emerald-500/10 px-2.5 py-1 text-xs font-semibold text-emerald-700 dark:text-emerald-300">
                  <span class="h-2 w-2 rounded-full bg-emerald-500"></span>GPT
                </span>
                <span class="inline-flex items-center gap-1.5 rounded-xl bg-amber-500/10 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:text-amber-300">
                  <span class="h-2 w-2 rounded-full bg-amber-500"></span>{{ t('home.providers.gemini') }}
                </span>
                <span class="inline-flex items-center gap-1.5 rounded-xl bg-rose-500/10 px-2.5 py-1 text-xs font-semibold text-rose-700 dark:text-rose-300">
                  <span class="h-2 w-2 rounded-full bg-rose-500"></span>{{ t('home.providers.antigravity') }}
                </span>
              </div>
            </div>
          </div>

          <!-- Right 5 Cols: 2 Stacked Capability Bento Cards -->
          <div class="flex flex-col gap-6 lg:col-span-5">
            <!-- Bento Right Top: Multi-Account Intelligent Pool -->
            <div
              class="flex flex-1 flex-col justify-between rounded-3xl border border-white/80 bg-white/70 p-6 shadow-glass backdrop-blur-2xl sm:p-7 dark:border-white/10 dark:bg-dark-800/70"
            >
              <div>
                <div
                  class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-lg shadow-primary-500/25"
                >
                  <Icon name="server" size="md" :stroke-width="2" />
                </div>
                <h3 class="text-lg font-bold tracking-tight text-gray-900 dark:text-white">
                  {{ t('home.features.multiAccount') }}
                </h3>
                <p class="mt-2 text-sm leading-relaxed text-gray-600 dark:text-dark-400">
                  {{ t('home.features.multiAccountDesc') }}
                </p>
              </div>
              <div class="mt-5 flex items-center gap-2 text-xs font-semibold text-amber-600 dark:text-amber-400">
                <Icon name="shield" size="sm" />
                <span>{{ t('home.tags.stickySession') }} · 自动负载均衡容灾</span>
              </div>
            </div>

            <!-- Bento Right Bottom: Real-Time Billing & Quota -->
            <div
              class="flex flex-1 flex-col justify-between rounded-3xl border border-white/80 bg-white/70 p-6 shadow-glass backdrop-blur-2xl sm:p-7 dark:border-white/10 dark:bg-dark-800/70"
            >
              <div>
                <div
                  class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-500 to-red-500 text-white shadow-lg shadow-orange-500/25"
                >
                  <Icon name="chart" size="md" :stroke-width="2" />
                </div>
                <h3 class="text-lg font-bold tracking-tight text-gray-900 dark:text-white">
                  {{ t('home.features.balanceQuota') }}
                </h3>
                <p class="mt-2 text-sm leading-relaxed text-gray-600 dark:text-dark-400">
                  {{ t('home.features.balanceQuotaDesc') }}
                </p>
              </div>
              <div class="mt-5 flex items-center gap-2 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                <Icon name="bolt" size="sm" />
                <span>{{ t('home.tags.realtimeBilling') }} · Token 级透明审计</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 border-t border-white/60 bg-white/40 px-6 py-8 backdrop-blur-xl dark:border-white/[0.06] dark:bg-dark-900/40">
      <div
        class="mx-auto flex max-w-6xl items-center justify-center text-center"
      >
        <p class="text-sm text-gray-500 dark:text-dark-400">
          &copy; {{ currentYear }} {{ siteName }}. {{ t('home.footer.allRightsReserved') }}
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore, useAppStore } from '@/stores'
import LocaleSwitcher from '@/components/common/LocaleSwitcher.vue'
import Icon from '@/components/icons/Icon.vue'
import { resolveBrandName } from '@/utils/branding'
import { sanitizeUrl } from '@/utils/url'
import DOMPurify from 'dompurify'
import { FeatureFlags, isFeatureFlagEnabled } from '@/utils/featureFlags'

const { t } = useI18n()

const authStore = useAuthStore()
const appStore = useAppStore()

// Site settings - directly from appStore (already initialized from injected config)
const siteName = computed(() =>
  resolveBrandName(appStore.cachedPublicSettings?.site_name || appStore.siteName)
)
const siteLogo = computed(() => sanitizeUrl(appStore.cachedPublicSettings?.site_logo || appStore.siteLogo || '', { allowRelative: true, allowDataUrl: true }))
const siteSubtitle = computed(() => appStore.cachedPublicSettings?.site_subtitle || 'Intelligent AI Agent & API Gateway Platform')
const docUrl = computed(() => sanitizeUrl(appStore.cachedPublicSettings?.doc_url || appStore.docUrl || ''))
void docUrl.value
const homeContent = computed(() => appStore.cachedPublicSettings?.home_content || '')
const sanitizedHomeContent = computed(() => DOMPurify.sanitize(homeContent.value))
const hasHomeContent = computed(() => homeContent.value.trim().length > 0)
const compactHomeEnabled = computed(() => appStore.cachedPublicSettings?.compact_home_enabled === true)
const modelPlazaEnabled = computed(() => isFeatureFlagEnabled(FeatureFlags.modelPlaza))

// Check if homeContent is a URL (for iframe display)
const isHomeContentUrl = computed(() => {
  const content = homeContent.value.trim()
  return content.startsWith('http://') || content.startsWith('https://')
})

// Theme
const isDark = ref(document.documentElement.classList.contains('dark'))

// Auth state
const isAuthenticated = computed(() => authStore.isAuthenticated)
const modelPlazaRequiresAuth = computed(
  () => appStore.cachedPublicSettings?.model_plaza_require_auth === true,
)
const showModelPlazaEntry = computed(
  () => modelPlazaEnabled.value && (isAuthenticated.value || !modelPlazaRequiresAuth.value),
)
const isAdmin = computed(() => authStore.isAdmin)
const dashboardPath = computed(() => isAdmin.value ? '/admin/dashboard' : '/dashboard')
const userInitial = computed(() => {
  const user = authStore.user
  if (!user || !user.email) return ''
  return user.email.charAt(0).toUpperCase()
})

// Current year for footer
const currentYear = computed(() => new Date().getFullYear())

// Toggle theme
function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Initialize theme
function initTheme() {
  const savedTheme = localStorage.getItem('theme')
  if (
    savedTheme === 'dark' ||
    (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)
  ) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
}

onMounted(() => {
  initTheme()

  // Check auth state
  authStore.checkAuth()

  // Ensure public settings are loaded (will use cache if already loaded from injected config)
  if (!appStore.publicSettingsLoaded) {
    appStore.fetchPublicSettings()
  }
})
</script>

<style scoped>
/* Terminal Container */
.terminal-container {
  position: relative;
  display: inline-block;
}

/* Terminal Window - Apple Spatial Dark Glass */
.terminal-window {
  width: 430px;
  max-width: 92vw;
  background: linear-gradient(145deg, rgba(33, 27, 22, 0.94) 0%, rgba(18, 14, 11, 0.97) 100%);
  backdrop-filter: blur(24px);
  border-radius: 22px;
  box-shadow:
    0 28px 60px -12px rgba(15, 10, 5, 0.45),
    0 0 0 1px rgba(251, 191, 36, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.14);
  overflow: hidden;
  transform: perspective(1000px) rotateX(2deg) rotateY(-2deg);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease;
}

.terminal-window:hover {
  transform: perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(-5px);
  box-shadow:
    0 32px 64px -12px rgba(245, 158, 11, 0.25),
    0 0 0 1px rgba(245, 158, 11, 0.32),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Terminal Header */
.terminal-header {
  display: flex;
  align-items: center;
  padding: 13px 18px;
  background: rgba(42, 34, 28, 0.75);
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.terminal-buttons {
  display: flex;
  gap: 8px;
}

.terminal-buttons span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.btn-close {
  background: #ff5f56;
}
.btn-minimize {
  background: #ffbd2e;
}
.btn-maximize {
  background: #27c93f;
}

.terminal-title {
  flex: 1;
  text-align: center;
  font-size: 12px;
  font-family: ui-monospace, monospace;
  color: #a8a29e;
  margin-right: 52px;
}

/* Terminal Body */
.terminal-body {
  padding: 22px 26px;
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 14px;
  line-height: 2;
}

.code-line {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  opacity: 0;
  animation: line-appear 0.5s ease forwards;
}

.line-1 {
  animation-delay: 0.3s;
}
.line-2 {
  animation-delay: 1s;
}
.line-3 {
  animation-delay: 1.8s;
}
.line-4 {
  animation-delay: 2.5s;
}

@keyframes line-appear {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.code-prompt {
  color: #f59e0b;
  font-weight: bold;
}
.code-cmd {
  color: #fde68a;
}
.code-flag {
  color: #fb923c;
}
.code-url {
  color: #fbbf24;
}
.code-comment {
  color: #78716c;
  font-style: italic;
}
.code-success {
  color: #fbbf24;
  background: rgba(245, 158, 11, 0.18);
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 600;
}
.code-response {
  color: #fef3c7;
}

/* Blinking Cursor */
.cursor {
  display: inline-block;
  width: 8px;
  height: 16px;
  background: #f59e0b;
  border-radius: 2px;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}

/* Dark mode adjustments */
:deep(.dark) .terminal-window {
  box-shadow:
    0 28px 60px -12px rgba(0, 0, 0, 0.65),
    0 0 0 1px rgba(245, 158, 11, 0.25),
    0 0 44px rgba(245, 158, 11, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
}
</style>
