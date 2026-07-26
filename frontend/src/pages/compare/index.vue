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
      <!-- 外观对比 -->
      <view class="compare-card">
        <text class="compare-card__title">外观对比</text>
        <view class="compare-images">
          <view class="compare-images__item">
            <image :src="resolveImageUrl(herb1.image_main)" mode="aspectFill" class="compare-images__img" @error="onImageError(1)" />
            <text class="compare-images__name">{{ herb1.name }}</text>
          </view>
          <view class="compare-images__item">
            <image :src="resolveImageUrl(herb2.image_main)" mode="aspectFill" class="compare-images__img" @error="onImageError(2)" />
            <text class="compare-images__name">{{ herb2.name }}</text>
          </view>
        </view>
      </view>

      <!-- AI 智能对比 -->
      <view class="compare-card" v-if="aiCompareResult">
        <text class="compare-card__title">AI 智能对比</text>

        <view class="ai-loading" v-if="aiLoading">
          <text>正在调用大模型生成专业对比，请稍候...</text>
        </view>

        <view v-else>
          <text class="ai-summary">{{ aiCompareResult.summary }}</text>

          <view class="ai-comparison" v-for="(item, index) in aiCompareResult.comparisons" :key="index">
            <text class="comparison-field">{{ item.field }}</text>
            <view class="comparison-content">
              <text class="comparison-herb1">{{ herb1.name }}：{{ item.herb1 }}</text>
              <text class="comparison-herb2">{{ herb2.name }}：{{ item.herb2 }}</text>
              <text class="comparison-diff">区别要点：{{ item.difference }}</text>
            </view>
          </view>
        </view>
      </view>

      <view class="compare-card" v-else-if="!aiLoading">
        <text class="compare-card__title">AI 智能对比</text>
        <view v-if="aiError" class="ai-error">
          <text class="ai-error__text">{{ aiError }}</text>
          <view class="ai-error__retry" @click="loadAiCompare">
            <text class="ai-error__retry-text">点击重试</text>
          </view>
        </view>
        <text v-else class="compare-placeholder">暂无智能对比结果</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 混淆药材对比页
 * 两个药材选择、快捷对比、AI 智能对比
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { compareHerbs, getHerbDetail, aiCompareHerbs } from '@/api/knowledge'
import { resolveImageUrl } from '@/utils/common'

const herb1 = ref({})
const herb2 = ref({})
const aiCompareResult = ref(null)
const aiLoading = ref(false)
const aiError = ref('')

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
    loadCompare(query.id1, query.id2).then(() => loadAiCompare())
  }
})

/**
 * 加载基础对比数据
 */
async function loadCompare(id1, id2) {
  try {
    const data = await compareHerbs(id1, id2)
    herb1.value = data.herb_1 || data.herb1 || {}
    herb2.value = data.herb_2 || data.herb2 || {}
  } catch (err) {
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
 * 调用大模型生成智能对比
 */
async function loadAiCompare() {
  if (!herb1.value.id || !herb2.value.id) {
    return
  }
  aiLoading.value = true
  aiCompareResult.value = null
  aiError.value = ''

  try {
    const data = await aiCompareHerbs(herb1.value.id, herb2.value.id)
    aiCompareResult.value = data.ai_compare || null
    if (!aiCompareResult.value) {
      aiError.value = '未获取到对比结果'
    }
  } catch (err) {
    aiError.value = err.message || '智能对比失败'
    uni.showToast({ title: '智能对比失败', icon: 'none' })
  } finally {
    aiLoading.value = false
  }
}

/**
 * 选择药材
 */
function onSelectHerb(side) {
  uni.navigateTo({
    url: `/pages/knowledge/search?select=compare${side}`
  })
}

/**
 * 选择页返回后回填药材
 */
function onHerbSelected(side, herb) {
  if (side === 1) {
    herb1.value = herb || {}
  } else if (side === 2) {
    herb2.value = herb || {}
  }
  if (herb1.value.id && herb2.value.id) {
    loadAiCompare()
  }
}

/**
 * 快捷对比：点击常见混淆对后，先加载基础数据立即展示，再异步调用大模型对比
 */
async function onQuickPair(item) {
  await loadCompare(item.id1, item.id2)
  loadAiCompare()
}

function onImageError(side) {
  // 图片加载失败时不做处理，依赖 CSS 背景色显示占位效果
}

defineExpose({ onHerbSelected })
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
    width: 260rpx;
    height: 260rpx;
    border-radius: $radius-md;
    background-color: $border-color;
  }

  &__name {
    font-size: $font-md;
    font-weight: 500;
    color: $text-color;
  }
}

/* AI 对比 */
.ai-loading {
  font-size: $font-md;
  color: $text-secondary;
  padding: $spacing-lg 0;
}

.ai-summary {
  font-size: $font-md;
  font-weight: 500;
  color: $text-color;
  line-height: 1.7;
  display: block;
  margin-bottom: $spacing-lg;
}

.ai-comparison {
  margin-bottom: $spacing-lg;

  &:last-child {
    margin-bottom: 0;
  }
}

.comparison-field {
  font-size: $font-md;
  font-weight: 600;
  color: $primary-color;
  display: block;
  margin-bottom: $space-xs;
}

.comparison-content {
  display: flex;
  flex-direction: column;
  gap: $space-xs;
}

.comparison-herb1,
.comparison-herb2 {
  font-size: $font-sm;
  color: $text-color;
  line-height: 1.7;
}

.comparison-diff {
  font-size: $font-sm;
  color: $ink-soft;
  line-height: 1.7;
}

.compare-placeholder {
  font-size: $font-md;
  color: $text-secondary;
}

.ai-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-lg 0;

  &__text {
    font-size: $font-sm;
    color: $text-secondary;
    text-align: center;
    line-height: 1.6;
  }

  &__retry {
    padding: $spacing-sm $spacing-lg;
    background-color: $primary-color;
    border-radius: $radius-lg;

    &-text {
      font-size: $font-md;
      color: #FFFFFF;
      font-weight: 500;
    }
  }
}
</style>
