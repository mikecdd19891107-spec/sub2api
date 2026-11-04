<template>
  <section class="card flex flex-col p-5" data-testid="dashboard-quick-connect">
    <h2 class="text-sm font-semibold text-gray-950 dark:text-white">{{ t('dashboard.quickConnect.title') }}</h2>

    <label for="qc-base-url" class="mt-4 text-xs text-gray-600 dark:text-dark-400">
      {{ t('dashboard.quickConnect.baseUrl') }}
    </label>
    <div class="mt-1 flex gap-2">
      <input id="qc-base-url" :value="baseUrl" readonly class="input min-w-0 flex-1 bg-gray-50 font-mono text-xs dark:bg-dark-800" />
      <button type="button" class="btn btn-secondary btn-sm" @click="copy(baseUrl)">
        {{ t('dashboard.quickConnect.copy') }}
      </button>
    </div>

    <template v-if="keys.length">
      <label for="qc-key" class="mt-3 text-xs text-gray-600 dark:text-dark-400">
        {{ t('dashboard.quickConnect.key') }}
      </label>
      <select id="qc-key" v-model="selectedKeyId" class="input mt-1 text-sm">
        <option v-for="k in keys" :key="k.id" :value="k.id">{{ k.name }} · {{ maskKey(k.key) }}</option>
      </select>

      <div class="mt-4 flex flex-wrap gap-x-1 border-b border-gray-200 dark:border-dark-800" role="tablist">
        <button
          v-for="c in clients"
          :key="c.id"
          type="button"
          role="tab"
          :aria-selected="activeClient === c.id"
          class="-mb-px whitespace-nowrap border-b-2 px-2 py-2 text-[13px] transition-colors"
          :class="
            activeClient === c.id
              ? 'border-primary-500 font-semibold text-gray-950 dark:text-white'
              : 'border-transparent text-gray-600 hover:text-gray-950 dark:text-dark-400 dark:hover:text-white'
          "
          @click="activeClient = c.id"
        >
          {{ c.label }}
        </button>
      </div>
      <pre class="code-block mt-3 min-h-[120px] flex-1 whitespace-pre-wrap break-all text-xs leading-relaxed">{{ snippet(true) }}</pre>
      <div class="mt-3 flex gap-2">
        <button type="button" class="btn btn-primary flex-1" @click="copy(snippet(false))">
          {{ t('dashboard.quickConnect.copyConfig') }}
        </button>
        <button v-if="selectedKey" type="button" class="btn btn-secondary" @click="showUseKey = true">
          {{ t('dashboard.quickConnect.fullConfig') }}
        </button>
      </div>
    </template>

    <div v-else-if="!loading" class="mt-4 rounded-lg bg-gray-50 p-4 text-sm dark:bg-dark-800/60">
      <p class="text-gray-700 dark:text-gray-300">{{ t('dashboard.quickConnect.noKey') }}</p>
      <router-link to="/keys" class="btn btn-primary btn-sm mt-3">{{ t('dashboard.quickConnect.createKey') }}</router-link>
    </div>

    <UseKeyModal
      v-if="selectedKey"
      :show="showUseKey"
      :api-key="selectedKey.key"
      :base-url="baseUrl"
      :platform="selectedKey.group?.platform || null"
      :claude-code-only="selectedKey.group?.claude_code_only || false"
      :allow-messages-dispatch="selectedKey.group?.allow_messages_dispatch || false"
      @close="showUseKey = false"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { keysAPI } from '@/api'
import { useAppStore } from '@/stores'
import { useClipboard } from '@/composables/useClipboard'
import { resolveBrandName } from '@/utils/branding'
import UseKeyModal from '@/components/keys/UseKeyModal.vue'
import type { ApiKey } from '@/types'

type ClientId = 'claude' | 'codex' | 'openai' | 'python'

const { t } = useI18n()
const appStore = useAppStore()
const { copyToClipboard } = useClipboard()

const keys = ref<ApiKey[]>([])
const loading = ref(true)
const selectedKeyId = ref<number | null>(null)
const activeClient = ref<ClientId>('claude')
const showUseKey = ref(false)

const clients = computed<Array<{ id: ClientId; label: string }>>(() => [
  { id: 'claude', label: 'Claude Code' },
  { id: 'codex', label: 'Codex' },
  { id: 'openai', label: t('dashboard.quickConnect.openaiCompatible') },
  { id: 'python', label: 'Python' }
])

const baseUrl = computed(() => {
  const raw = (appStore.apiBaseUrl || window.location.origin).trim()
  return raw.replace(/\/+$/, '').replace(/\/v1$/, '')
})

const brand = computed(() => resolveBrandName(appStore.siteName))
const providerId = computed(() => brand.value.toLowerCase().replace(/[^a-z0-9]+/g, '') || 'gateway')
const envKey = computed(() => `${providerId.value.toUpperCase()}_API_KEY`)

const selectedKey = computed(() => keys.value.find((k) => k.id === selectedKeyId.value) || null)

function maskKey(key: string): string {
  if (!key) return ''
  return key.length <= 10 ? key : `${key.slice(0, 3)}…${key.slice(-4)}`
}

function snippet(masked: boolean): string {
  const k = selectedKey.value?.key || ''
  const key = masked ? maskKey(k) : k
  const base = baseUrl.value
  switch (activeClient.value) {
    case 'claude':
      return `export ANTHROPIC_BASE_URL="${base}"\nexport ANTHROPIC_AUTH_TOKEN="${key}"\nclaude`
    case 'codex':
      return `# ~/.codex/config.toml\nmodel_provider = "${providerId.value}"\n\n[model_providers.${providerId.value}]\nname = "${brand.value}"\nbase_url = "${base}/v1"\nenv_key = "${envKey.value}"\nwire_api = "responses"\n\n# ${t('dashboard.quickConnect.shellHint')}\nexport ${envKey.value}="${key}"`
    case 'openai':
      return `API Key:  ${key}\nBase URL: ${base}/v1`
    case 'python':
      return `from openai import OpenAI\n\nclient = OpenAI(\n    base_url="${base}/v1",\n    api_key="${key}",\n)`
  }
  return ''
}

async function copy(text: string) {
  await copyToClipboard(text, t('dashboard.quickConnect.copied'))
}

onMounted(async () => {
  try {
    const res = await keysAPI.list(1, 20, { status: 'active' })
    keys.value = res.items || []
    selectedKeyId.value = keys.value[0]?.id ?? null
  } catch (error) {
    console.error('Failed to load keys for quick connect:', error)
  } finally {
    loading.value = false
  }
})
</script>
