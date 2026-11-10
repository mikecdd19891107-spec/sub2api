<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <LoadingSpinner />
      </div>

      <template v-else-if="stats">
        <!-- VisionOS Bento 便当盒管理中枢 -->
        <!-- Top Bento Grid: 5-col Hero Gateway Card + 7-col 2x2 Core Metrics -->
        <div class="grid grid-cols-1 gap-5 lg:grid-cols-12">
            <!-- Left 5 Cols: Gateway Live Command Hero Card -->
            <div
              class="relative flex flex-col justify-between overflow-hidden rounded-3xl bg-gradient-to-br from-dark-900 via-dark-800 to-dark-950 p-6 text-white shadow-glass ring-1 ring-amber-500/25 lg:col-span-5"
            >
              <div class="pointer-events-none absolute -right-12 -top-12 h-48 w-48 rounded-full bg-amber-500/20 blur-3xl"></div>
              <div class="pointer-events-none absolute -bottom-14 -left-14 h-44 w-44 rounded-full bg-orange-500/15 blur-3xl"></div>

              <div class="relative z-10">
                <div class="flex items-center justify-between gap-2">
                  <span class="inline-flex items-center gap-2 rounded-full bg-amber-500/15 px-3 py-1 text-xs font-semibold text-amber-300 ring-1 ring-amber-400/25">
                    <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    AgentByte Gateway Core
                  </span>
                  <div class="flex items-center gap-2 rounded-full bg-white/[0.06] px-3 py-1 text-xs font-medium text-amber-200 ring-1 ring-white/10">
                    <Icon name="bolt" size="xs" class="text-amber-400" />
                    <span>{{ formatTokens(stats.rpm) }} RPM</span>
                    <span class="text-white/30">·</span>
                    <span>{{ formatTokens(stats.tpm) }} TPM</span>
                  </div>
                </div>

                <!-- Today Core Volume & Actual Cost -->
                <div class="mt-5 grid grid-cols-3 gap-3">
                  <div class="rounded-2xl bg-white/[0.05] p-3.5 ring-1 ring-white/[0.08]">
                    <p class="text-[11px] font-medium text-gray-400">{{ t('admin.dashboard.todayRequests') }}</p>
                    <p class="mt-1 text-2xl font-extrabold tracking-tight text-white">
                      {{ formatNumber(stats.today_requests) }}
                    </p>
                    <p class="mt-0.5 text-[11px] text-gray-400">
                      {{ t('common.total') }} {{ formatNumber(stats.total_requests) }}
                    </p>
                  </div>
                  <div class="rounded-2xl bg-white/[0.05] p-3.5 ring-1 ring-white/[0.08]">
                    <p class="text-[11px] font-medium text-gray-400">{{ t('admin.dashboard.todayTokens') }}</p>
                    <p class="mt-1 text-2xl font-extrabold tracking-tight text-amber-400">
                      {{ formatTokens(stats.today_tokens) }}
                    </p>
                    <p class="mt-0.5 text-[11px] text-gray-400">
                      {{ t('common.total') }} {{ formatTokens(stats.total_tokens) }}
                    </p>
                  </div>
                  <div class="rounded-2xl bg-white/[0.05] p-3.5 ring-1 ring-white/[0.08]">
                    <p class="text-[11px] font-medium text-gray-400">{{ t('admin.dashboard.actual') }}</p>
                    <p class="mt-1 text-2xl font-extrabold tracking-tight text-emerald-400">
                      ¥{{ formatCost(stats.today_actual_cost) }}
                    </p>
                    <p class="mt-0.5 text-[11px] text-gray-400">
                      {{ t('common.total') }} ¥{{ formatCost(stats.total_actual_cost) }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Quick Gateway Shortcuts inside Hero Bento -->
              <div class="relative z-10 mt-5 flex flex-wrap items-center gap-2.5 border-t border-white/10 pt-4">
                <button
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 px-3.5 py-2 text-xs font-semibold text-white shadow-md shadow-amber-500/25 transition-all hover:-translate-y-0.5"
                  @click="router.push('/admin/accounts')"
                >
                  <Icon name="server" size="sm" :stroke-width="2" />
                  {{ t('admin.dashboard.accounts') }}
                </button>
                <button
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-2xl bg-white/10 px-3.5 py-2 text-xs font-semibold text-white ring-1 ring-white/15 backdrop-blur-md transition-all hover:bg-white/15"
                  @click="router.push('/admin/groups')"
                >
                  <Icon name="grid" size="sm" :stroke-width="2" />
                  {{ t('admin.dashboard.groupPricing') }}
                </button>
                <button
                  v-if="canUseBatchImage"
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-2xl bg-white/10 px-3.5 py-2 text-xs font-semibold text-amber-200 ring-1 ring-white/15 backdrop-blur-md transition-all hover:bg-white/15"
                  @click="router.push('/batch-image')"
                >
                  <Icon name="sparkles" size="sm" :stroke-width="2" />
                  {{ t('admin.dashboard.batchImage') }}
                </button>
              </div>
            </div>

            <!-- Right 7 Cols: 2x2 Bento Stat Grid -->
            <div class="grid grid-cols-2 gap-4 lg:col-span-7">
              <!-- Service Accounts Pool -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-dark-400">
                    {{ t('admin.dashboard.accounts') }}
                  </span>
                  <div class="rounded-2xl bg-gradient-to-br from-orange-500/15 to-amber-500/10 p-2.5 text-orange-600 ring-1 ring-orange-500/20 dark:text-orange-400">
                    <Icon name="server" size="md" :stroke-width="2" />
                  </div>
                </div>
                <div class="mt-3">
                  <p class="text-3xl font-extrabold tracking-tight text-gray-900 dark:text-white">
                    {{ stats.total_accounts }}
                  </p>
                  <p class="mt-1.5 text-xs">
                    <span class="font-semibold text-emerald-600 dark:text-emerald-400">
                      {{ stats.normal_accounts }} {{ t('common.active') }}
                    </span>
                    <span v-if="stats.error_accounts > 0" class="ml-1.5 font-semibold text-red-500">
                      · {{ stats.error_accounts }} {{ t('common.error') }}
                    </span>
                  </p>
                </div>
              </div>

              <!-- Total API Keys -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-dark-400">
                    {{ t('admin.dashboard.apiKeys') }}
                  </span>
                  <div class="rounded-2xl bg-gradient-to-br from-amber-500/15 to-orange-500/10 p-2.5 text-amber-600 ring-1 ring-amber-500/20 dark:text-amber-400">
                    <Icon name="key" size="md" :stroke-width="2" />
                  </div>
                </div>
                <div class="mt-3">
                  <p class="text-3xl font-extrabold tracking-tight text-gray-900 dark:text-white">
                    {{ stats.total_api_keys }}
                  </p>
                  <p class="mt-1.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                    {{ stats.active_api_keys }} {{ t('common.active') }}
                  </p>
                </div>
              </div>

              <!-- Users & Active Users -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-dark-400">
                    {{ t('admin.dashboard.users') }}
                  </span>
                  <div class="rounded-2xl bg-gradient-to-br from-amber-500/15 to-yellow-500/10 p-2.5 text-amber-600 ring-1 ring-amber-500/20 dark:text-amber-400">
                    <Icon name="userPlus" size="md" :stroke-width="2" />
                  </div>
                </div>
                <div class="mt-3">
                  <div class="flex items-baseline gap-2">
                    <p class="text-3xl font-extrabold tracking-tight text-gray-900 dark:text-white">
                      {{ formatNumber(stats.total_users) }}
                    </p>
                    <span class="rounded-full bg-amber-500/15 px-2 py-0.5 text-xs font-bold text-amber-600 dark:text-amber-400">
                      +{{ stats.today_new_users }}
                    </span>
                  </div>
                  <p class="mt-1.5 text-xs text-gray-500 dark:text-dark-400">
                    {{ stats.active_users }} {{ t('admin.dashboard.activeUsers') }}
                  </p>
                </div>
              </div>

              <!-- Avg Response Time & Cost Breakdown -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-dark-400">
                    {{ t('admin.dashboard.avgResponse') }}
                  </span>
                  <div class="rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 p-2.5 text-emerald-600 ring-1 ring-emerald-500/20 dark:text-emerald-400">
                    <Icon name="clock" size="md" :stroke-width="2" />
                  </div>
                </div>
                <div class="mt-3">
                  <p class="text-3xl font-extrabold tracking-tight text-gray-900 dark:text-white">
                    {{ formatDuration(stats.average_duration_ms) }}
                  </p>
                  <p class="mt-1.5 text-xs text-gray-500 dark:text-dark-400">
                    {{ t('admin.dashboard.accountCost') }} ¥{{ formatCost(stats.today_account_cost) }} · {{ t('admin.dashboard.standard') }} ¥{{ formatCost(stats.today_cost) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Charts Section (Layout A) -->
          <div class="space-y-6">
            <!-- Date Range Filter -->
            <div class="card p-4">
              <div class="flex flex-wrap items-center gap-4">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300"
                    >{{ t('admin.dashboard.timeRange') }}:</span
                  >
                  <DateRangePicker
                    v-model:start-date="startDate"
                    v-model:end-date="endDate"
                    @change="onDateRangeChange"
                  />
                </div>
                <button @click="loadDashboardStats" :disabled="chartsLoading" class="btn btn-secondary">
                  {{ t('common.refresh') }}
                </button>
                <div class="ml-auto flex items-center gap-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300"
                    >{{ t('admin.dashboard.granularity') }}:</span
                  >
                  <div class="w-28">
                    <Select
                      v-model="granularity"
                      :options="granularityOptions"
                      @change="loadChartData"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Charts Grid (2 Columns) -->
            <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <ModelDistributionChart
                :model-stats="modelStats"
                :enable-ranking-view="true"
                :ranking-items="rankingItems"
                :ranking-total-actual-cost="rankingTotalActualCost"
                :ranking-total-requests="rankingTotalRequests"
                :ranking-total-tokens="rankingTotalTokens"
                :loading="chartsLoading"
                :ranking-loading="rankingLoading"
                :ranking-error="rankingError"
                :start-date="startDate"
                :end-date="endDate"
                @ranking-click="goToUserUsage"
              />
              <TokenUsageTrend :trend-data="trendData" :loading="chartsLoading" />
            </div>

            <!-- User Usage Trend (Full Width) -->
            <div class="card p-5">
              <div class="mb-4 flex items-center justify-between gap-3">
                <h3 class="text-sm font-semibold text-gray-900 dark:text-white">{{ t('admin.dashboard.recentUsage') }} (Top 12)</h3>
                <div class="flex gap-1 rounded-xl border border-black/[0.06] bg-gray-100/70 p-0.5 dark:border-white/[0.08] dark:bg-dark-800/70" role="group" :aria-label="t('admin.dashboard.recentUsage')">
                  <button v-for="metric in (['tokens', 'actual_cost'] as const)" :key="metric" type="button"
                    class="rounded-lg px-2.5 py-1 text-xs font-medium transition-all" :class="userTrendMetric === metric ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-sm' : 'text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white'"
                    :aria-pressed="userTrendMetric === metric" @click="setUserTrendMetric(metric)">
                    {{ t(metric === 'tokens' ? 'admin.dashboard.tokens' : 'admin.dashboard.actualSpending') }}
                  </button>
                </div>
              </div>
              <div class="h-64">
                <div v-if="userTrendLoading" class="flex h-full items-center justify-center">
                  <LoadingSpinner size="md" />
                </div>
                <Line v-else-if="userTrendChartData" :data="userTrendChartData" :options="lineOptions" />
                <div
                  v-else
                  class="flex h-full items-center justify-center text-sm text-gray-500 dark:text-gray-400"
                >
                  {{ t('admin.dashboard.noDataAvailable') }}
                </div>
              </div>
            </div>
          </div>
      </template>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

const { t } = useI18n()
import { adminAPI } from '@/api/admin'
import type {
  DashboardStats,
  TrendDataPoint,
  ModelStat,
  UserUsageTrendPoint,
  UserSpendingRankingItem
} from '@/types'
import AppLayout from '@/components/layout/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import Icon from '@/components/icons/Icon.vue'
import DateRangePicker from '@/components/common/DateRangePicker.vue'
import Select from '@/components/common/Select.vue'
import ModelDistributionChart from '@/components/charts/ModelDistributionChart.vue'
import TokenUsageTrend from '@/components/charts/TokenUsageTrend.vue'
import { useBatchImageAccess } from '@/composables/useBatchImageAccess'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
)

const appStore = useAppStore()
const router = useRouter()
const { canUseBatchImage, refreshBatchImageAccess } = useBatchImageAccess()
const stats = ref<DashboardStats | null>(null)
const loading = ref(false)
const chartsLoading = ref(false)
const userTrendLoading = ref(false)
const rankingLoading = ref(false)
const rankingError = ref(false)

// Chart data
const trendData = ref<TrendDataPoint[]>([])
const modelStats = ref<ModelStat[]>([])
const userTrend = ref<UserUsageTrendPoint[]>([])
const userTrendMetric = ref<'tokens' | 'actual_cost'>('tokens')
const rankingItems = ref<UserSpendingRankingItem[]>([])
const rankingTotalActualCost = ref(0)
const rankingTotalRequests = ref(0)
const rankingTotalTokens = ref(0)
let chartLoadSeq = 0
let usersTrendLoadSeq = 0
let rankingLoadSeq = 0
const rankingLimit = 12

// Helper function to format date in local timezone
const formatLocalDate = (date: Date): string => {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const getLast24HoursRangeDates = (): { start: string; end: string } => {
  const end = new Date()
  const start = new Date(end.getTime() - 24 * 60 * 60 * 1000)
  return {
    start: formatLocalDate(start),
    end: formatLocalDate(end)
  }
}

// Date range
const granularity = ref<'day' | 'hour'>('hour')
const defaultRange = getLast24HoursRangeDates()
const startDate = ref(defaultRange.start)
const endDate = ref(defaultRange.end)

// Granularity options for Select component
const granularityOptions = computed(() => [
  { value: 'day', label: t('admin.dashboard.day') },
  { value: 'hour', label: t('admin.dashboard.hour') }
])

// Dark mode detection
const isDarkMode = computed(() => {
  return document.documentElement.classList.contains('dark')
})

// Chart colors
const chartColors = computed(() => ({
  text: isDarkMode.value ? '#e5e7eb' : '#374151',
  grid: isDarkMode.value ? '#374151' : '#e5e7eb'
}))

// Line chart options (for user trend chart)
const lineOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: 'index' as const
  },
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        color: chartColors.value.text,
        usePointStyle: true,
        pointStyle: 'circle',
        padding: 15,
        font: {
          size: 11
        }
      }
    },
    tooltip: {
      itemSort: (a: any, b: any) => {
        const aValue = typeof a?.raw === 'number' ? a.raw : Number(a?.parsed?.y ?? 0)
        const bValue = typeof b?.raw === 'number' ? b.raw : Number(b?.parsed?.y ?? 0)
        return bValue - aValue
      },
      callbacks: {
        label: (context: any) => {
          return `${context.dataset.label}: ${formatUserTrendValue(Number(context.raw))}`
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: chartColors.value.grid
      },
      ticks: {
        color: chartColors.value.text,
        font: {
          size: 10
        }
      }
    },
    y: {
      grid: {
        color: chartColors.value.grid
      },
      ticks: {
        color: chartColors.value.text,
        font: {
          size: 10
        },
        callback: (value: string | number) => formatUserTrendValue(Number(value))
      }
    }
  }
}))

// User trend chart data
const userTrendChartData = computed(() => {
  if (!userTrend.value?.length) return null

  const getDisplayName = (point: UserUsageTrendPoint): string => {
    const username = point.username?.trim()
    if (username) {
      return username
    }

    const email = point.email?.trim()
    if (email) {
      return email
    }

    return t('admin.redeem.userPrefix', { id: point.user_id })
  }

  // Group by user_id to avoid merging different users with the same display name
  const userGroups = new Map<number, { name: string; data: Map<string, number> }>()
  const allDates = new Set<string>()

  userTrend.value.forEach((point) => {
    allDates.add(point.date)
    const key = point.user_id
    if (!userGroups.has(key)) {
      userGroups.set(key, { name: getDisplayName(point), data: new Map() })
    }
    userGroups.get(key)!.data.set(point.date, userTrendMetric.value === 'tokens' ? point.tokens : point.actual_cost)
  })

  const sortedDates = Array.from(allDates).sort()
  const colors = [
    '#f59e0b',
    '#ea580c',
    '#10b981',
    '#fbbf24',
    '#f97316',
    '#8b5cf6',
    '#ec4899',
    '#14b8a6',
    '#ef4444',
    '#6366f1',
    '#84cc16',
    '#06b6d4'
  ]

  const datasets = Array.from(userGroups.values()).map((group, idx) => ({
    label: group.name,
    data: sortedDates.map((date) => group.data.get(date) || 0),
    borderColor: colors[idx % colors.length],
    backgroundColor: `${colors[idx % colors.length]}20`,
    fill: false,
    tension: 0.3
  }))

  return {
    labels: sortedDates,
    datasets
  }
})

// Format helpers
const formatUserTrendValue = (value: number): string =>
  userTrendMetric.value === 'tokens' ? formatTokens(value) : `¥${formatCost(value)}`

const formatTokens = (value: number | undefined): string => {
  if (value === undefined || value === null) return '0'
  if (value >= 1_000_000_000) {
    return `${(value / 1_000_000_000).toFixed(2)}B`
  } else if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(2)}M`
  } else if (value >= 1_000) {
    return `${(value / 1_000).toFixed(2)}K`
  }
  return value.toLocaleString()
}

const toFiniteNumber = (value: unknown): number => {
  const numberValue = Number(value)
  return Number.isFinite(numberValue) ? numberValue : 0
}

const formatNumber = (value: number | null | undefined): string => {
  return toFiniteNumber(value).toLocaleString()
}

const formatCost = (value: number | null | undefined): string => {
  const safeValue = toFiniteNumber(value)
  if (safeValue >= 1000) {
    return (safeValue / 1000).toFixed(2) + 'K'
  } else if (safeValue >= 1) {
    return safeValue.toFixed(2)
  } else if (safeValue >= 0.01) {
    return safeValue.toFixed(3)
  }
  return safeValue.toFixed(4)
}

const formatDuration = (ms: number): string => {
  if (ms >= 1000) {
    return `${(ms / 1000).toFixed(2)}s`
  }
  return `${Math.round(ms)}ms`
}

const goToUserUsage = (item: UserSpendingRankingItem) => {
  void router.push({
    path: '/admin/usage',
    query: {
      user_id: String(item.user_id),
      start_date: startDate.value,
      end_date: endDate.value
    }
  })
}

// Date range change handler
const onDateRangeChange = (range: {
  startDate: string
  endDate: string
  preset: string | null
}) => {
  // Auto-select granularity based on date range
  const start = new Date(range.startDate)
  const end = new Date(range.endDate)
  const daysDiff = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))

  // If range is 1 day, use hourly granularity
  if (daysDiff <= 1) {
    granularity.value = 'hour'
  } else {
    granularity.value = 'day'
  }

  loadChartData()
}

// Load data
const loadDashboardSnapshot = async (includeStats: boolean) => {
  const currentSeq = ++chartLoadSeq
  if (includeStats && !stats.value) {
    loading.value = true
  }
  chartsLoading.value = true
  try {
    const response = await adminAPI.dashboard.getSnapshotV2({
      start_date: startDate.value,
      end_date: endDate.value,
      granularity: granularity.value,
      include_stats: includeStats,
      include_trend: true,
      include_model_stats: true,
      include_group_stats: false,
      include_users_trend: false
    })
    if (currentSeq !== chartLoadSeq) return
    if (includeStats && response.stats) {
      stats.value = response.stats
    }
    trendData.value = response.trend || []
    modelStats.value = response.models || []
  } catch (error) {
    if (currentSeq !== chartLoadSeq) return
    appStore.showError(t('admin.dashboard.failedToLoad'))
    console.error('Error loading dashboard snapshot:', error)
  } finally {
    if (currentSeq === chartLoadSeq) {
      loading.value = false
      chartsLoading.value = false
    }
  }
}

const setUserTrendMetric = (metric: 'tokens' | 'actual_cost') => {
  if (userTrendMetric.value === metric) return
  userTrendMetric.value = metric
  userTrend.value = []
  loadUsersTrend()
}

const loadUsersTrend = async () => {
  const currentSeq = ++usersTrendLoadSeq
  userTrendLoading.value = true
  try {
    const response = await adminAPI.dashboard.getUserUsageTrend({
      start_date: startDate.value,
      end_date: endDate.value,
      granularity: granularity.value,
      limit: 12,
      metric: userTrendMetric.value
    })
    if (currentSeq !== usersTrendLoadSeq) return
    userTrend.value = response.trend || []
  } catch (error) {
    if (currentSeq !== usersTrendLoadSeq) return
    console.error('Error loading users trend:', error)
    userTrend.value = []
  } finally {
    if (currentSeq === usersTrendLoadSeq) {
      userTrendLoading.value = false
    }
  }
}

const loadUserSpendingRanking = async () => {
  const currentSeq = ++rankingLoadSeq
  rankingLoading.value = true
  rankingError.value = false
  try {
    const response = await adminAPI.dashboard.getUserSpendingRanking({
      start_date: startDate.value,
      end_date: endDate.value,
      limit: rankingLimit
    })
    if (currentSeq !== rankingLoadSeq) return
    rankingItems.value = response.ranking || []
    rankingTotalActualCost.value = response.total_actual_cost || 0
    rankingTotalRequests.value = response.total_requests || 0
    rankingTotalTokens.value = response.total_tokens || 0
  } catch (error) {
    if (currentSeq !== rankingLoadSeq) return
    console.error('Error loading user spending ranking:', error)
    rankingItems.value = []
    rankingTotalActualCost.value = 0
    rankingTotalRequests.value = 0
    rankingTotalTokens.value = 0
    rankingError.value = true
  } finally {
    if (currentSeq === rankingLoadSeq) {
      rankingLoading.value = false
    }
  }
}

const loadDashboardStats = async () => {
  await Promise.all([
    loadDashboardSnapshot(true),
    loadUsersTrend(),
    loadUserSpendingRanking()
  ])
}

const loadChartData = async () => {
  await Promise.all([
    loadDashboardSnapshot(false),
    loadUsersTrend(),
    loadUserSpendingRanking()
  ])
}

onMounted(() => {
  void refreshBatchImageAccess()
  loadDashboardStats()
})
</script>

<style scoped>
</style>
