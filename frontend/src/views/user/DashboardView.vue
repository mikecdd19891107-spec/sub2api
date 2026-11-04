<template>
  <AppLayout>
    <div class="space-y-6">
      <div v-if="loading && !stats" class="flex items-center justify-center py-12">
        <LoadingSpinner />
      </div>

      <template v-else-if="stats">
        <!-- 新手引导：创建 Key → 配置客户端 → 发出第一个请求 -->
        <UserDashboardGetStarted
          v-if="!authStore.isSimpleMode"
          :total-keys="stats.total_api_keys"
          :total-requests="stats.total_requests"
        />

        <!-- 核心指标 -->
        <section class="grid grid-cols-2 gap-4 lg:grid-cols-4" data-testid="dashboard-kpis">
          <div v-if="!authStore.isSimpleMode" class="card p-5">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-600 dark:text-dark-400">{{ t('dashboard.balance') }}</span>
              <router-link to="/keys" class="text-xs text-gray-500 hover:text-gray-950 dark:text-dark-400 dark:hover:text-white">
                {{ t('dashboard.kpi.keysActive', { active: stats.active_api_keys, total: stats.total_api_keys }) }}
              </router-link>
            </div>
            <div class="mt-1.5 font-mono text-2xl font-semibold tracking-tight text-gray-950 dark:text-white">
              ${{ formatBalance(user?.balance || 0) }}
            </div>
            <div class="mt-3 flex gap-2">
              <router-link v-if="paymentEnabled" to="/purchase" class="btn btn-primary btn-sm">{{ t('nav.recharge') }}</router-link>
              <router-link to="/redeem" class="btn btn-secondary btn-sm">{{ t('nav.redeem') }}</router-link>
            </div>
          </div>

          <div class="card p-5">
            <span class="text-xs text-gray-600 dark:text-dark-400">{{ t('dashboard.todayCost') }}</span>
            <div class="mt-1.5 font-mono text-2xl font-semibold tracking-tight text-gray-950 dark:text-white">
              ${{ formatCost(stats.today_actual_cost) }}
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-dark-400">
              {{ t('dashboard.kpi.costSub', { total: formatCost(stats.total_actual_cost), standard: formatCost(stats.today_cost) }) }}
            </p>
          </div>

          <div class="card p-5">
            <span class="text-xs text-gray-600 dark:text-dark-400">{{ t('dashboard.todayRequests') }}</span>
            <div class="mt-1.5 font-mono text-2xl font-semibold tracking-tight text-gray-950 dark:text-white">
              {{ formatNumber(stats.today_requests) }}
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-dark-400">
              {{ t('dashboard.kpi.requestsSub', { total: formatNumber(stats.total_requests), rpm: formatNumber(Math.round(stats.rpm || 0)) }) }}
            </p>
          </div>

          <div class="card p-5">
            <span class="text-xs text-gray-600 dark:text-dark-400">{{ t('dashboard.todayTokens') }}</span>
            <div class="mt-1.5 font-mono text-2xl font-semibold tracking-tight text-gray-950 dark:text-white">
              {{ formatTokens(stats.today_tokens) }}
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-dark-400">
              {{ t('dashboard.kpi.tokensSub', { total: formatTokens(stats.total_tokens), avg: formatDuration(stats.average_duration_ms) }) }}
            </p>
          </div>
        </section>

        <!-- 用量趋势 + 快速接入 -->
        <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
          <div class="min-w-0 xl:col-span-2">
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
          <div class="min-w-0">
            <UserDashboardQuickConnect />
          </div>
        </div>

        <!-- 按平台拆分（含平台额度） -->
        <UserDashboardStats
          v-if="!authStore.isSimpleMode"
          platforms-only
          :stats="stats"
          :balance="user?.balance || 0"
          :is-simple="authStore.isSimpleMode"
          :platform-quotas="platformQuotas"
        />

        <!-- 最近请求 + 快捷操作 -->
        <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
          <div class="min-w-0 xl:col-span-2">
            <UserDashboardRecentUsage :data="recentUsage" :loading="loadingUsage" />
          </div>
          <div class="min-w-0">
            <UserDashboardQuickActions />
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
import { getMyPlatformQuotas } from '@/api/user'
import AppLayout from '@/components/layout/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import UserDashboardGetStarted from '@/components/user/dashboard/UserDashboardGetStarted.vue'
import UserDashboardQuickConnect from '@/components/user/dashboard/UserDashboardQuickConnect.vue'
import UserDashboardStats from '@/components/user/dashboard/UserDashboardStats.vue'
import UserDashboardCharts from '@/components/user/dashboard/UserDashboardCharts.vue'
import UserDashboardRecentUsage from '@/components/user/dashboard/UserDashboardRecentUsage.vue'
import UserDashboardQuickActions from '@/components/user/dashboard/UserDashboardQuickActions.vue'
import type { UsageLog, TrendDataPoint, ModelStat, PlatformQuotaItem } from '@/types'
import { formatDateLocalInput } from '@/utils/format'
import { FeatureFlags, isFeatureFlagEnabled } from '@/utils/featureFlags'

const { t } = useI18n()
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const paymentEnabled = computed(() => isFeatureFlagEnabled(FeatureFlags.payment))

const stats = ref<UserStatsType | null>(null)
const loading = ref(false)
const loadingUsage = ref(false)
const loadingCharts = ref(false)
const trendData = ref<TrendDataPoint[]>([])
const modelStats = ref<ModelStat[]>([])
const recentUsage = ref<UsageLog[]>([])
const platformQuotas = ref<PlatformQuotaItem[] | null>(null)

const startDate = ref(formatDateLocalInput(new Date(Date.now() - 6 * 86400000)))
const endDate = ref(formatDateLocalInput(new Date()))
const granularity = ref('day')

const usdFormatter = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

function formatBalance(val: number): string {
  return usdFormatter.format(Number(val || 0))
}

function formatNumber(val: number | undefined): string {
  return Number(val || 0).toLocaleString()
}

// 金额统一两位小数；不足 1 分的小额保留 4 位，避免显示成 0.00
function formatCost(val: number | undefined): string {
  const n = Number(val || 0)
  if (n === 0) return '0.00'
  return n < 0.01 ? n.toFixed(4) : usdFormatter.format(n)
}

function formatTokens(val: number | undefined): string {
  const n = Number(val || 0)
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(2)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return n.toLocaleString()
}

function formatDuration(ms: number | undefined): string {
  const n = Number(ms || 0)
  return n >= 1000 ? `${(n / 1000).toFixed(2)} s` : `${Math.round(n)} ms`
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
        granularity: granularity.value as 'day' | 'hour'
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
    recentUsage.value = res.items.slice(0, 6)
  } catch (error) {
    console.error('Failed to load recent usage:', error)
  } finally {
    loadingUsage.value = false
  }
}

const loadPlatformQuotas = async () => {
  try {
    const data = await getMyPlatformQuotas()
    platformQuotas.value = data.platform_quotas ?? []
  } catch (error) {
    console.warn('Failed to load platform quotas:', error)
    platformQuotas.value = []
  }
}

const refreshAll = () => {
  loadStats()
  loadCharts()
  loadRecent()
  loadPlatformQuotas()
}

onMounted(() => {
  refreshAll()
})
</script>
