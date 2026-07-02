<template>
  <view class="page-detail">
    <!-- 顶部轮播图 -->
    <swiper class="banner-swiper" indicator-dots autoplay circular>
      <swiper-item v-for="(img, index) in bannerImages" :key="index">
        <image :src="img" mode="aspectFill" class="banner-swiper__img" />
      </swiper-item>
    </swiper>

    <!-- 药典标准名称+别名 -->
    <view class="name-section">
      <text class="name-section__title">{{ herb.name || '药材详情' }}</text>
      <text class="name-section__alias" v-if="herb.alias">别名：{{ herb.alias }}</text>
    </view>

    <!-- 基本信息卡片 -->
    <view class="info-card">
      <text class="info-card__title">基本信息</text>
      <view class="info-row">
        <text class="info-row__label">科属</text>
        <text class="info-row__value">{{ herb.family || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="info-row__label">来源</text>
        <text class="info-row__value">{{ herb.source || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="info-row__label">药用部位</text>
        <text class="info-row__value">{{ herb.medicinalPart || '-' }}</text>
      </view>
    </view>

    <!-- 性味归经 -->
    <view class="info-card">
      <text class="info-card__title">性味归经</text>
      <text class="info-card__text">{{ herb.property || '-' }}</text>
    </view>

    <!-- 功效主治 -->
    <view class="info-card">
      <text class="info-card__title">功效主治</text>
      <text class="info-card__text">{{ herb.efficacy || '-' }}</text>
    </view>

    <!-- 性状鉴别 -->
    <view class="info-card">
      <text class="info-card__title">性状鉴别</text>
      <view class="trait-grid">
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F3A8;</text>
          <text class="trait-item__label">颜色</text>
          <text class="trait-item__value">{{ herb.appearance?.color || '-' }}</text>
        </view>
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F44B;</text>
          <text class="trait-item__label">质地</text>
          <text class="trait-item__value">{{ herb.appearance?.texture || '-' }}</text>
        </view>
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F52D;</text>
          <text class="trait-item__label">断面</text>
          <text class="trait-item__value">{{ herb.appearance?.fracture || '-' }}</text>
        </view>
        <view class="trait-item">
          <text class="trait-item__icon">&#x1F443;</text>
          <text class="trait-item__label">气味</text>
          <text class="trait-item__value">{{ herb.appearance?.odor || '-' }}</text>
        </view>
      </view>
    </view>

    <!-- 真伪鉴别要点 -->
    <view class="info-card">
      <text class="info-card__title">真伪鉴别</text>
      <text class="info-card__text">{{ herb.authentication || '暂无鉴别要点' }}</text>
    </view>

    <!-- 用法用量 -->
    <view class="info-card">
      <text class="info-card__title">用法用量</text>
      <text class="info-card__text">{{ herb.usage || '-' }}</text>
    </view>

    <!-- 禁忌 -->
    <view class="info-card">
      <text class="info-card__title">禁忌</text>
      <text class="info-card__text" :class="{ 'info-card__text--danger': herb.contraindication }">{{ herb.contraindication || '暂无禁忌信息' }}</text>
    </view>

    <!-- 采收加工 -->
    <view class="info-card" v-if="herb.harvest">
      <text class="info-card__title">采收加工</text>
      <text class="info-card__text">{{ herb.harvest }}</text>
    </view>

    <!-- 储存条件 -->
    <view class="info-card" v-if="herb.storage">
      <text class="info-card__title">储存条件</text>
      <text class="info-card__text">{{ herb.storage }}</text>
    </view>

    <!-- 炮制方法 -->
    <view class="info-card" v-if="herb.processing">
      <text class="info-card__title">炮制方法</text>
      <text class="info-card__text">{{ herb.processing }}</text>
    </view>

    <!-- 底部收藏按钮 -->
    <view class="bottom-bar">
      <view class="bottom-bar__fav" :class="{ 'bottom-bar__fav--active': isFavorited }" @click="onToggleFavorite">
        <text class="bottom-bar__fav-icon">{{ isFavorited ? '&#x2B50;' : '&#x2606;' }}</text>
        <text class="bottom-bar__fav-text">{{ isFavorited ? '已收藏' : '收藏' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 药材详情页
 * 完整展示药材信息
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getHerbDetail } from '@/api/knowledge'
import { addFavorite, removeFavorite } from '@/api/user'
import { useHerbStore } from '@/store/herb'
import { saveHerbCache } from '@/utils/cache'

const herbStore = useHerbStore()

const herb = ref({})
const isFavorited = ref(false)
const bannerImages = ref([])

onLoad((query) => {
  if (query.id) {
    loadHerbDetail(query.id)
  }
})

/**
 * 加载药材详情
 */
async function loadHerbDetail(id) {
  try {
    const data = await getHerbDetail(id)
    herb.value = data
    isFavorited.value = data.isFavorited || false

    // 设置轮播图
    const images = []
    if (data.image) images.push(data.image)
    if (data.microscopicImage) images.push(data.microscopicImage)
    if (data.processedImage) images.push(data.processedImage)
    if (!images.length) images.push('/static/images/placeholder.png')
    bannerImages.value = images

    // 缓存药材数据
    saveHerbCache(data)

    // 添加到最近浏览
    herbStore.addRecentViewed({
      id: data.id,
      name: data.name,
      image: data.image
    })
  } catch (err) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

/**
 * 切换收藏
 */
async function onToggleFavorite() {
  try {
    if (isFavorited.value) {
      await removeFavorite(herb.value.id)
      isFavorited.value = false
      uni.showToast({ title: '已取消收藏', icon: 'none' })
    } else {
      await addFavorite(herb.value.id)
      isFavorited.value = true
      uni.showToast({ title: '收藏成功', icon: 'none' })
    }
  } catch (err) {
    // 静默处理
  }
}
</script>

<style lang="scss" scoped>
.page-detail {
  min-height: 100vh;
  background-color: $bg-color;
  padding-bottom: 120rpx;
}

.banner-swiper {
  height: 400rpx;

  &__img {
    width: 100%;
    height: 100%;
  }
}

.name-section {
  background-color: $card-bg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;

  &__title {
    font-size: 48rpx;
    font-weight: 700;
    color: $text-color;
    display: block;
  }

  &__alias {
    font-size: $font-sm;
    color: $text-secondary;
    margin-top: $spacing-xs;
    display: block;
  }
}

.info-card {
  background-color: $card-bg;
  border-radius: $radius-md;
  padding: $spacing-lg;
  margin: 0 $spacing-lg $spacing-md;
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

.info-row {
  display: flex;
  padding: $spacing-sm 0;
  border-bottom: 1rpx solid $border-color;

  &:last-child { border-bottom: none; }

  &__label {
    width: 140rpx;
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

  &__icon { font-size: 40rpx; }
  &__label { font-size: $font-sm; color: $text-secondary; }
  &__value { font-size: $font-md; color: $text-color; font-weight: 500; }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: $card-bg;
  padding: $spacing-md $spacing-lg;
  padding-bottom: calc(#{$spacing-md} + env(safe-area-inset-bottom));
  box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.06);
  z-index: 100;

  &__fav {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: $spacing-sm;
    padding: $spacing-md 0;
    background: linear-gradient(135deg, $primary-color, $secondary-color);
    border-radius: $radius-lg;

    &--active {
      background: $accent-color;
    }
  }

  &__fav-icon { font-size: $font-lg; }
  &__fav-text {
    font-size: $font-lg;
    font-weight: 600;
    color: #FFFFFF;
  }
}
</style>
