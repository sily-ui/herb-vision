<template>
  <view class="page-compare">
    <!-- 顶部药材选择器 -->
    <view class="selector-row">
      <view class="selector-item" @click="onSelectHerb(1)">
        <text class="selector-item__label">药材一</text>
        <text class="selector-item__name">{{ herb1.name || '点击选择' }}</text>
      </view>
      <text class="selector-vs">VS</text>
      <view class="selector-item" @click="onSelectHerb(2)">
        <text class="selector-item__label">药材二</text>
        <text class="selector-item__name">{{ herb2.name || '点击选择' }}</text>
      </view>
    </view>

    <!-- 常见混淆对快捷入口 -->
    <view class="quick-pairs" v-if="!herb1.id && !herb2.id">
      <text class="quick-pairs__title">常见混淆对</text>
      <view class="quick-pairs__list">
        <view
          class="quick-pair-item"
          v-for="(item, index) in commonPairs"
          :key="index"
          @click="onQuickPair(item)"
        >
          <text>{{ item.name1 }} vs {{ item.name2 }}</text>
        </view>
      </view>
    </view>

    <!-- 对比区域 -->
    <view class="compare-area" v-if="herb1.id && herb2.id">
      <!-- 图片对比 -->
      <view class="compare-card">
        <text class="compare-card__title">外观对比</text>
        <view class="compare-images">
          <view class="compare-images__item">
            <image :src="herb1.image || '/static/images/placeholder.png'" mode="aspectFill" class="compare-images__img" />
            <text class="compare-images__name">{{ herb1.name }}</text>
          </view>
          <view class="compare-images__item">
            <image :src="herb2.image || '/static/images/placeholder.png'" mode="aspectFill" class="compare-images__img" />
            <text class="compare-images__name">{{ herb2.name }}</text>
          </view>
        </view>
      </view>

      <!-- 性状对比 -->
      <view class="compare-card">
        <text class="compare-card__title">性状对比</text>
        <view class="compare-table">
          <view class="compare-table__header">
            <text class="compare-table__th">特征</text>
            <text class="compare-table__th">{{ herb1.name }}</text>
            <text class="compare-table__th">{{ herb2.name }}</text>
          </view>
          <view class="compare-table__row">
            <text class="compare-table__td">颜色</text>
            <text class="compare-table__td">{{ herb1.appearance?.color || '-' }}</text>
            <text class="compare-table__td">{{ herb2.appearance?.color || '-' }}</text>
          </view>
          <view class="compare-table__row">
            <text class="compare-table__td">质地</text>
            <text class="compare-table__td">{{ herb1.appearance?.texture || '-' }}</text>
            <text class="compare-table__td">{{ herb2.appearance?.texture || '-' }}</text>
          </view>
          <view class="compare-table__row">
            <text class="compare-table__td">断面</text>
            <text class="compare-table__td">{{ herb1.appearance?.fracture || '-' }}</text>
            <text class="compare-table__td">{{ herb2.appearance?.fracture || '-' }}</text>
          </view>
          <view class="compare-table__row">
            <text class="compare-table__td">气味</text>
            <text class="compare-table__td">{{ herb1.appearance?.odor || '-' }}</text>
            <text class="compare-table__td">{{ herb2.appearance?.odor || '-' }}</text>
          </view>
        </view>
      </view>

      <!-- 鉴别要点对比 -->
      <view class="compare-card">
        <text class="compare-card__title">鉴别要点</text>
        <view class="compare-text">
          <view class="compare-text__item">
            <text class="compare-text__name">{{ herb1.name }}</text>
            <text class="compare-text__content">{{ herb1.authentication || '暂无' }}</text>
          </view>
          <view class="compare-text__item">
            <text class="compare-text__name">{{ herb2.name }}</text>
            <text class="compare-text__content">{{ herb2.authentication || '暂无' }}</text>
          </view>
        </view>
      </view>

      <!-- 功效对比 -->
      <view class="compare-card">
        <text class="compare-card__title">功效对比</text>
        <view class="compare-text">
          <view class="compare-text__item">
            <text class="compare-text__name">{{ herb1.name }}</text>
            <text class="compare-text__content">{{ herb1.efficacy || '暂无' }}</text>
          </view>
          <view class="compare-text__item">
            <text class="compare-text__name">{{ herb2.name }}</text>
            <text class="compare-text__content">{{ herb2.efficacy || '暂无' }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 混淆药材对比页
 * 两个药材选择、快捷对比、详细对比
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { compareHerbs, getHerbDetail } from '@/api/knowledge'

const herb1 = ref({})
const herb2 = ref({})

// 常见混淆对
const commonPairs = ref([
  { name1: '赤芍', name2: '白芍', id1: 1, id2: 2 },
  { name1: '黄芪', name2: '红芪', id1: 3, id2: 4 },
  { name1: '半夏', name2: '水半夏', id1: 5, id2: 6 },
  { name1: '柴胡', name2: '银柴胡', id1: 7, id2: 8 },
  { name1: '人参', name2: '党参', id1: 9, id2: 10 }
])

onLoad((query) => {
  if (query.id1 && query.id2) {
    loadCompare(query.id1, query.id2)
  }
})

/**
 * 加载对比数据
 */
async function loadCompare(id1, id2) {
  try {
    const data = await compareHerbs(id1, id2)
    herb1.value = data.herb1 || {}
    herb2.value = data.herb2 || {}
  } catch (err) {
    // 如果对比接口失败，分别获取详情
    try {
      const [d1, d2] = await Promise.all([getHerbDetail(id1), getHerbDetail(id2)])
      herb1.value = d1 || {}
      herb2.value = d2 || {}
    } catch (e) {
      uni.showToast({ title: '加载失败', icon: 'none' })
    }
  }
}

/**
 * 选择药材
 */
function onSelectHerb(side) {
  // 跳转到搜索页选择药材
  uni.navigateTo({
    url: `/pages/knowledge/search?select=compare${side}`
  })
}

/**
 * 快捷对比
 */
function onQuickPair(item) {
  loadCompare(item.id1, item.id2)
}
</script>

<style lang="scss" scoped>
.page-compare {
  min-height: 100vh;
  background-color: $bg-color;
  padding: $spacing-lg;
}

/* 选择器 */
.selector-row {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
}

.selector-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-lg;
  background-color: $card-bg;
  border-radius: $radius-lg;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
  gap: $spacing-xs;

  &__label {
    font-size: $font-xs;
    color: $text-secondary;
  }

  &__name {
    font-size: $font-lg;
    font-weight: 600;
    color: $primary-color;
  }
}

.selector-vs {
  font-size: $font-lg;
  font-weight: 700;
  color: $danger-color;
  flex-shrink: 0;
}

/* 快捷对比 */
.quick-pairs {
  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
    display: block;
    margin-bottom: $spacing-md;
  }

  &__list {
    display: flex;
    flex-direction: column;
    gap: $spacing-sm;
  }
}

.quick-pair-item {
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
  border-radius: $radius-md;
  font-size: $font-md;
  color: $text-color;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

/* 对比卡片 */
.compare-card {
  background-color: $card-bg;
  border-radius: $radius-md;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
    display: block;
    margin-bottom: $spacing-md;
    padding-bottom: $spacing-sm;
    border-bottom: 1rpx solid $border-color;
  }
}

/* 图片对比 */
.compare-images {
  display: flex;
  gap: $spacing-lg;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $spacing-xs;
  }

  &__img {
    width: 240rpx;
    height: 240rpx;
    border-radius: $radius-md;
    background-color: $border-color;
  }

  &__name {
    font-size: $font-md;
    font-weight: 500;
    color: $text-color;
  }
}

/* 对比表格 */
.compare-table {
  &__header {
    display: flex;
    background-color: $accent-color;
    border-radius: $radius-sm $radius-sm 0 0;
  }

  &__row {
    display: flex;
    border-bottom: 1rpx solid $border-color;
  }

  &__th, &__td {
    flex: 1;
    padding: $spacing-sm $spacing-md;
    font-size: $font-sm;
    text-align: center;
  }

  &__th {
    font-weight: 600;
    color: $primary-color;
  }

  &__td {
    color: $text-color;
  }
}

/* 文字对比 */
.compare-text {
  display: flex;
  gap: $spacing-lg;

  &__item {
    flex: 1;
  }

  &__name {
    font-size: $font-md;
    font-weight: 500;
    color: $primary-color;
    display: block;
    margin-bottom: $spacing-xs;
  }

  &__content {
    font-size: $font-sm;
    color: $text-color;
    line-height: 1.8;
    display: block;
  }
}
</style>
