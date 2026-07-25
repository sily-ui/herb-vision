<template>
  <view class="page-result">
    <!-- 顶部返回 + 操作 -->
    <view class="result-header">
      <view class="result-header__top">
        <view class="back" @click="goBack">
          <text class="back__icon">&#x2190;</text>
          <text class="back__text">返回</text>
        </view>
        <view class="actions">
          <text class="actions__btn" @click="onFavorite">{{ isFavorited ? '&#x2B50;' : '&#x2606;' }}</text>
          <text class="actions__btn actions__btn--primary" @click="onReidentify">重新识别</text>
        </view>
      </view>

      <view class="result-header__main">
        <text class="result-header__name">{{ result.name || '未知药材' }}</text>
        <view class="result-header__meta">
          <text class="result-header__confidence">置信度 {{ displayConfidence }}%</text>
          <text class="result-header__tag" v-if="result.family">{{ result.family }}</text>
        </view>
      </view>
    </view>

    <!-- 药材图片 -->
    <view class="image-card" v-if="displayImage">
      <image class="image-card__img" :src="displayImage" mode="aspectFill" />
    </view>

    <!-- 基本信息 -->
    <view class="info-card">
      <text class="info-card__title">基本信息</text>
      <view class="info-row">
        <text class="info-row__label">别名</text>
        <text class="info-row__value">{{ result.alias || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="info-row__label">科属</text>
        <text class="info-row__value">{{ result.family || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="info-row__label">来源</text>
        <text class="info-row__value">{{ result.source || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="info-row__label">药用部位</text>
        <text class="info-row__value">{{ result.part_used || '-' }}</text>
      </view>
    </view>

    <!-- 性状鉴别 -->
    <view class="info-card">
      <text class="info-card__title">性状鉴别</text>
      <view class="trait-row">
        <text class="trait-row__label">颜色</text>
        <text class="trait-row__value">{{ result.appearance?.color || '-' }}</text>
      </view>
      <view class="trait-row">
        <text class="trait-row__label">质地</text>
        <text class="trait-row__value">{{ result.appearance?.texture || '-' }}</text>
      </view>
      <view class="trait-row">
        <text class="trait-row__label">断面</text>
        <text class="trait-row__value">{{ result.appearance?.fracture || '-' }}</text>
      </view>
      <view class="trait-row">
        <text class="trait-row__label">气味</text>
        <text class="trait-row__value">{{ result.appearance?.odor || '-' }}</text>
      </view>
    </view>

    <!-- 性味归经 -->
    <view class="info-card info-card--inline" v-if="result.property">
      <text class="info-card__title">性味归经</text>
      <text class="info-card__text">{{ result.property }}</text>
    </view>

    <!-- 功效主治 -->
    <view class="info-card">
      <text class="info-card__title">功效主治</text>
      <text class="info-card__text">{{ result.efficacy || '-' }}</text>
    </view>

    <!-- 用法用量 -->
    <view class="info-card">
      <text class="info-card__title">用法用量</text>
      <text class="info-card__text">{{ result.usage || '-' }}</text>
    </view>

    <!-- 真伪鉴别 -->
    <view class="info-card">
      <text class="info-card__title">真伪鉴别</text>
      <text class="info-card__text">{{ result.authentication || '暂无鉴别要点' }}</text>
      <view class="confused-herbs" v-if="result.confusedHerbs && result.confusedHerbs.length">
        <text class="confused-herbs__label">易混淆药材</text>
        <view class="confused-herbs__list">
          <text
            class="confused-herbs__item"
            v-for="(item, index) in result.confusedHerbs"
            :key="index"
            @click="goCompare(item)"
          >{{ item.name }}</text>
        </view>
      </view>
    </view>

    <!-- 禁忌 -->
    <view class="info-card info-card--warning" v-if="result.contraindication">
      <text class="info-card__title">禁忌</text>
      <text class="info-card__text info-card__text--danger">{{ result.contraindication }}</text>
    </view>

    <!-- 查看详情入口 -->
    <view class="detail-entry" v-if="result.herb_id" @click="goDetail">
      <text class="detail-entry__text">查看药材详情</text>
      <text class="detail-entry__arrow">&#x2192;</text>
    </view>

    <!-- 底部留白 -->
    <view class="epilogue">
      <view class="epilogue__line"></view>
      <text class="epilogue__text">— 辨药识真，用药明道 —</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 识别结果页 · 墨韵版
 * 与首页统一风格，去掉底部固定导航栏，信息集中一页展示
 */
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { addFavorite, removeFavorite } from '@/api/user'

const BASE_URL = import.meta.env.VITE_BASE_URL || 'http://localhost:8000'

const result = ref({})
const rawResult = ref({})
const isFavorited = ref(false)

const displayConfidence = computed(() => {
  const c = result.value.confidence
  if (typeof c === 'number') return c
  if (c === '高') return 95
  if (c === '中') return 70
  if (c === '低') return 45
  return 0
})

const displayImage = computed(() => {
  const img = result.value.image
  if (!img) return ''
  if (img.startsWith('http')) return img
  // 相对路径补全为后端完整 URL
  const path = img.startsWith('/') ? img : `/${img}`
  return `${BASE_URL}${path}`
})

onLoad((query) => {
  if (query.data) {
    try {
      rawResult.value = JSON.parse(decodeURIComponent(query.data))
      normalizeResult(rawResult.value)
    } catch (err) {
      console.error('解析识别结果失败:', err)
    }
  }
})

/**
 * 将后端返回结果统一转换为页面可用结构
 */
function normalizeResult(data) {
  const r = data.result || data
  result.value = {
    herb_id: r.herb_id,
    name: r.name || '未知药材',
    alias: r.alias || r.aliases || '',
    family: r.family || '',
    source: r.source || '',
    part_used: r.part_used || '',
    property: r.property || (r.nature_taste && r.meridian_tropism ? `${r.nature_taste}；归${r.meridian_tropism}` : ''),
    efficacy: r.efficacy || r.indications || '',
    usage: r.usage || r.usage_dosage || '',
    authentication: r.authentication || r.authenticity_tips || '',
    contraindication: r.contraindication || r.contraindications || '',
    confidence: r.confidence || '低',
    image: r.image || '',
    appearance: {
      color: r.appearance?.color || r.appearance_color || '',
      texture: r.appearance?.texture || r.appearance_texture || '',
      fracture: r.appearance?.fracture || r.appearance_fracture || '',
      odor: r.appearance?.odor || r.appearance_odor || ''
    },
    confusedHerbs: normalizeConfused(r.confusedHerbs || r.confusable_herbs || [])
  }
}

function normalizeConfused(list) {
  if (!list) return []
  if (Array.isArray(list)) {
    return list.map(item => typeof item === 'string' ? { name: item, id: '' } : item)
  }
  if (typeof list === 'string') {
    return list.split(/[,，]/).filter(Boolean).map(name => ({ name: name.trim(), id: '' }))
  }
  return []
}

async function onFavorite() {
  try {
    if (isFavorited.value) {
      await removeFavorite(result.value.record_id)
      isFavorited.value = false
      uni.showToast({ title: '已取消收藏', icon: 'none' })
    } else {
      await addFavorite(result.value.record_id)
      isFavorited.value = true
      uni.showToast({ title: '收藏成功', icon: 'none' })
    }
  } catch (err) {
    // 静默处理
  }
}

function onReidentify() {
  uni.navigateBack()
}

function goBack() {
  uni.navigateBack()
}

function goDetail() {
  if (result.value.herb_id) {
    uni.navigateTo({
      url: `/pages/knowledge/detail?id=${result.value.herb_id}`
    })
  }
}

function goCompare(item) {
  if (result.value.herb_id && item.id) {
    uni.navigateTo({
      url: `/pages/compare/index?id1=${result.value.herb_id}&id2=${item.id}`
    })
  }
}
</script>

<style lang="scss" scoped>
.page-result {
  min-height: 100vh;
  background-color: #FAF8F3;
  padding: 0 30rpx 60rpx;
}

.result-header {
  padding: 40rpx 0 30rpx;

  &__top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30rpx;
  }

  &__main {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
  }

  &__name {
    font-size: 56rpx;
    font-weight: 700;
    color: #1A1A1A;
    letter-spacing: 4rpx;
    line-height: 1.2;
  }

  &__meta {
    display: flex;
    align-items: center;
    gap: 16rpx;
  }

  &__confidence {
    font-family: "Songti SC", serif;
    font-size: 28rpx;
    color: #A8362F;
    font-weight: 600;
  }

  &__tag {
    font-size: 22rpx;
    color: #8C8C8C;
    padding: 4rpx 14rpx;
    border: 1rpx solid #E5DFD2;
    border-radius: 4rpx;
  }
}

.back {
  display: flex;
  align-items: center;
  gap: 8rpx;

  &__icon {
    font-size: 30rpx;
    color: #4A4A4A;
  }

  &__text {
    font-size: 26rpx;
    color: #4A4A4A;
    letter-spacing: 2rpx;
  }
}

.actions {
  display: flex;
  align-items: center;
  gap: 16rpx;

  &__btn {
    font-size: 30rpx;
    color: #4A4A4A;
    padding: 8rpx 16rpx;

    &--primary {
      font-size: 24rpx;
      color: #FFFFFF;
      background-color: #A8362F;
      border-radius: 4rpx;
      letter-spacing: 2rpx;
    }
  }
}

.image-card {
  background-color: #FFFFFF;
  border: 1rpx solid #E5DFD2;
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 30rpx;

  &__img {
    width: 100%;
    height: 360rpx;
    display: block;
  }
}

.info-card {
  background-color: #FFFFFF;
  border: 1rpx solid #E5DFD2;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;

  &__title {
    display: flex;
    align-items: center;
    font-size: 30rpx;
    font-weight: 600;
    color: #1A1A1A;
    letter-spacing: 2rpx;
    margin-bottom: 24rpx;

    &::before {
      content: "";
      display: inline-block;
      width: 4rpx;
      height: 28rpx;
      background-color: #A8362F;
      margin-right: 16rpx;
    }
  }

  &__text {
    font-size: 26rpx;
    color: #4A4A4A;
    line-height: 1.8;
    display: block;

    &--danger {
      color: #A8362F;
    }
  }

  &--warning {
    border-color: rgba(168, 54, 47, 0.25);
    background-color: #FDF8F7;
  }
}

.info-row {
  display: flex;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #F2EFE8;

  &:last-child {
    border-bottom: none;
  }

  &__label {
    width: 140rpx;
    font-size: 26rpx;
    color: #8C8C8C;
    flex-shrink: 0;
  }

  &__value {
    flex: 1;
    font-size: 26rpx;
    color: #1A1A1A;
  }
}

.trait-row {
  display: flex;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #F2EFE8;

  &:last-child {
    border-bottom: none;
  }

  &__label {
    width: 140rpx;
    font-size: 26rpx;
    color: #8C8C8C;
    flex-shrink: 0;
  }

  &__value {
    flex: 1;
    font-size: 26rpx;
    color: #1A1A1A;
  }
}

.confused-herbs {
  margin-top: 24rpx;
  padding-top: 24rpx;
  border-top: 1rpx solid #F2EFE8;

  &__label {
    font-size: 24rpx;
    color: #8C8C8C;
    display: block;
    margin-bottom: 12rpx;
  }

  &__list {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
  }

  &__item {
    font-size: 24rpx;
    color: #A8362F;
    background-color: #FAF8F3;
    padding: 8rpx 20rpx;
    border: 1rpx solid #E5DFD2;
    border-radius: 4rpx;
  }
}

.detail-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #FFFFFF;
  border: 1rpx solid #E5DFD2;
  border-radius: 12rpx;
  padding: 28rpx 30rpx;
  margin-bottom: 40rpx;

  &__text {
    font-size: 28rpx;
    color: #1A1A1A;
    letter-spacing: 2rpx;
    font-weight: 500;
  }

  &__arrow {
    font-size: 30rpx;
    color: #A8362F;
  }
}

.epilogue {
  margin-top: 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16rpx;

  &__line {
    width: 64rpx;
    height: 1rpx;
    background-color: #D9D3C5;
  }

  &__text {
    font-family: "Songti SC", serif;
    font-size: 24rpx;
    color: #8C8C8C;
    letter-spacing: 4rpx;
  }
}
</style>
