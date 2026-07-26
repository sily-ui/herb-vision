<template>
  <view class="page-detail">
    <!-- 顶部图：单张静态图，左上角印章 -->
    <view class="banner">
      <image :src="bannerImages[0] || '/static/images/placeholder.png'" mode="aspectFill" class="banner__img" />
      <view class="banner__seal" v-if="herb.id">
        <text class="banner__seal-text">No.{{ String(herb.id).padStart(3, '0') }}</text>
      </view>
    </view>

    <!-- 名讳区：大字 + 别名 -->
    <view class="name-block">
      <text class="name-block__title">{{ herb.name || '药材详录' }}</text>
      <view class="name-block__alias-row" v-if="herb.alias">
        <text class="name-block__alias-label">别名</text>
        <text class="name-block__alias-value">{{ herb.alias }}</text>
      </view>
    </view>

    <!-- 信息卡片：基本信息 -->
    <view class="info-card" v-if="herb.family || herb.source || herb.medicinalPart">
      <view class="info-card__head">
        <text class="info-card__num">壹</text>
        <text class="info-card__title">基本信息</text>
      </view>
      <view class="info-row" v-if="herb.family">
        <text class="info-row__label">科属</text>
        <text class="info-row__value">{{ herb.family }}</text>
      </view>
      <view class="info-row" v-if="herb.source">
        <text class="info-row__label">来源</text>
        <text class="info-row__value">{{ herb.source }}</text>
      </view>
      <view class="info-row" v-if="herb.medicinalPart">
        <text class="info-row__label">药用部位</text>
        <text class="info-row__value">{{ herb.medicinalPart }}</text>
      </view>
    </view>

    <!-- 性味归经 -->
    <view class="info-card" v-if="herb.property">
      <view class="info-card__head">
        <text class="info-card__num">贰</text>
        <text class="info-card__title">性味归经</text>
      </view>
      <text class="info-card__text">{{ herb.property }}</text>
    </view>

    <!-- 功效主治 -->
    <view class="info-card" v-if="herb.efficacy">
      <view class="info-card__head">
        <text class="info-card__num">叁</text>
        <text class="info-card__title">功效主治</text>
      </view>
      <text class="info-card__text">{{ herb.efficacy }}</text>
    </view>

    <!-- 性状鉴别 -->
    <view class="info-card" v-if="herb.appearance">
      <view class="info-card__head">
        <text class="info-card__num">肆</text>
        <text class="info-card__title">性状鉴别</text>
      </view>
      <view class="trait-grid">
        <view class="trait-item" v-if="herb.appearance.color">
          <text class="trait-item__label">色</text>
          <text class="trait-item__value">{{ herb.appearance.color }}</text>
        </view>
        <view class="trait-item" v-if="herb.appearance.texture">
          <text class="trait-item__label">质</text>
          <text class="trait-item__value">{{ herb.appearance.texture }}</text>
        </view>
        <view class="trait-item" v-if="herb.appearance.fracture">
          <text class="trait-item__label">断面</text>
          <text class="trait-item__value">{{ herb.appearance.fracture }}</text>
        </view>
        <view class="trait-item" v-if="herb.appearance.odor">
          <text class="trait-item__label">气</text>
          <text class="trait-item__value">{{ herb.appearance.odor }}</text>
        </view>
      </view>
    </view>

    <!-- 真伪鉴别 -->
    <view class="info-card info-card--accent" v-if="herb.authentication">
      <view class="info-card__head">
        <text class="info-card__num">伍</text>
        <text class="info-card__title">真伪鉴别</text>
        <text class="info-card__tag">关键</text>
      </view>
      <text class="info-card__text">{{ herb.authentication }}</text>
    </view>

    <!-- 用法用量 -->
    <view class="info-card" v-if="herb.usage">
      <view class="info-card__head">
        <text class="info-card__num">陆</text>
        <text class="info-card__title">用法用量</text>
      </view>
      <text class="info-card__text">{{ herb.usage }}</text>
    </view>

    <!-- 禁忌 -->
    <view class="info-card info-card--danger" v-if="herb.contraindication">
      <view class="info-card__head">
        <text class="info-card__num">柒</text>
        <text class="info-card__title">禁忌</text>
        <text class="info-card__tag info-card__tag--danger">慎用</text>
      </view>
      <text class="info-card__text">{{ herb.contraindication }}</text>
    </view>

    <!-- 采收加工 -->
    <view class="info-card" v-if="herb.harvest">
      <view class="info-card__head">
        <text class="info-card__num">捌</text>
        <text class="info-card__title">采收加工</text>
      </view>
      <text class="info-card__text">{{ herb.harvest }}</text>
    </view>

    <!-- 储存 -->
    <view class="info-card" v-if="herb.storage">
      <view class="info-card__head">
        <text class="info-card__num">玖</text>
        <text class="info-card__title">储存条件</text>
      </view>
      <text class="info-card__text">{{ herb.storage }}</text>
    </view>

    <!-- 炮制 -->
    <view class="info-card" v-if="herb.processing">
      <view class="info-card__head">
        <text class="info-card__num">拾</text>
        <text class="info-card__title">炮制方法</text>
      </view>
      <text class="info-card__text">{{ herb.processing }}</text>
    </view>

    <!-- 留白 -->
    <view class="bottom-spacer"></view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar">
      <view class="bottom-bar__fav" :class="{ 'bottom-bar__fav--active': isFavorited }" @click="onToggleFavorite">
        <text class="bottom-bar__fav-icon">{{ isFavorited ? '★' : '☆' }}</text>
        <text class="bottom-bar__fav-text">{{ isFavorited ? '已收藏' : '加入收藏' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 药材详录 · 墨韵版
 * 衬线序号 + 朱砂重点强调
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getHerbDetail } from '@/api/knowledge'
import { addFavorite, removeFavorite } from '@/api/user'
import { useHerbStore } from '@/store/herb'
import { useUserStore } from '@/store/user'
import { saveHerbCache } from '@/utils/cache'
import { resolveImageUrl } from '@/utils/common'

const herbStore = useHerbStore()
const userStore = useUserStore()

const herb = ref({})
const isFavorited = ref(false)
const bannerImages = ref([])

onLoad((query) => {
  if (query.id) loadHerbDetail(query.id)
})

async function loadHerbDetail(id) {
  try {
    const data = await getHerbDetail(id)
    herb.value = data
    isFavorited.value = data.is_favorited || data.isFavorited || false

    const images = []
    if (data.image_main) images.push(resolveImageUrl(data.image_main))
    if (data.image_microscopic) images.push(resolveImageUrl(data.image_microscopic))
    if (data.image_processed) images.push(resolveImageUrl(data.image_processed))
    if (!images.length) images.push('/static/images/placeholder.png')
    bannerImages.value = images

    saveHerbCache(data)

    herbStore.addRecentViewed({
      id: data.id,
      name: data.name,
      image: resolveImageUrl(data.image_main)
    })
  } catch (err) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

async function onToggleFavorite() {
  if (!userStore.isLogin) {
    uni.showToast({ title: '请先登录', icon: 'none' })
    return
  }
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
    uni.showToast({ title: '操作失败', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.page-detail {
  min-height: 100vh;
  background-color: $paper;
  padding-bottom: 160rpx;
}

/* ===== 顶部图 ===== */
.banner {
  position: relative;
  width: 100%;
  height: 480rpx;
  background-color: $paper-deep;

  &__img {
    width: 100%;
    height: 100%;
  }

  &__seal {
    position: absolute;
    top: $space-lg;
    left: $space-lg;
    padding: 4rpx 12rpx;
    background-color: rgba(250, 248, 243, 0.9);
    border: 1rpx solid $line;
    border-radius: $radius-xs;
  }

  &__seal-text {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $cinnabar;
    letter-spacing: 2rpx;
    font-weight: $weight-medium;
  }
}

/* ===== 名讳 ===== */
.name-block {
  padding: $space-xl $space-lg $space-lg;
  background-color: $paper;
  border-bottom: 1rpx solid $line;

  &__title {
    font-size: 72rpx;
    font-weight: $weight-bold;
    color: $ink;
    letter-spacing: 8rpx;
    line-height: 1.2;
    display: block;
  }

  &__alias-row {
    display: flex;
    align-items: baseline;
    gap: $space-sm;
    margin-top: $space-sm;
  }

  &__alias-label {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 2rpx;
  }

  &__alias-value {
    font-size: $font-sm;
    color: $ink-soft;
    letter-spacing: 1rpx;
  }
}

/* ===== 信息卡 ===== */
.info-card {
  margin: $space-sm $space-lg 0;
  padding: $space-lg;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;

  &--accent {
    border-left: 4rpx solid $cinnabar;
  }

  &--danger {
    border-left: 4rpx solid $danger;
  }

  &__head {
    display: flex;
    align-items: center;
    gap: $space-sm;
    margin-bottom: $space-md;
    padding-bottom: $space-sm;
    border-bottom: 1rpx solid $line-soft;
  }

  &__num {
    font-family: $font-serif;
    font-size: $font-md;
    color: $cinnabar;
    font-weight: $weight-medium;
    width: 40rpx;
  }

  &__title {
    flex: 1;
    font-size: $font-lg;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__tag {
    font-size: $font-xs;
    color: $cinnabar;
    padding: 2rpx 10rpx;
    border: 1rpx solid $cinnabar;
    border-radius: $radius-xs;
    letter-spacing: 1rpx;

    &--danger {
      color: #FFFFFF;
      background-color: $danger;
      border-color: $danger;
    }
  }

  &__text {
    font-size: $font-md;
    color: $ink-soft;
    line-height: 1.9;
    letter-spacing: 0.5rpx;
    display: block;
  }
}

.info-row {
  display: flex;
  padding: $space-sm 0;
  border-bottom: 1rpx solid $line-soft;

  &:last-child {
    border-bottom: none;
  }

  &__label {
    width: 140rpx;
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 1rpx;
    flex-shrink: 0;
  }

  &__value {
    flex: 1;
    font-size: $font-md;
    color: $ink;
    letter-spacing: 0.5rpx;
  }
}

/* ===== 性状网格 ===== */
.trait-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rpx;
  background-color: $line;
  border: 1rpx solid $line;
  border-radius: $radius-sm;
  overflow: hidden;
}

.trait-item {
  width: calc(50% - 1rpx);
  padding: $space-md $space-sm;
  background-color: $paper;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-xs;

  &__label {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $cinnabar;
    font-weight: $weight-medium;
    letter-spacing: 2rpx;
  }

  &__value {
    font-size: $font-sm;
    color: $ink-soft;
    text-align: center;
  }
}

/* ===== 底部操作栏 ===== */
.bottom-spacer {
  height: $space-2xl;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: $paper;
  padding: $space-md $space-lg;
  padding-bottom: calc(#{$space-md} + env(safe-area-inset-bottom));
  border-top: 1rpx solid $line;
  z-index: 100;

  &__fav {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: $space-sm;
    padding: $space-md 0;
    border: 1rpx solid $ink;
    border-radius: $radius-sm;
    background-color: $paper;

    &--active {
      background-color: $ink;
    }
  }

  &__fav-icon {
    font-size: $font-md;
    color: $cinnabar;
  }

  &__fav-text {
    font-size: $font-md;
    color: $ink;
    font-weight: $weight-medium;
    letter-spacing: 2rpx;

    .bottom-bar__fav--active & {
      color: #FFFFFF;
    }
  }
}
</style>
