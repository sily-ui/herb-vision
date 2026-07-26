<template>
  <view class="herb-card" @click="handleClick">
    <!-- 图：方图 + 编号水印 -->
    <view class="herb-card__image">
      <image
        :src="resolveImageUrl(herb.image_main)"
        mode="aspectFill"
        class="herb-card__img"
        @error="onImageError"
      />
      <view class="herb-card__num" v-if="herb.id">
        <text class="herb-card__num-text">No.{{ String(herb.id).padStart(3, '0') }}</text>
      </view>
    </view>
    <!-- 信息区 -->
    <view class="herb-card__info">
      <view class="herb-card__name-row">
        <text class="herb-card__name">{{ herb.name || '未知药材' }}</text>
        <text class="herb-card__family" v-if="herb.family">{{ herb.family }}</text>
      </view>
      <view class="herb-card__tags" v-if="herb.effects && herb.effects.length">
        <text
          class="herb-card__tag"
          v-for="(tag, index) in herb.effects.slice(0, 2)"
          :key="index"
        >{{ tag }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { resolveImageUrl } from '@/utils/common'

const props = defineProps({
  herb: {
    type: Object,
    default: () => ({})
  },
  navigate: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['click'])

function handleClick() {
  if (props.navigate && props.herb.id) {
    uni.navigateTo({
      url: `/pages/knowledge/detail?id=${props.herb.id}`
    })
  }
  emit('click', props.herb)
}

function onImageError() {
  // 图片加载失败时不做处理，依赖 CSS 背景色显示占位效果
}
</script>

<style lang="scss" scoped>
.herb-card {
  display: flex;
  flex-direction: column;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  overflow: hidden;
  flex-shrink: 0;

  &:active {
    background-color: $paper-warm;
  }

  &__image {
    width: 100%;
    height: 200rpx;
    overflow: hidden;
    position: relative;
    background-color: $paper-deep;
  }

  &__img {
    width: 100%;
    height: 100%;
  }

  &__num {
    position: absolute;
    top: $space-sm;
    left: $space-sm;
    padding: 2rpx 8rpx;
    background-color: rgba(250, 248, 243, 0.85);
    backdrop-filter: blur(4rpx);
    border-radius: $radius-xs;
  }

  &__num-text {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $ink-soft;
    letter-spacing: 1rpx;
    font-weight: $weight-medium;
  }

  &__info {
    padding: $space-sm $space-md $space-md;
    display: flex;
    flex-direction: column;
    gap: $space-xs;
  }

  &__name-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: $space-xs;
  }

  &__name {
    font-size: $font-md;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 1rpx;
  }

  &__family {
    font-size: $font-xs;
    color: $ink-light;
    flex-shrink: 0;
  }

  &__tags {
    display: flex;
    flex-wrap: wrap;
    gap: $space-xxs;
  }

  &__tag {
    font-size: $font-xs;
    color: $bamboo;
    background-color: $bamboo-soft;
    padding: 2rpx 10rpx;
    border-radius: $radius-xs;
    letter-spacing: 1rpx;
  }
}
</style>
