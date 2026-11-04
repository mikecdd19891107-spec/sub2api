<template>
  <section v-if="visible" class="card p-5" data-testid="dashboard-get-started">
    <div class="flex items-start justify-between gap-4">
      <div>
        <h2 class="text-sm font-semibold text-gray-950 dark:text-white">
          {{ t('dashboard.getStarted.title', { name: siteName }) }}
        </h2>
        <p class="mt-0.5 text-xs text-gray-500 dark:text-dark-400">
          {{ t('dashboard.getStarted.progress', { done: doneCount, total: steps.length }) }}
        </p>
      </div>
      <button type="button" class="btn-ghost rounded-md px-2 py-1 text-xs" @click="dismiss">
        {{ t('dashboard.getStarted.dismiss') }}
      </button>
    </div>

    <ol class="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
      <li
        v-for="(step, index) in steps"
        :key="step.key"
        class="flex items-start gap-3 rounded-lg p-3.5"
        :class="
          step.current
            ? 'border border-gray-950 dark:border-gray-300'
            : 'bg-gray-50 dark:bg-dark-800/60'
        "
      >
        <span
          class="flex h-[22px] w-[22px] flex-none items-center justify-center rounded-full font-mono text-xs"
          :class="
            step.done
              ? 'bg-emerald-700 text-white'
              : step.current
                ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950'
                : 'border border-gray-400 text-gray-500 dark:border-dark-500 dark:text-dark-400'
          "
          aria-hidden="true"
        >
          <Icon v-if="step.done" name="check" size="xs" :stroke-width="3" />
          <template v-else>{{ index + 1 }}</template>
        </span>
        <div class="min-w-0">
          <component
            :is="step.to && !step.done ? 'router-link' : 'div'"
            :to="step.to"
            class="text-sm font-semibold"
            :class="step.done ? 'text-gray-500 line-through dark:text-dark-400' : 'text-gray-950 hover:underline dark:text-white'"
          >
            {{ step.title }}
          </component>
          <p class="text-xs text-gray-600 dark:text-dark-400">{{ step.desc }}</p>
        </div>
      </li>
    </ol>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
import { useAppStore } from '@/stores'
import { resolveBrandName } from '@/utils/branding'

const props = defineProps<{
  totalKeys: number
  totalRequests: number
}>()

const DISMISS_KEY = 'dashboard_get_started_dismissed'

const { t } = useI18n()
const appStore = useAppStore()
const siteName = computed(() => resolveBrandName(appStore.siteName))

function readDismissed(): boolean {
  try {
    return localStorage.getItem(DISMISS_KEY) === '1'
  } catch {
    return false
  }
}

const dismissed = ref(readDismissed())

const hasKey = computed(() => props.totalKeys > 0)
const hasRequest = computed(() => props.totalRequests > 0)

const steps = computed(() => {
  const list = [
    {
      key: 'key',
      done: hasKey.value,
      to: '/keys',
      title: t('dashboard.getStarted.step1Title'),
      desc: hasKey.value
        ? t('dashboard.getStarted.step1Done', { count: props.totalKeys })
        : t('dashboard.getStarted.step1Desc')
    },
    {
      key: 'client',
      // 无法直接检测客户端是否配置，以「已有请求」视为完成
      done: hasRequest.value,
      to: '',
      title: t('dashboard.getStarted.step2Title'),
      desc: t('dashboard.getStarted.step2Desc')
    },
    {
      key: 'request',
      done: hasRequest.value,
      to: '/usage',
      title: t('dashboard.getStarted.step3Title'),
      desc: hasRequest.value ? t('dashboard.getStarted.step3Done') : t('dashboard.getStarted.step3Desc')
    }
  ]
  const firstOpen = list.findIndex((s) => !s.done)
  return list.map((s, i) => ({ ...s, current: i === firstOpen }))
})

const doneCount = computed(() => steps.value.filter((s) => s.done).length)
const visible = computed(() => !dismissed.value && doneCount.value < steps.value.length)

function dismiss() {
  dismissed.value = true
  try {
    localStorage.setItem(DISMISS_KEY, '1')
  } catch {
    // ignore storage errors
  }
}
</script>
