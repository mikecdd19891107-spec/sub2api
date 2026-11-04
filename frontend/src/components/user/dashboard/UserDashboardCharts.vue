<template>
  <section class="card p-5">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <h2 class="text-sm font-semibold text-gray-950 dark:text-white">{{ t('dashboard.usageTrend') }}</h2>
      <div class="flex flex-wrap items-center gap-2">
        <DateRangePicker :start-date="startDate" :end-date="endDate" @update:startDate="$emit('update:startDate', $event)" @update:endDate="$emit('update:endDate', $event)" @change="$emit('dateRangeChange', $event)" />
        <div class="w-24">
          <Select :model-value="granularity" :options="[{value:'day', label:t('dashboard.day')}, {value:'hour', label:t('dashboard.hour')}]" @update:model-value="$emit('update:granularity', $event)" @change="$emit('granularityChange')" />
        </div>
        <button type="button" :disabled="loading" class="btn btn-secondary btn-icon" :aria-label="t('common.refresh')" :title="t('common.refresh')" @click="$emit('refresh')">
          <Icon name="refresh" size="sm" />
        </button>
      </div>
    </div>

    <div class="mt-5">
      <TokenUsageTrend :trend-data="trend" :loading="loading" bare />
    </div>

    <!-- 模型分布 -->
    <div class="mt-6 border-t border-gray-200 pt-5 dark:border-dark-800">
      <h3 class="mb-3 text-sm font-semibold text-gray-950 dark:text-white">{{ t('dashboard.modelDistribution') }}</h3>
      <div v-if="loading" class="flex h-32 items-center justify-center"><LoadingSpinner size="md" /></div>
      <div v-else-if="modelData" class="flex flex-col gap-5 sm:flex-row sm:items-start">
        <div class="h-36 w-36 shrink-0 self-center sm:self-start">
          <Doughnut :data="modelData" :options="doughnutOptions" />
        </div>
        <div class="w-full min-w-0 flex-1 overflow-x-auto">
          <table class="w-full min-w-[420px] text-xs">
            <thead>
              <tr class="text-left text-gray-500 dark:text-dark-400">
                <th class="pb-2 font-medium">{{ t('dashboard.model') }}</th>
                <th class="pb-2 text-right font-medium">{{ t('dashboard.requests') }}</th>
                <th class="pb-2 text-right font-medium">{{ t('dashboard.tokens') }}</th>
                <th class="pb-2 text-right font-medium">{{ t('dashboard.actual') }}</th>
                <th class="pb-2 text-right font-medium">{{ t('dashboard.standard') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(model, i) in models" :key="model.model" class="border-t border-gray-200 dark:border-dark-800">
                <td class="max-w-[180px] py-2">
                  <span class="flex items-center gap-2">
                    <span class="h-2 w-2 flex-none rounded-sm" :style="{ backgroundColor: MODEL_COLORS[i % MODEL_COLORS.length] }" aria-hidden="true"></span>
                    <span class="truncate font-mono text-gray-950 dark:text-white" :title="model.model">{{ model.model }}</span>
                  </span>
                </td>
                <td class="py-2 text-right font-mono text-gray-700 dark:text-gray-300">{{ formatNumber(model.requests) }}</td>
                <td class="py-2 text-right font-mono text-gray-700 dark:text-gray-300">{{ formatTokens(model.total_tokens) }}</td>
                <td class="py-2 text-right font-mono font-medium text-gray-950 dark:text-white">${{ formatCost(model.actual_cost) }}</td>
                <td class="py-2 text-right font-mono text-gray-500 dark:text-dark-400">${{ formatCost(model.cost) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="flex h-24 items-center justify-center text-sm text-gray-500 dark:text-dark-400">{{ t('dashboard.noDataAvailable') }}</div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import DateRangePicker from '@/components/common/DateRangePicker.vue'
import Select from '@/components/common/Select.vue'
import { Doughnut } from 'vue-chartjs'
import TokenUsageTrend from '@/components/charts/TokenUsageTrend.vue'
import Icon from '@/components/icons/Icon.vue'
import type { TrendDataPoint, ModelStat } from '@/types'
import { formatNumberLocaleString as formatNumber, formatTokensK as formatTokens } from '@/utils/format'

// 金额两位小数；不足 1 分保留 4 位
const formatCost = (v: number) => { const n = Number(v || 0); return n === 0 ? '0.00' : n < 0.01 ? n.toFixed(4) : n.toFixed(2) }
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler)

const props = defineProps<{ loading: boolean, startDate: string, endDate: string, granularity: string, trend: TrendDataPoint[], models: ModelStat[] }>()
defineEmits(['update:startDate', 'update:endDate', 'update:granularity', 'dateRangeChange', 'granularityChange', 'refresh'])
const { t } = useI18n()

// 第一色为品牌强调色，其余为中性/低饱和色，相邻颜色明度区分明显
const MODEL_COLORS = ['#E8590C', '#6E6E73', '#0F766E', '#2563EB', '#A1A1A8', '#B45309', '#D6D6D2', '#2E2E33']

const modelData = computed(() => !props.models?.length ? null : {
  labels: props.models.map((m: ModelStat) => m.model),
  datasets: [{
    data: props.models.map((m: ModelStat) => m.total_tokens),
    backgroundColor: MODEL_COLORS,
    borderWidth: 0
  }]
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '68%',
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context: any) => `${context.label}: ${formatTokens(context.parsed)} tokens`
      }
    }
  }
}
</script>
