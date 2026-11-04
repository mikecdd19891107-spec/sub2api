<template>
  <section class="card">
    <div class="px-5 py-4">
      <h2 class="text-sm font-semibold text-gray-950 dark:text-white">{{ t('dashboard.quickActions') }}</h2>
    </div>
    <div class="px-2 pb-2">
      <button
        v-for="action in actions"
        :key="action.to"
        type="button"
        class="group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left transition-colors hover:bg-gray-100 dark:hover:bg-dark-800"
        @click="router.push(action.to)"
      >
        <span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg border border-gray-200 text-gray-700 dark:border-dark-700 dark:text-gray-300">
          <Icon :name="action.icon" size="sm" />
        </span>
        <span class="min-w-0 flex-1">
          <span class="block text-sm font-medium text-gray-950 dark:text-white">{{ action.title }}</span>
          <span class="block truncate text-xs text-gray-500 dark:text-dark-400">{{ action.desc }}</span>
        </span>
        <Icon name="chevronRight" size="sm" class="text-gray-400 group-hover:text-gray-950 dark:text-dark-500 dark:group-hover:text-white" />
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
import { useBatchImageAccess } from '@/composables/useBatchImageAccess'
const router = useRouter()
const { t } = useI18n()
const { canUseBatchImage, refreshBatchImageAccess } = useBatchImageAccess()

const actions = computed(() => {
  const list: Array<{ to: string; icon: 'key' | 'chart' | 'sparkles' | 'gift'; title: string; desc: string }> = [
    { to: '/keys', icon: 'key', title: t('dashboard.createApiKey'), desc: t('dashboard.generateNewKey') },
    { to: '/usage', icon: 'chart', title: t('dashboard.viewUsage'), desc: t('dashboard.checkDetailedLogs') }
  ]
  if (canUseBatchImage.value) {
    list.push({ to: '/batch-image', icon: 'sparkles', title: t('dashboard.batchImageAgent'), desc: t('dashboard.batchImageAgentDesc') })
  }
  list.push({ to: '/redeem', icon: 'gift', title: t('dashboard.redeemCode'), desc: t('dashboard.addBalanceWithCode') })
  return list
})

onMounted(() => {
  void refreshBatchImageAccess()
})
</script>
