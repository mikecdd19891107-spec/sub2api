<template>
  <section class="card overflow-hidden">
    <div class="flex items-center justify-between px-5 py-4">
      <h2 class="text-sm font-semibold text-gray-950 dark:text-white">{{ t('dashboard.recentUsage') }}</h2>
      <router-link to="/usage" class="text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
        {{ t('dashboard.viewAllUsage') }} →
      </router-link>
    </div>
    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoadingSpinner size="lg" />
    </div>
    <div v-else-if="data.length === 0" class="px-5 pb-8">
      <EmptyState :title="t('dashboard.noUsageRecords')" :description="t('dashboard.startUsingApi')" />
    </div>
    <div v-else class="overflow-x-auto">
      <table class="w-full min-w-[560px] text-sm">
        <thead>
          <tr class="bg-gray-50 text-left text-xs text-gray-600 dark:bg-dark-900 dark:text-dark-400">
            <th class="px-5 py-2.5 font-medium">{{ t('dashboard.recent.time') }}</th>
            <th class="px-3 py-2.5 font-medium">{{ t('dashboard.model') }}</th>
            <th class="px-3 py-2.5 text-right font-medium">{{ t('dashboard.recent.tokensInOut') }}</th>
            <th class="px-3 py-2.5 text-right font-medium">{{ t('dashboard.recent.duration') }}</th>
            <th class="px-5 py-2.5 text-right font-medium">{{ t('dashboard.recent.cost') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in data" :key="log.id" class="border-t border-gray-200 dark:border-dark-800">
            <td class="whitespace-nowrap px-5 py-2.5 font-mono text-xs text-gray-600 dark:text-dark-400">{{ formatDateTime(log.created_at) }}</td>
            <td class="max-w-[220px] truncate px-3 py-2.5 font-mono text-xs text-gray-950 dark:text-white" :title="log.model">{{ log.model }}</td>
            <td class="whitespace-nowrap px-3 py-2.5 text-right font-mono text-xs text-gray-700 dark:text-gray-300">
              {{ log.input_tokens.toLocaleString() }} / {{ log.output_tokens.toLocaleString() }}
            </td>
            <td class="whitespace-nowrap px-3 py-2.5 text-right font-mono text-xs text-gray-600 dark:text-dark-400">{{ formatDuration(log.duration_ms) }}</td>
            <td class="whitespace-nowrap px-5 py-2.5 text-right font-mono text-xs">
              <span class="font-medium text-gray-950 dark:text-white" :title="t('dashboard.actual')">¥{{ formatCost(log.actual_cost) }}</span>
              <span v-if="log.total_cost !== log.actual_cost" class="ml-1 text-gray-500 dark:text-dark-400" :title="t('dashboard.standard')">/ ¥{{ formatCost(log.total_cost) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import { formatDateTime } from '@/utils/format'
import type { UsageLog } from '@/types'

defineProps<{
  data: UsageLog[]
  loading: boolean
}>()
const { t } = useI18n()
const formatCost = (c: number) => Number(c || 0).toFixed(4)
const formatDuration = (ms: number | null) => (ms == null ? '-' : ms >= 1000 ? `${(ms / 1000).toFixed(1)} s` : `${Math.round(ms)} ms`)
</script>
