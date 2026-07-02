<template>
  <view class="page-learn">
    <!-- 收藏夹入口 -->
    <view class="fav-entry" @click="goFavorites">
      <view class="fav-entry__icon">&#x2B50;</view>
      <view class="fav-entry__info">
        <text class="fav-entry__title">我的收藏</text>
        <text class="fav-entry__count">{{ favoriteCount }} 个药材</text>
      </view>
      <text class="fav-entry__arrow">&#x276F;</text>
    </view>

    <!-- 学习统计卡片 -->
    <view class="stats-card">
      <view class="stats-item">
        <text class="stats-item__value">{{ identifyCount }}</text>
        <text class="stats-item__label">识别次数</text>
      </view>
      <view class="stats-item">
        <text class="stats-item__value">{{ favoriteCount }}</text>
        <text class="stats-item__label">收藏数</text>
      </view>
      <view class="stats-item">
        <text class="stats-item__value">{{ viewCount }}</text>
        <text class="stats-item__label">浏览数</text>
      </view>
    </view>

    <!-- 最近浏览 -->
    <view class="section">
      <view class="section__header">
        <text class="section__title">最近浏览</text>
        <text class="section__clear" @click="onClearRecent" v-if="recentViewed.length">清除</text>
      </view>
      <scroll-view class="recent-scroll" scroll-x enable-flex v-if="recentViewed.length">
        <view
          class="recent-item"
          v-for="(item, index) in recentViewed"
          :key="index"
          @click="goDetail(item)"
        >
          <image :src="item.image || '/static/images/placeholder.png'" mode="aspectFill" class="recent-item__img" />
          <text class="recent-item__name">{{ item.name }}</text>
        </view>
      </scroll-view>
      <view class="empty-tip" v-else>
        <text class="empty-tip__text">暂无浏览记录</text>
      </view>
    </view>

    <!-- 学习推荐 -->
    <view class="section">
      <view class="section__header">
        <text class="section__title">推荐学习</text>
      </view>
      <view class="recommend-list">
        <HerbCard
          v-for="(item, index) in recommendList"
          :key="index"
          :herb="item"
        />
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 学习首页
 * 收藏夹入口、最近浏览、学习统计、推荐
 */
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useHerbStore } from '@/store/herb'
import { getFavorites, getRecords } from '@/api/user'
import { getHerbs } from '@/api/knowledge'
import HerbCard from '@/components/HerbCard.vue'

const herbStore = useHerbStore()

const favoriteCount = ref(0)
const identifyCount = ref(0)
const viewCount = ref(0)
const recentViewed = ref([])
const recommendList = ref([])

onShow(() => {
  recentViewed.value = herbStore.recentViewed
  viewCount.value = herbStore.recentViewed.length
  loadStats()
  loadRecommend()
})

/**
 * 加载统计数据
 */
async function loadStats() {
  try {
    const [favData, recData] = await Promise.all([
      getFavorites({ page: 1, pageSize: 1 }),
      getRecords({ page: 1, pageSize: 1 })
    ])
    favoriteCount.value = favData.total || 0
    identifyCount.value = recData.total || 0
  } catch (err) {
    // 静默处理
  }
}

/**
 * 加载推荐药材
 */
async function loadRecommend() {
  try {
    const data = await getHerbs({ page: 1, pageSize: 4 })
    recommendList.value = data.list || data || []
  } catch (err) {
    // 静默处理
  }
}

/**
 * 跳转收藏夹
 */
function goFavorites() {
  uni.navigateTo({
    url: '/pages/learn/favorites'
  })
}

/**
 * 清除最近浏览
 */
function onClearRecent() {
  herbStore.clearRecentViewed()
  recentViewed.value = []
  viewCount.value = 0
}

/**
 * 跳转详情
 */
function goDetail(item) {
  uni.navigateTo({
    url: `/pages/knowledge/detail?id=${item.id}`
  })
}
</script>

<style lang="scss" scoped>
.page-learn {
  min-height: 100vh;
  background-color: $bg-color;
  padding: $spacing-lg;
}

/* 收藏夹入口 */
.fav-entry {
  display: flex;
  align-items: center;
  padding: $spacing-lg;
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  border-radius: $radius-lg;
  margin-bottom: $spacing-lg;
  gap: $spacing-md;

  &__icon {
    font-size: 48rpx;
  }

  &__info {
    flex: 1;
  }

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: #FFFFFF;
    display: block;
  }

  &__count {
    font-size: $font-sm;
    color: $accent-color;
    display: block;
    margin-top: $spacing-xs;
  }

  &__arrow {
    font-size: $font-lg;
    color: $accent-color;
  }
}

/* 统计卡片 */
.stats-card {
  display: flex;
  background-color: $card-bg;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-lg;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
}

.stats-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-xs;

  &__value {
    font-size: 48rpx;
    font-weight: 700;
    color: $primary-color;
  }

  &__label {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

/* 通用板块 */
.section {
  margin-bottom: $spacing-lg;

  &__header {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-md;
  }

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
  }

  &__clear {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

.recent-scroll {
  white-space: nowrap;
}

.recent-item {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: 160rpx;
  margin-right: $spacing-md;
  flex-shrink: 0;

  &__img {
    width: 160rpx;
    height: 160rpx;
    border-radius: $radius-md;
    background-color: $border-color;
  }

  &__name {
    font-size: $font-sm;
    color: $text-color;
    margin-top: $spacing-xs;
  }
}

.empty-tip {
  padding: $spacing-xl 0;
  text-align: center;

  &__text {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

.recommend-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-md;

  > * {
    width: calc(50% - 12rpx);
  }
}
</style>
