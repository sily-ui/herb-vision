<template>
  <view class="page-result">
    <!-- 顶部：药材名称+置信度 -->
    <view class="result-header">
      <text class="result-header__name">{{ result.name || '未知药材' }}</text>
      <view class="result-header__confidence">
        <text class="result-header__confidence-label">置信度</text>
        <text class="result-header__confidence-value">{{ result.confidence || 0 }}%</text>
      </view>
    </view>

    <!-- 基本信息区 -->
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
    </view>

    <!-- 性状鉴别区 -->
    <view class="info-card">
      <text class="info-card__title">性状鉴别</text>
      <view class="trait-grid">
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F3A8;</text>
          <text class="trait-item__label">颜色</text>
          <text class="trait-item__value">{{ result.appearance?.color || '-' }}</text>
        </view>
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F44B;</text>
          <text class="trait-item__label">质地</text>
          <text class="trait-item__value">{{ result.appearance?.texture || '-' }}</text>
        </view>
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F52D;</text>
          <text class="trait-item__label">断面</text>
          <text class="trait-item__value">{{ result.appearance?.fracture || '-' }}</text>
        </view>
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F443;</text>
          <text class="trait-item__label">气味</text>
          <text class="trait-item__value">{{ result.appearance?.odor || '-' }}</text>
        </view>
      </view>
    </view>

    <!-- 真伪鉴别区 -->
    <view class="info-card">
      <text class="info-card__title">真伪鉴别</text>
      <text class="info-card__text">{{ result.authentication || '暂无鉴别要点' }}</text>
      <!-- 混淆药材 -->
      <view class="confused-herbs" v-if="result.confusedHerbs && result.confusedHerbs.length">
        <text class="confused-herbs__label">易混淆药材：</text>
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

    <!-- 性味归经 -->
    <view class="info-card">
      <text class="info-card__title">性味归经</text>
      <text class="info-card__text">{{ result.property || '-' }}</text>
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

    <!-- 禁忌 -->
    <view class="info-card">
      <text class="info-card__title">禁忌</text>
      <text class="info-card__text" :class="{ 'info-card__text--danger': result.contraindication }">{{ result.contraindication || '暂无禁忌信息' }}</text>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-actions">
      <view class="bottom-actions__item" @click="onFavorite">
        <text class="bottom-actions__icon">{{ isFavorited ? '&#x2B50;' : '&#x2606;' }}</text>
        <text class="bottom-actions__text">收藏</text>
      </view>
      <view class="bottom-actions__item" @click="onShare">
        <text class="bottom-actions__icon">&#x1F4E4;</text>
        <text class="bottom-actions__text">分享</text>
      </view>
      <view class="bottom-actions__item" @click="onFeedback">
        <text class="bottom-actions__icon">&#x1F4A9;</text>
        <text class="bottom-actions__text">反馈</text>
      </view>
      <view class="bottom-actions__item" @click="onReidentify">
        <text class="bottom-actions__icon">&#x1F504;</text>
        <text class="bottom-actions__text">重新识别</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 识别结果页
 * 展示识别结果的详细信息
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { addFavorite, removeFavorite } from '@/api/user'

const result = ref({})
const isFavorited = ref(false)

onLoad((query) => {
  if (query.data) {
    try {
      result.value = JSON.parse(decodeURIComponent(query.data))
    } catch (err) {
      console.error('解析识别结果失败:', err)
    }
  }
})

/**
 * 收藏/取消收藏
 */
async function onFavorite() {
  try {
    if (isFavorited.value) {
      await removeFavorite(result.value.id)
      isFavorited.value = false
      uni.showToast({ title: '已取消收藏', icon: 'none' })
    } else {
      await addFavorite(result.value.id)
      isFavorited.value = true
      uni.showToast({ title: '收藏成功', icon: 'none' })
    }
  } catch (err) {
    // 静默处理
  }
}

/**
 * 分享
 */
function onShare() {
  // 小程序分享功能
}

/**
 * 反馈错误
 */
function onFeedback() {
  uni.navigateTo({
    url: `/pages/feedback/index?herbId=${result.value.id || ''}`
  })
}

/**
 * 重新识别
 */
function onReidentify() {
  uni.navigateBack()
}

/**
 * 跳转对比页
 */
function goCompare(item) {
  uni.navigateTo({
    url: `/pages/compare/index?id1=${result.value.id}&id2=${item.id}`
  })
}
</script>

<style lang="scss" scoped>
.page-result {
  min-height: 100vh;
  background-color: $bg-color;
  padding: $spacing-lg;
  padding-bottom: 160rpx;
}

/* 顶部 */
.result-header {
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  border-radius: $radius-lg;
  padding: $spacing-xl $spacing-lg;
  margin-bottom: $spacing-lg;

  &__name {
    font-size: 48rpx;
    font-weight: 700;
    color: #FFFFFF;
    display: block;
  }

  &__confidence {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    margin-top: $spacing-sm;
  }

  &__confidence-label {
    font-size: $font-sm;
    color: $accent-color;
  }

  &__confidence-value {
    font-size: $font-lg;
    font-weight: 600;
    color: #FFFFFF;
  }
}

/* 信息卡片 */
.info-card {
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

  &__text {
    font-size: $font-md;
    color: $text-color;
    line-height: 1.8;
    display: block;

    &--danger {
      color: $danger-color;
    }
  }
}

/* 信息行 */
.info-row {
  display: flex;
  padding: $spacing-sm 0;
  border-bottom: 1rpx solid $border-color;

  &:last-child {
    border-bottom: none;
  }

  &__label {
    width: 120rpx;
    font-size: $font-md;
    color: $text-secondary;
    flex-shrink: 0;
  }

  &__value {
    flex: 1;
    font-size: $font-md;
    color: $text-color;
  }
}

/* 性状网格 */
.trait-grid {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-md;
}

.trait-item {
  width: calc(50% - 12rpx);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-md;
  background-color: $accent-color;
  border-radius: $radius-md;
  gap: $spacing-xs;

  &__icon {
    font-size: 40rpx;
  }

  &__label {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__value {
    font-size: $font-md;
    color: $text-color;
    font-weight: 500;
  }
}

/* 混淆药材 */
.confused-herbs {
  margin-top: $spacing-md;

  &__label {
    font-size: $font-sm;
    color: $text-secondary;
    display: block;
    margin-bottom: $spacing-xs;
  }

  &__list {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;
  }

  &__item {
    font-size: $font-sm;
    color: $primary-color;
    background-color: $accent-color;
    padding: 8rpx $spacing-md;
    border-radius: $radius-sm;
  }
}

/* 底部操作栏 */
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background-color: $card-bg;
  padding: $spacing-md 0;
  padding-bottom: calc(#{$spacing-md} + env(safe-area-inset-bottom));
  box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.06);
  z-index: 100;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $spacing-xs;
  }

  &__icon {
    font-size: 40rpx;
  }

  &__text {
    font-size: $font-xs;
    color: $text-secondary;
  }
}
</style>
