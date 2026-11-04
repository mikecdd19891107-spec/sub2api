<template>
  <AppLayout>
    <div class="space-y-6">
      <div v-if="loading" class="flex items-center justify-center py-12">
        <LoadingSpinner />
      </div>

      <template v-else-if="stats">
        <!-- VisionOS Bento 便当盒工作台 -->
        <div class="grid grid-cols-1 gap-5 lg:grid-cols-12">
            <!-- Left Hero Bento Card: Balance + Quick Actions (5 cols) -->
            <div
              class="relative overflow-hidden rounded-3xl border border-amber-500/25 bg-gradient-to-br from-[#1C1815] via-[#251E18] to-[#171412] p-6 text-white shadow-glass lg:col-span-5"
            >
              <div class="pointer-events-none absolute -right-12 -top-12 h-44 w-44 rounded-full bg-amber-500/25 blur-3xl"></div>
              <div class="pointer-events-none absolute -bottom-12 -left-12 h-36 w-36 rounded-full bg-orange-500/20 blur-2xl"></div>

              <div class="relative z-10 flex h-full flex-col justify-between gap-6">
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <span class="inline-flex items-center gap-1.5 rounded-full bg-amber-500/20 px-3 py-1 text-[11px] font-semibold text-amber-300 ring-1 ring-amber-400/30">
                      <span class="h-1.5 w-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                      {{ t('dashboard.balance') }}
                    </span>
                    <div class="mt-3 flex items-baseline gap-2">
                      <span class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
                        ${{ formatBalance(user?.balance || 0) }}
                      </span>
                      <span class="text-xs text-stone-400">USD</span>
                    </div>
                  </div>

                  <div class="rounded-2xl bg-white/10 px-3.5 py-2 text-right backdrop-blur-md ring-1 ring-white/15">
                    <p class="text-[11px] text-stone-300">{{ t('dashboard.apiKeys') }}</p>
                    <p class="text-sm font-bold text-amber-300">
                      {{ stats.active_api_keys }} / {{ stats.total_api_keys }} {{ t('common.active') }}
                    </p>
                  </div>
                </div>

                <!-- Streamlined Direct Actions -->
                <div class="flex flex-wrap items-center gap-2.5">
                  <router-link
                    to="/keys"
                    class="inline-flex items-center gap-1.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-amber-500/25 transition-all hover:-translate-y-0.5 hover:shadow-lg"
                  >
                    <Icon name="key" size="sm" />
                    {{ t('nav.apiKeys') }}
                  </router-link>
                  <router-link
                    v-if="!authStore.isSimpleMode"
                    to="/purchase"
                    class="inline-flex items-center gap-1.5 rounded-2xl bg-white/12 px-4 py-2 text-xs font-semibold text-white ring-1 ring-white/20 backdrop-blur-md transition-all hover:bg-white/20"
                  >
                    <Icon name="dollar" size="sm" />
                    {{ t('nav.recharge') }}
                  </router-link>
                  <router-link
                    v-if="!authStore.isSimpleMode"
                    to="/redeem"
                    class="inline-flex items-center gap-1.5 rounded-2xl bg-white/10 px-3.5 py-2 text-xs font-medium text-stone-200 ring-1 ring-white/15 backdrop-blur-md transition-all hover:bg-white/15"
                  >
                    {{ t('nav.redeem') }}
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Right 3 Streamlined Core Metric Cards (7 cols) -->
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-3 lg:col-span-7">
              <!-- Today Requests -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-500 dark:text-dark-400">
                    {{ t('dashboard.todayRequests') }}
                  </span>
                  <div class="rounded-2xl bg-amber-500/15 p-2.5 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400">
                    <Icon name="chart" size="sm" :stroke-width="2" />
                  </div>
                </div>
                <div class="my-3">
                  <p class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {{ formatNumber(stats.today_requests) }}
                  </p>
                  <p class="mt-1 text-xs text-gray-500 dark:text-dark-400">
                    {{ t('common.total') }}: {{ formatNumber(stats.total_requests) }}
                  </p>
                </div>
                <div class="flex items-center justify-between border-t border-black/[0.04] pt-2.5 text-xs dark:border-white/[0.06]">
                  <span class="text-gray-400">实时速率</span>
                  <span class="font-semibold text-amber-600 dark:text-amber-400">{{ stats.rpm || 0 }} RPM</span>
                </div>
              </div>

              <!-- Today Cost -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-500 dark:text-dark-400">
                    {{ t('dashboard.todayCost') }}
                  </span>
                  <div class="rounded-2xl bg-orange-500/15 p-2.5 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400">
                    <Icon name="dollar" size="sm" :stroke-width="2" />
                  </div>
                </div>
                <div class="my-3">
                  <p class="text-2xl font-bold tracking-tight text-orange-600 dark:text-orange-400">
                    ${{ formatCost(stats.today_actual_cost) }}
                  </p>
                  <p class="mt-1 text-xs text-gray-500 dark:text-dark-400">
                    {{ t('common.total') }}: ${{ formatCost(stats.total_actual_cost) }}
                  </p>
                </div>
                <div class="flex items-center justify-between border-t border-black/[0.04] pt-2.5 text-xs dark:border-white/[0.06]">
                  <span class="text-gray-400">标准折算</span>
                  <span class="font-medium text-gray-600 dark:text-dark-300">${{ formatCost(stats.today_cost) }}</span>
                </div>
              </div>

              <!-- Today Tokens -->
              <div class="card flex flex-col justify-between p-5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-500 dark:text-dark-400">
                    {{ t('dashboard.todayTokens') }}
                  </span>
                  <div class="rounded-2xl bg-emerald-500/15 p-2.5 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400">
                    <Icon name="cube" size="sm" :stroke-width="2" />
                  </div>
                </div>
                <div class="my-3">
                  <p class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {{ formatTokens(stats.today_tokens) }}
                  </p>
                  <p class="mt-1 text-xs text-gray-500 dark:text-dark-400">
                    {{ t('common.total') }}: {{ formatTokens(stats.total_tokens) }}
                  </p>
                </div>
                <div class="flex items-center justify-between border-t border-black/[0.04] pt-2.5 text-xs dark:border-white/[0.06]">
                  <span class="text-gray-400">{{ t('dashboard.avgResponse') }}</span>
                  <span class="font-semibold text-emerald-600 dark:text-emerald-400">{{ Math.round(stats.average_duration_ms || 0) }} ms</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Streamlined Row: Charts + Recent Calls -->
          <div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
            <div class="lg:col-span-7">
              <UserDashboardCharts
                v-model:startDate="startDate"
                v-model:endDate="endDate"
                v-model:granularity="granularity"
                :loading="loadingCharts"
                :trend="trendData"
                :models="modelStats"
                @dateRangeChange="loadCharts"
                @granularityChange="loadCharts"
                @refresh="refreshAll"
              />
            </div>
            <div class="lg:col-span-5">
              <UserDashboardRecentUsage :data="recentUsage" :loading="loadingUsage" />
            </div>
          </div>
      </template>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { usageAPI, type UserDashboardStats as UserStatsType } from '@/api/usage'
import AppLayout from '@/components/layout/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import Icon from '@/components/icons/Icon.vue'
import UserDashboardCharts from '@/components/user/dashboard/UserDashboardCharts.vue'
import UserDashboardRecentUsage from '@/components/user/dashboard/UserDashboardRecentUsage.vue'
import type { UsageLog, TrendDataPoint, ModelStat } from '@/types'
import { formatDateLocalInput } from '@/utils/format'

const { t } = useI18n()
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const stats = ref<UserStatsType | null>(null)
const loading = ref(false)
const loadingUsage = ref(false)
const loadingCharts = ref(false)
const trendData = ref<TrendDataPoint[]>([])
const modelStats = ref<ModelStat[]>([])
const recentUsage = ref<UsageLog[]>([])

const startDate = ref(formatDateLocalInput(new Date(Date.now() - 6 * 86400000)))
const endDate = ref(formatDateLocalInput(new Date()))
const granularity = ref('day')

function formatBalance(val: number): string {
  return Number(val || 0).toFixed(2)
}

function formatNumber(val: number | undefined): string {
  return Number(val || 0).toLocaleString()
}

function formatCost(val: number | undefined): string {
  const n = Number(val || 0)
  return n >= 1 ? n.toFixed(2) : n.toFixed(4)
}

function formatTokens(val: number | undefined): string {
  const n = Number(val || 0)
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(2)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return n.toLocaleString()
}

const loadStats = async () => {
  loading.value = true
  try {
    await authStore.refreshUser()
    stats.value = await usageAPI.getDashboardStats()
  } catch (error) {
    console.error('Failed to load dashboard stats:', error)
  } finally {
    loading.value = false
  }
}

const loadCharts = async () => {
  loadingCharts.value = true
  try {
    const res = await Promise.all([
      usageAPI.getDashboardTrend({
        start_date: startDate.value,
        end_date: endDate.value,
        granularity: granularity.value as any
      }),
      usageAPI.getDashboardModels({ start_date: startDate.value, end_date: endDate.value })
    ])
    trendData.value = res[0].trend || []
    modelStats.value = res[1].models || []
  } catch (error) {
    console.error('Failed to load charts:', error)
  } finally {
    loadingCharts.value = false
  }
}

const loadRecent = async () => {
  loadingUsage.value = true
  try {
    const res = await usageAPI.getByDateRange(startDate.value, endDate.value)
    recentUsage.value = res.items.slice(0, 5)
  } catch (error) {
    console.error('Failed to load recent usage:', error)
  } finally {
    loadingUsage.value = false
  }
}

const refreshAll = () => {
  loadStats()
  loadCharts()
  loadRecent()
}

onMounted(() => {
  refreshAll()
})
</script>
