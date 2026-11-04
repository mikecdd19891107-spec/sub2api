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

  <!-- Compact Home Page -->
  <div
    v-else-if="compactHomeEnabled"
    data-testid="compact-home"
    class="relative flex min-h-screen flex-col bg-white text-gray-950 dark:bg-dark-950 dark:text-white"
  >
    <header class="relative z-20 border-b border-gray-200 px-4 py-3 sm:px-6 dark:border-dark-800">
      <nav class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 sm:gap-4">
        <div class="flex min-w-0 flex-1 items-center gap-3">
          <div class="flex h-8 w-8 shrink-0 items-center justify-center overflow-hidden rounded-md">
            <img
              :src="siteLogo || '/logo.svg'"
              alt="Logo"
              class="h-full w-full object-contain"
            />
          </div>
          <span class="min-w-0 truncate text-base font-bold tracking-tight">{{ siteName }}</span>
        </div>
        <div class="flex max-w-full shrink-0 flex-wrap items-center justify-end gap-2">
          <LocaleSwitcher />
          <router-link
            v-if="showModelPlazaEntry"
            to="/model-plaza"
            class="flex h-9 shrink-0 items-center gap-1.5 rounded-lg px-3 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-950 dark:text-dark-400 dark:hover:bg-dark-800 dark:hover:text-white"
            :title="t('nav.modelPlaza')"
          >
            <Icon name="grid" size="md" />
            <span class="hidden sm:inline">{{ t('nav.modelPlaza') }}</span>
          </router-link>
          <button
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-gray-600 transition-colors hover:bg-gray-100 dark:text-dark-400 dark:hover:bg-dark-800"
            :title="isDark ? t('home.switchToLight') : t('home.switchToDark')"
            @click="toggleTheme"
          >
            <Icon v-if="isDark" name="sun" size="md" />
            <Icon v-else name="moon" size="md" />
          </button>
          <router-link
            :to="isAuthenticated ? dashboardPath : '/login'"
            class="btn btn-primary btn-sm shrink-0"
          >
            {{ isAuthenticated ? t('home.dashboard') : t('home.login') }}
          </router-link>
        </div>
      </nav>
    </header>

    <main class="relative z-10 flex min-w-0 flex-1 items-center justify-center px-4 py-16 sm:px-6">
      <div class="min-w-0 max-w-xl text-center">
        <div class="mx-auto mb-6 flex h-14 w-14 items-center justify-center overflow-hidden rounded-xl">
          <img
            :src="siteLogo || '/logo.svg'"
            alt="Logo"
            class="h-full w-full object-contain"
          />
        </div>
        <h1 class="[overflow-wrap:anywhere] text-3xl font-bold tracking-tight md:text-4xl">{{ siteName }}</h1>
        <p class="mt-4 whitespace-pre-wrap [overflow-wrap:anywhere] text-base text-gray-600 dark:text-dark-300">{{ siteSubtitle }}</p>
        <router-link
          :to="isAuthenticated ? dashboardPath : '/login'"
          class="btn btn-primary btn-lg mt-8"
        >
          {{ isAuthenticated ? t('home.goToDashboard') : t('home.login') }}
        </router-link>
      </div>
    </main>

    <footer class="relative z-10 min-w-0 border-t border-gray-200 px-4 py-5 text-center text-sm text-gray-500 [overflow-wrap:anywhere] sm:px-6 dark:border-dark-800 dark:text-dark-400">
      &copy; {{ currentYear }} {{ siteName }}
    </footer>
  </div>

  <!-- Default Home Page -->
  <div v-else class="flex min-h-screen flex-col bg-white text-gray-950 dark:bg-dark-950 dark:text-gray-100">
    <!-- Nav -->
    <header class="sticky top-0 z-20 border-b border-gray-200 bg-white/95 dark:border-dark-800 dark:bg-dark-950/95">
      <nav class="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
        <div class="flex min-w-0 items-center gap-8">
          <router-link to="/home" class="flex min-w-0 items-center gap-2.5">
            <img :src="siteLogo || '/logo.svg'" alt="Logo" class="h-7 w-7 flex-none rounded-md object-contain" />
            <span class="truncate text-base font-semibold tracking-tight">{{ siteName }}</span>
          </router-link>
          <div class="hidden items-center gap-6 text-sm text-gray-600 dark:text-dark-400 md:flex">
            <router-link v-if="showModelPlazaEntry" to="/model-plaza" class="hover:text-gray-950 dark:hover:text-white">{{ t('home.v2.navModels') }}</router-link>
            <a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer" class="hover:text-gray-950 dark:hover:text-white">{{ t('home.docs') }}</a>
            <a href="#start" class="hover:text-gray-950 dark:hover:text-white">{{ t('home.v2.navStart') }}</a>
            <router-link to="/key-usage" class="hover:text-gray-950 dark:hover:text-white">{{ t('home.v2.navKeyUsage') }}</router-link>
          </div>
        </div>
        <div class="flex flex-none items-center gap-1 sm:gap-2">
          <LocaleSwitcher />
          <button
            type="button"
            class="btn-ghost btn-icon"
            :aria-label="isDark ? t('home.switchToLight') : t('home.switchToDark')"
            :title="isDark ? t('home.switchToLight') : t('home.switchToDark')"
            @click="toggleTheme"
          >
            <Icon v-if="isDark" name="sun" size="sm" />
            <Icon v-else name="moon" size="sm" />
          </button>
          <template v-if="isAuthenticated">
            <router-link :to="dashboardPath" class="btn btn-primary btn-sm">
              <span class="flex h-5 w-5 items-center justify-center rounded-full bg-white/20 text-[11px] font-semibold dark:bg-gray-950/15">{{ userInitial }}</span>
              {{ t('home.dashboard') }}
            </router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-ghost btn-sm hidden sm:inline-flex">{{ t('home.login') }}</router-link>
            <router-link to="/register" class="btn btn-primary btn-sm">{{ t('home.v2.signUp') }}</router-link>
          </template>
        </div>
      </nav>
    </header>

    <main class="flex-1">
      <!-- Hero -->
      <section class="mx-auto grid max-w-6xl items-center gap-12 px-4 pb-16 pt-16 sm:px-6 md:pt-24 lg:grid-cols-2">
        <div class="min-w-0">
          <span class="inline-flex items-center gap-2 rounded-full border border-gray-200 py-1 pl-2 pr-3 text-xs text-gray-600 dark:border-dark-700 dark:text-dark-400">
            <span class="h-2 w-2 rounded-full bg-emerald-600" aria-hidden="true"></span>
            {{ t('home.v2.badge') }}
          </span>
          <h1 class="mt-5 text-4xl font-bold leading-[1.12] tracking-tight sm:text-5xl">
            {{ t('home.v2.heroTitle') }}
          </h1>
          <p class="mt-5 max-w-xl text-lg text-gray-600 dark:text-dark-400">
            {{ t('home.v2.heroDesc') }}
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <router-link :to="isAuthenticated ? dashboardPath : '/register'" class="btn btn-primary btn-lg">
              {{ isAuthenticated ? t('home.goToDashboard') : t('home.v2.ctaPrimary') }}
            </router-link>
            <router-link v-if="showModelPlazaEntry" to="/model-plaza" class="btn btn-secondary btn-lg">
              {{ t('home.v2.ctaModels') }}
            </router-link>
            <a v-else-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-lg">
              {{ t('home.viewDocs') }}
            </a>
          </div>
          <p v-if="siteSubtitleCustom" class="mt-4 whitespace-pre-wrap text-sm text-gray-500 dark:text-dark-400">{{ siteSubtitleCustom }}</p>
        </div>

        <!-- Code panel -->
        <div class="terminal-container min-w-0 overflow-hidden rounded-xl border border-dark-800 bg-dark-950 text-gray-100">
          <div class="flex items-center justify-between border-b border-dark-800 pr-2">
            <div class="flex overflow-x-auto" role="tablist">
              <button
                v-for="tab in codeTabs"
                :key="tab.id"
                type="button"
                role="tab"
                :aria-selected="activeCodeTab === tab.id"
                class="-mb-px whitespace-nowrap border-b-2 px-4 py-3 text-[13px] transition-colors"
                :class="activeCodeTab === tab.id ? 'border-primary-500 text-white' : 'border-transparent text-dark-400 hover:text-gray-200'"
                @click="activeCodeTab = tab.id"
              >
                {{ tab.label }}
              </button>
            </div>
            <button type="button" class="rounded-md p-2 text-dark-400 hover:bg-dark-800 hover:text-white" :aria-label="t('home.v2.copyCode')" @click="copyCode">
              <Icon :name="codeCopied ? 'check' : 'copy'" size="sm" />
            </button>
          </div>
          <pre class="min-h-[250px] overflow-x-auto whitespace-pre p-6 font-mono text-[13px] leading-7 text-gray-200">{{ activeCode }}</pre>
          <div class="flex flex-wrap justify-between gap-2 border-t border-dark-800 px-6 py-3 text-xs text-dark-400">
            <span>Base URL：<span class="font-mono text-gray-100">{{ apiBase }}</span></span>
            <span>{{ activeCodeHint }}</span>
          </div>
        </div>
      </section>

      <!-- Providers strip -->
      <section class="border-y border-gray-200 bg-gray-50 dark:border-dark-800 dark:bg-dark-900">
        <div class="mx-auto flex max-w-6xl flex-wrap items-center justify-center gap-x-10 gap-y-3 px-4 py-5 text-sm sm:px-6">
          <span class="text-gray-500 dark:text-dark-400">{{ t('home.v2.supported') }}</span>
          <span v-for="p in providerNames" :key="p" class="font-semibold text-gray-950 dark:text-white">{{ p }}</span>
        </div>
      </section>

      <!-- Steps -->
      <section id="start" class="mx-auto max-w-6xl scroll-mt-20 px-4 pt-24 sm:px-6">
        <p class="text-sm font-semibold text-primary-600 dark:text-primary-400">{{ t('home.v2.stepsEyebrow') }}</p>
        <h2 class="mt-2 text-3xl font-bold tracking-tight">{{ t('home.v2.stepsTitle') }}</h2>
        <ol class="mt-10 grid gap-5 md:grid-cols-3">
          <li v-for="(step, i) in steps" :key="step.title" class="rounded-xl border border-gray-200 p-7 dark:border-dark-800">
            <span class="font-mono text-sm text-gray-500 dark:text-dark-400">0{{ i + 1 }}</span>
            <h3 class="mt-3 text-lg font-semibold">{{ step.title }}</h3>
            <p class="mt-1.5 text-gray-600 dark:text-dark-400">{{ step.desc }}</p>
          </li>
        </ol>
      </section>

      <!-- Models (from model plaza) -->
      <section v-if="showModelPlazaEntry" class="mx-auto max-w-6xl px-4 pt-24 sm:px-6">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="text-sm font-semibold text-primary-600 dark:text-primary-400">{{ t('home.v2.modelsEyebrow') }}</p>
            <h2 class="mt-2 text-3xl font-bold tracking-tight">{{ t('home.v2.modelsTitle') }}</h2>
          </div>
          <router-link to="/model-plaza" class="text-sm font-semibold text-primary-600 hover:text-primary-700 dark:text-primary-400">
            {{ t('home.v2.modelsAll') }} →
          </router-link>
        </div>
        <div class="mt-8 overflow-x-auto rounded-xl border border-gray-200 dark:border-dark-800">
          <table class="w-full min-w-[480px] text-sm">
            <thead>
              <tr class="bg-gray-50 text-left text-xs text-gray-600 dark:bg-dark-900 dark:text-dark-400">
                <th class="px-5 py-3 font-medium">{{ t('home.v2.colModel') }}</th>
                <th class="px-5 py-3 font-medium">{{ t('home.v2.colProvider') }}</th>
                <th class="px-5 py-3 text-right font-medium">{{ t('home.v2.colPrice') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!plazaModels.length">
                <td colspan="3" class="px-5 py-8 text-center text-gray-500 dark:text-dark-400">{{ t('home.v2.modelsEmpty') }}</td>
              </tr>
              <tr v-for="m in plazaModels" :key="m.platform + m.name" class="border-t border-gray-200 dark:border-dark-800">
                <td class="px-5 py-3 font-mono font-medium">{{ m.name }}</td>
                <td class="px-5 py-3 text-gray-600 dark:text-dark-400">{{ platformLabel(m.platform) }}</td>
                <td class="px-5 py-3 text-right">
                  <router-link to="/model-plaza" class="text-gray-600 underline-offset-2 hover:text-gray-950 hover:underline dark:text-dark-400 dark:hover:text-white">{{ t('home.v2.viewPrice') }}</router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Why -->
      <section class="mx-auto max-w-6xl px-4 py-24 sm:px-6">
        <h2 class="text-3xl font-bold tracking-tight">{{ t('home.v2.whyTitle', { name: siteName }) }}</h2>
        <div class="mt-10 grid gap-10 md:grid-cols-3">
          <div v-for="f in features" :key="f.title">
            <Icon :name="f.icon" size="lg" class="text-primary-600 dark:text-primary-400" />
            <h3 class="mt-3 text-lg font-semibold">{{ f.title }}</h3>
            <p class="mt-1.5 text-gray-600 dark:text-dark-400">{{ f.desc }}</p>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section class="border-t border-gray-200 bg-gray-50 dark:border-dark-800 dark:bg-dark-900">
        <div class="mx-auto max-w-3xl px-4 py-20 sm:px-6">
          <h2 class="text-center text-3xl font-bold tracking-tight">{{ t('home.v2.faqTitle') }}</h2>
          <div class="mt-10">
            <div v-for="(item, i) in faqs" :key="item.q" class="border-b border-gray-200 dark:border-dark-700">
              <button
                type="button"
                class="flex w-full items-center justify-between gap-4 py-5 text-left text-base font-semibold"
                :aria-expanded="openFaq === i"
                @click="openFaq = openFaq === i ? -1 : i"
              >
                <span>{{ item.q }}</span>
                <span class="font-mono text-gray-500" aria-hidden="true">{{ openFaq === i ? '−' : '+' }}</span>
              </button>
              <p v-if="openFaq === i" class="pb-5 text-gray-600 dark:text-dark-400">{{ item.a }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="mx-auto max-w-6xl px-4 py-24 text-center sm:px-6">
        <h2 class="text-3xl font-bold tracking-tight sm:text-4xl">{{ t('home.v2.ctaTitle') }}</h2>
        <p class="mt-3 text-lg text-gray-600 dark:text-dark-400">{{ t('home.v2.ctaDesc') }}</p>
        <div class="mt-8 flex flex-wrap justify-center gap-3">
          <router-link :to="isAuthenticated ? dashboardPath : '/register'" class="btn btn-primary btn-lg">
            {{ isAuthenticated ? t('home.goToDashboard') : t('home.v2.signUp') }}
          </router-link>
          <a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-lg">{{ t('home.viewDocs') }}</a>
        </div>
      </section>
    </main>

    <footer class="border-t border-gray-200 dark:border-dark-800">
      <div class="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-8 text-sm text-gray-500 dark:text-dark-400 sm:px-6">
        <span>&copy; {{ currentYear }} {{ siteName }}</span>
        <div class="flex flex-wrap gap-6">
          <router-link v-for="doc in legalDocs" :key="doc.id" :to="`/legal/${doc.id}`" class="hover:text-gray-950 dark:hover:text-white">{{ doc.title }}</router-link>
          <a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer" class="hover:text-gray-950 dark:hover:text-white">{{ t('home.docs') }}</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore, useAppStore } from '@/stores'
import LocaleSwitcher from '@/components/common/LocaleSwitcher.vue'
import Icon from '@/components/icons/Icon.vue'
import { resolveBrandName } from '@/utils/branding'
import { sanitizeUrl } from '@/utils/url'
import DOMPurify from 'dompurify'
import { FeatureFlags, isFeatureFlagEnabled } from '@/utils/featureFlags'
import { modelPlazaAPI } from '@/api/modelPlaza'
import { useClipboard } from '@/composables/useClipboard'

const { t } = useI18n()

const authStore = useAuthStore()
const appStore = useAppStore()

// Site settings - directly from appStore (already initialized from injected config)
const siteName = computed(() =>
  resolveBrandName(appStore.cachedPublicSettings?.site_name || appStore.siteName)
)
const siteLogo = computed(() => sanitizeUrl(appStore.cachedPublicSettings?.site_logo || appStore.siteLogo || '', { allowRelative: true, allowDataUrl: true }))
const siteSubtitle = computed(() => appStore.cachedPublicSettings?.site_subtitle || t('home.v2.heroDesc'))
// 管理员自定义的副标题（非默认值）才在首页大标题下额外展示
const siteSubtitleCustom = computed(() => {
  const raw = (appStore.cachedPublicSettings?.site_subtitle || '').trim()
  if (!raw || /^(AI API Gateway|Intelligent AI Agent & API Gateway Platform)$/i.test(raw)) return ''
  return raw
})
const docUrl = computed(() => sanitizeUrl(appStore.cachedPublicSettings?.doc_url || appStore.docUrl || ''))
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

// ============ 默认首页内容 ============
const { copyToClipboard } = useClipboard()

const apiBase = computed(() => {
  const raw = (appStore.apiBaseUrl || window.location.origin).trim()
  return raw.replace(/\/+$/, '').replace(/\/v1$/, '')
})
const providerId = computed(() => siteName.value.toLowerCase().replace(/[^a-z0-9]+/g, '') || 'gateway')
const envKey = computed(() => `${providerId.value.toUpperCase()}_API_KEY`)

type CodeTabId = 'curl' | 'python' | 'claude' | 'codex'
const activeCodeTab = ref<CodeTabId>('curl')
const codeCopied = ref(false)
const codeTabs = computed(() => {
  const base = apiBase.value
  return [
    {
      id: 'curl' as const,
      label: 'cURL',
      hint: t('home.v2.hintOpenai'),
      code: `curl ${base}/v1/chat/completions \\\n  -H "Authorization: Bearer $${envKey.value}" \\\n  -H "Content-Type: application/json" \\\n  -d '{\n    "model": "<model>",\n    "messages": [{"role": "user", "content": "Hello"}]\n  }'`
    },
    {
      id: 'python' as const,
      label: 'Python',
      hint: t('home.v2.hintSdk'),
      code: `from openai import OpenAI\n\nclient = OpenAI(\n    base_url="${base}/v1",\n    api_key="sk-...",\n)\n\nresp = client.chat.completions.create(\n    model="<model>",\n    messages=[{"role": "user", "content": "Hello"}],\n)\nprint(resp.choices[0].message.content)`
    },
    {
      id: 'claude' as const,
      label: 'Claude Code',
      hint: t('home.v2.hintAnthropic'),
      code: `export ANTHROPIC_BASE_URL="${base}"\nexport ANTHROPIC_AUTH_TOKEN="sk-..."\n\nclaude`
    },
    {
      id: 'codex' as const,
      label: 'Codex',
      hint: '~/.codex/config.toml',
      code: `model_provider = "${providerId.value}"\nmodel = "<model>"\n\n[model_providers.${providerId.value}]\nname = "${siteName.value}"\nbase_url = "${base}/v1"\nenv_key = "${envKey.value}"\nwire_api = "responses"`
    }
  ]
})
const activeTabData = computed(() => codeTabs.value.find((tab) => tab.id === activeCodeTab.value) ?? codeTabs.value[0])
const activeCode = computed(() => activeTabData.value.code)
const activeCodeHint = computed(() => activeTabData.value.hint)

async function copyCode() {
  const ok = await copyToClipboard(activeCode.value, t('home.v2.copied'))
  if (ok) {
    codeCopied.value = true
    setTimeout(() => (codeCopied.value = false), 1500)
  }
}

const PLATFORM_LABELS: Record<string, string> = {
  anthropic: 'Anthropic',
  openai: 'OpenAI',
  gemini: 'Google',
  grok: 'xAI',
  deepseek: 'DeepSeek',
  kimi: 'Moonshot',
  zhipu: 'Zhipu',
  minimax: 'MiniMax'
}
function platformLabel(p: string): string {
  return PLATFORM_LABELS[p] ?? p
}

const plazaModels = ref<Array<{ name: string; platform: string }>>([])
const providerNames = computed(() => {
  const fromPlaza = Array.from(new Set(plazaModels.value.map((m) => platformLabel(m.platform))))
  return fromPlaza.length ? fromPlaza.slice(0, 6) : ['Anthropic Claude', 'OpenAI GPT', 'Google Gemini', 'xAI Grok']
})

async function loadPlazaModels() {
  try {
    const res = await modelPlazaAPI.getModelPlaza()
    const seen = new Set<string>()
    const list: Array<{ name: string; platform: string }> = []
    for (const group of res.groups || []) {
      for (const m of group.models || []) {
        const key = `${m.platform}:${m.name}`
        if (seen.has(key)) continue
        seen.add(key)
        list.push({ name: m.name, platform: m.platform || group.platform })
      }
    }
    plazaModels.value = list.slice(0, 8)
  } catch {
    plazaModels.value = []
  }
}

const steps = computed(() => [
  { title: t('home.v2.step1Title'), desc: t('home.v2.step1Desc') },
  { title: t('home.v2.step2Title'), desc: t('home.v2.step2Desc') },
  { title: t('home.v2.step3Title'), desc: t('home.v2.step3Desc') }
])

const features = computed(() => [
  { icon: 'shield' as const, title: t('home.v2.feat1Title'), desc: t('home.v2.feat1Desc') },
  { icon: 'chartBar' as const, title: t('home.v2.feat2Title'), desc: t('home.v2.feat2Desc') },
  { icon: 'terminal' as const, title: t('home.v2.feat3Title'), desc: t('home.v2.feat3Desc') }
])

const openFaq = ref(0)
const faqs = computed(() => [
  { q: t('home.v2.faq1Q'), a: t('home.v2.faq1A') },
  { q: t('home.v2.faq2Q'), a: t('home.v2.faq2A') },
  { q: t('home.v2.faq3Q'), a: t('home.v2.faq3A') }
])

const legalDocs = computed(() =>
  (appStore.cachedPublicSettings?.login_agreement_documents ?? []).filter((doc) => doc.id && doc.title)
)

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

// 默认首页且模型广场对访客可见时，读取真实模型列表
watch(
  () => !hasHomeContent.value && !compactHomeEnabled.value && showModelPlazaEntry.value,
  (shouldLoad) => {
    if (shouldLoad && !plazaModels.value.length) void loadPlazaModels()
  },
  { immediate: true }
)
</script>

<style scoped>
.terminal-container pre {
  tab-size: 2;
}
</style>
