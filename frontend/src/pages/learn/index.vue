<template>
  <view class="page-learn">
    <!-- 顶部：习本标题 -->
    <view class="hero">
      <view class="hero__meta">
        <text class="hero__meta-line"></text>
        <text class="hero__meta-text">STUDY · 学习</text>
      </view>
      <text class="hero__title">日积月累</text>
    </view>

    <!-- 统计：衬线数字三联 -->
    <view class="stats">
      <view class="stats__item">
        <text class="stats__value">{{ identifyCount }}</text>
        <text class="stats__label">识</text>
      </view>
      <view class="stats__divider"></view>
      <view class="stats__item">
        <text class="stats__value">{{ favoriteCount }}</text>
        <text class="stats__label">藏</text>
      </view>
      <view class="stats__divider"></view>
      <view class="stats__item">
        <text class="stats__value">{{ viewCount }}</text>
        <text class="stats__label">览</text>
      </view>
    </view>

    <!-- 收藏入口 -->
    <view class="entry" @click="goFavorites">
      <view class="entry__seal">
        <text class="entry__seal-char">藏</text>
      </view>
      <view class="entry__body">
        <text class="entry__title">我的收藏</text>
        <text class="entry__desc">共 {{ favoriteCount }} 味药材</text>
      </view>
      <text class="entry__arrow">→</text>
    </view>

    <!-- 学习进度可视化 -->
    <view class="progress-section">
      <view class="progress-section__head">
        <text class="progress-section__title">学习足迹</text>
        <text class="progress-section__streak">已连续 {{ streakDays }} 天</text>
      </view>
      <view class="progress-dots">
        <view
          class="progress-dot"
          v-for="(day, index) in weekDays"
          :key="index"
          :class="{
            'progress-dot--active': day.active,
            'progress-dot--today': day.isToday
          }"
        >
          <text class="progress-dot__label">{{ day.label }}</text>
          <view class="progress-dot__circle">
            <text v-if="day.active" class="progress-dot__check">✓</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 最近浏览 -->
    <view class="section">
      <view class="section__head">
        <view class="section__title-wrap">
          <text class="section__bar"></text>
          <text class="section__title">近览</text>
        </view>
        <text class="section__clear" v-if="recentViewed.length" @click="onClearRecent">清空</text>
      </view>

      <view class="history-list" v-if="recentViewed.length">
        <view
          class="history-item"
          v-for="(item, index) in recentViewed"
          :key="item.id || index"
          @click="goDetail(item)"
        >
          <text class="history-item__idx">{{ String(index + 1).padStart(2, '0') }}</text>
          <view class="history-item__body">
            <text class="history-item__name">{{ item.name }}</text>
            <text class="history-item__meta">{{ item.category_part || '草本' }}</text>
          </view>
          <view class="history-item__line" v-if="index < recentViewed.length - 1"></view>
        </view>
      </view>
      <view class="empty-tip" v-else>
        <text class="empty-tip__text">— 尚无浏览记录 —</text>
      </view>
    </view>

    <!-- 推荐学习 -->
    <view class="section">
      <view class="section__head">
        <view class="section__title-wrap">
          <text class="section__bar section__bar--gold"></text>
          <text class="section__title">推荐</text>
        </view>
        <text class="section__hint">每日识一味</text>
      </view>

      <scroll-view class="recommend-scroll" scroll-x enable-flex v-if="recommendList.length">
        <view
          class="recommend-card"
          v-for="(item, index) in recommendList"
          :key="item.id || index"
          @click="goDetail(item)"
        >
          <view class="recommend-card__img-wrap">
            <image v-if="item.image && !item.image.includes('placeholder')" :src="item.image" mode="aspectFill" class="recommend-card__img" />
            <view v-else class="recommend-card__img-placeholder">
              <text class="recommend-card__img-placeholder-text">{{ item.name }}</text>
            </view>
            <view class="recommend-card__seal">
              <text class="recommend-card__seal-text">{{ String(index + 1).padStart(2, '0') }}</text>
            </view>
          </view>
          <view class="recommend-card__body">
            <text class="recommend-card__name">{{ item.name }}</text>
            <text class="recommend-card__efficacy">{{ item.efficacy || '草本药材' }}</text>
          </view>
        </view>
      </scroll-view>
      <view class="empty-tip" v-else>
        <text class="empty-tip__text">— 正在采撷 —</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 习本 · 墨韵版
 */
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useHerbStore } from '@/store/herb'
import { getFavorites, getRecords } from '@/api/user'
import { getHerbs } from '@/api/knowledge'
import { resolveImageUrl } from '@/utils/common'

const herbStore = useHerbStore()

const favoriteCount = ref(0)
const identifyCount = ref(0)
const viewCount = ref(0)
const recentViewed = ref([])
const recommendList = ref([])
const streakDays = ref(0)
const weekDays = ref([])

onShow(() => {
  recentViewed.value = herbStore.recentViewed
  viewCount.value = herbStore.recentViewed.length
  recordTodayStudy()
  loadStats()
  loadRecommend()
  calcStreak()
})

async function loadStats() {
  try {
    const [favData, recData] = await Promise.all([
      getFavorites({ page: 1, pageSize: 1 }),
      getRecords({ page: 1, pageSize: 1 })
    ])
    favoriteCount.value = favData.total || (favData.items || []).length
    identifyCount.value = recData.total || (recData.items || []).length
  } catch (err) {}
}

async function loadRecommend() {
  try {
    const data = await getHerbs({ page: 1, pageSize: 100 })
    const all = data.items || data.list || data || []
    const viewed = herbStore.recentViewed || []
    const viewedIds = new Set(viewed.map((item) => item.id))

    const favorites = (() => {
      try {
        return (JSON.parse(uni.getStorageSync('favorites') || '[]') || []).map((item) => item.id)
      } catch {
        return []
      }
    })()
    const favoriteIds = new Set(favorites)

    const viewedHerbs = all.filter((item) => viewedIds.has(item.id))
    const parts = new Set(viewedHerbs.map((item) => item.category_part || item.part_used).filter(Boolean))
    const effects = new Set(viewedHerbs.map((item) => item.category_efficacy).filter(Boolean))
    const viewedParts = new Set(viewedHerbs.map((item) => item.category_part || item.part_used).filter(Boolean))
    const viewedEffects = new Set(viewedHerbs.map((item) => item.category_efficacy).filter(Boolean))

    const scored = all
      .filter((item) => !viewedIds.has(item.id))
      .map((item) => {
        let score = 0
        if (parts.has(item.category_part || item.part_used)) score += 2
        if (effects.has(item.category_efficacy)) score += 2
        if (viewedParts.has(item.category_part || item.part_used)) score += 1
        if (viewedEffects.has(item.category_efficacy)) score += 1
        if (favoriteIds.has(item.id)) score += 1
        return { item, score }
      })
      .sort((a, b) => b.score - a.score)

    const picks = scored.filter((x) => x.score > 0).slice(0, 4)
    const pool = picks.map((x) => x.item)

    if (pool.length < 4) {
      const seen = new Set(pool.map((item) => item.id))
      for (const h of all) {
        if (!seen.has(h.id) && !viewedIds.has(h.id)) {
          pool.push(h)
          seen.add(h.id)
          if (pool.length >= 4) break
        }
      }
    }

    recommendList.value = pool.slice(0, 4).map((item) => ({
      ...item,
      image: resolveImageUrl(item.image_main || item.image),
      category_part: item.category_part || item.part_used || '草本',
      efficacy: item.efficacy || item.nature_taste || '草本药材'
    }))
  } catch (err) {}
}

function goFavorites() {
  uni.navigateTo({ url: '/pages/learn/favorites' })
}

function onClearRecent() {
  herbStore.clearRecentViewed()
  recentViewed.value = []
  viewCount.value = 0
}

function goDetail(item) {
  uni.navigateTo({ url: `/pages/knowledge/detail?id=${item.id}` })
}

/**
 * 记录今天的学习足迹（按天去重）
 * 只要用户进过学习页（tab 切换、切后台回来都算）就记一次
 */
function recordTodayStudy() {
  const d = new Date()
  const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  try {
    const raw = uni.getStorageSync('studyLog') || {}
    // 兜底：兼容旧数据可能是数组/字符串
    let log = {}
    if (typeof raw === 'object' && !Array.isArray(raw)) {
      log = raw
    } else if (typeof raw === 'string') {
      try { log = JSON.parse(raw) || {} } catch { log = {} }
    }
    if (log[key]) return // 今天已记过
    log[key] = true
    // 只保留最近 60 天的记录，避免 storage 无限增长
    const keys = Object.keys(log).sort()
    if (keys.length > 60) {
      const trimmed = {}
      keys.slice(-60).forEach((k) => { trimmed[k] = true })
      log = trimmed
    }
    uni.setStorageSync('studyLog', log)
  } catch (e) {
    // 静默失败，不影响主流程
  }
}

function getStudyLog() {
  try {
    const raw = uni.getStorageSync('studyLog') || {}
    if (typeof raw === 'object' && !Array.isArray(raw)) return raw
    if (typeof raw === 'string') {
      try { return JSON.parse(raw) || {} } catch { return {} }
    }
    return {}
  } catch {
    return {}
  }
}

function formatDateKey(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function calcStreak() {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime()
  const days = ['日', '一', '二', '三', '四', '五', '六']
  const log = getStudyLog()
  const week = []
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today - i * 86400000)
    const isToday = i === 0
    const key = formatDateKey(d)
    const hasActivity = !!log[key]
    week.push({
      label: days[d.getDay()],
      active: hasActivity,
      isToday
    })
  }
  weekDays.value = week

  // 连续天数：今天算 1，从昨天往前数连续活跃天数
  let streak = 0
  const todayActive = week[week.length - 1].active
  for (let i = week.length - 2; i >= 0; i--) {
    if (week[i].active) streak++
    else break
  }
  if (todayActive) {
    streak++
  }
  streakDays.value = streak
}
</script>

<style lang="scss" scoped>
.page-learn {
  min-height: 100vh;
  background-color: $paper;
  padding: 0 $space-lg $space-3xl;
}

/* ===== Hero ===== */
.hero {
  padding: $space-2xl 0 $space-lg;

  &__meta {
    display: flex;
    align-items: center;
    gap: $space-sm;
    margin-bottom: $space-md;
  }

  &__meta-line {
    width: 32rpx;
    height: 1rpx;
    background-color: $ink-light;
  }

  &__meta-text {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 3rpx;
    font-weight: $weight-medium;
  }

  &__title {
    font-size: 72rpx;
    font-weight: $weight-bold;
    color: $ink;
    letter-spacing: 8rpx;
    display: block;
  }
}

/* ===== 统计三联 ===== */
.stats {
  display: flex;
  align-items: center;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  padding: $space-lg 0;
  margin-bottom: $space-lg;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $space-xs;
  }

  &__value {
    font-family: $font-serif;
    font-size: 64rpx;
    font-weight: $weight-bold;
    color: $ink;
    line-height: 1;
    letter-spacing: 2rpx;
  }

  &__label {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 2rpx;
  }

  &__divider {
    width: 1rpx;
    height: 64rpx;
    background-color: $line;
  }
}

/* ===== 收藏入口 ===== */
.entry {
  display: flex;
  align-items: center;
  background-color: $ink;
  padding: $space-lg;
  border-radius: $radius-md;
  gap: $space-md;
  margin-bottom: $space-2xl;

  &:active {
    opacity: 0.9;
  }

  &__seal {
    width: 80rpx;
    height: 80rpx;
    background-color: $cinnabar;
    border-radius: $radius-sm;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  &__seal-char {
    font-family: $font-serif;
    font-size: 44rpx;
    color: #FFFFFF;
    font-weight: $weight-bold;
    line-height: 1;
  }

  &__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: $space-xxs;
  }

  &__title {
    font-size: $font-md;
    font-weight: $weight-semibold;
    color: #FFFFFF;
    letter-spacing: 2rpx;
  }

  &__desc {
    font-size: $font-xs;
    color: rgba(255, 255, 255, 0.5);
    letter-spacing: 1rpx;
  }

  &__arrow {
    font-size: $font-lg;
    color: rgba(255, 255, 255, 0.6);
  }
}

/* ===== Section ===== */
.section {
  margin-top: $space-xl;

  &__head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $space-md;
  }

  &__title-wrap {
    display: flex;
    align-items: center;
    gap: $space-sm;
  }

  &__bar {
    width: 4rpx;
    height: 28rpx;
    background-color: $cinnabar;

    &--gold {
      background-color: $gold;
    }
  }

  &__title {
    font-size: $font-lg;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__clear {
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 1rpx;
  }

  &__hint {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 2rpx;
  }
}

/* ===== 学习进度可视化 ===== */
.progress-section {
  margin-top: $space-xl;
  padding: $space-lg;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;

  &__head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $space-lg;
  }

  &__title {
    font-size: $font-md;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__streak {
    font-size: $font-xs;
    color: $cinnabar;
    letter-spacing: 1rpx;
    font-weight: $weight-medium;
  }
}

.progress-dots {
  display: flex;
  justify-content: space-between;
  gap: $space-xs;
}

.progress-dot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-xs;
  flex: 1;

  &__label {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 1rpx;
  }

  &__circle {
    width: 56rpx;
    height: 56rpx;
    border-radius: 50%;
    border: 2rpx solid $line;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: $paper;
    transition: all 0.3s;

    .progress-dot--active & {
      background-color: $cinnabar;
      border-color: $cinnabar;
    }

    .progress-dot--today & {
      border-color: $cinnabar;
      box-shadow: 0 0 0 4rpx rgba(168, 54, 47, 0.15);
    }
  }

  &__check {
    font-size: 28rpx;
    color: #FFFFFF;
    font-weight: $weight-bold;
  }
}

/* ===== 最近浏览（纯文本列表） ===== */
.history-list {
  display: flex;
  flex-direction: column;
}

.history-item {
  display: flex;
  align-items: center;
  padding: $space-md $space-lg;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  gap: $space-md;
  position: relative;

  &:active {
    background-color: $paper-warm;
  }

  &__idx {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $gold;
    letter-spacing: 2rpx;
    font-weight: $weight-medium;
    flex-shrink: 0;
    width: 48rpx;
    text-align: center;
  }

  &__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: $space-xxs;
    min-width: 0;
  }

  &__name {
    font-size: $font-md;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 1rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__meta {
    font-size: $font-xs;
    color: $ink-light;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__line {
    position: absolute;
    bottom: 0;
    left: $space-lg;
    right: $space-lg;
    height: 1rpx;
    background-color: $line;
  }
}

/* ===== 推荐学习（横向滚动卡片） ===== */
.recommend-scroll {
  white-space: nowrap;
  margin: 0 calc(-1 * #{$space-lg});
  padding: 0 $space-lg;
}

.recommend-card {
  display: inline-flex;
  flex-direction: column;
  width: 260rpx;
  margin-right: $space-md;
  flex-shrink: 0;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  overflow: hidden;
  transition: all 0.2s;

  &:active {
    background-color: $paper-warm;
    transform: scale(0.98);
  }

  &__img-wrap {
    position: relative;
    width: 100%;
    height: 260rpx;
    overflow: hidden;
    background-color: $paper-deep;
  }

  &__img {
    width: 100%;
    height: 100%;
  }

  &__seal {
    position: absolute;
    top: $space-sm;
    left: $space-sm;
    padding: 2rpx 8rpx;
    background-color: rgba(250, 248, 243, 0.9);
    border: 1rpx solid $line;
    border-radius: $radius-xs;
  }

  &__seal-text {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $cinnabar;
    letter-spacing: 1rpx;
    font-weight: $weight-medium;
  }

  &__body {
    padding: $space-md;
    display: flex;
    flex-direction: column;
    gap: $space-xs;
  }

  &__name {
    font-size: $font-md;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 1rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__efficacy {
    font-size: $font-xs;
    color: $ink-light;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.empty-tip {
  padding: $space-2xl 0;
  text-align: center;

  &__text {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $ink-faint;
    letter-spacing: 4rpx;
  }
}
</style>
