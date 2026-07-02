<template>
  <view class="herb-card" @click="handleClick">
    <!-- 缩略图 -->
    <view class="herb-card__image">
      <image
        :src="herb.image || '/static/images/placeholder.png'"
        mode="aspectFill"
        class="herb-card__img"
      />
    </view>
    <!-- 信息区 -->
    <view class="herb-card__info">
      <text class="herb-card__name">{{ herb.name || '未知药材' }}</text>
      <text class="herb-card__family">{{ herb.family || '' }}</text>
      <!-- 功效标签 -->
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
/**
 * 药材卡片组件
 * 展示缩略图、名称、科属、功效标签，点击跳转详情
 */
const props = defineProps({
  herb: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['click'])

function handleClick() {
  if (props.herb.id) {
    uni.navigateTo({
      url: `/pages/knowledge/detail?id=${props.herb.id}`
    })
  }
  emit('click', props.herb)
}
</script>

<style lang="scss" scoped>
.herb-card {
  display: flex;
  flex-direction: column;
  background-color: $card-bg;
  border-radius: $radius-md;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);

  &__image {
    width: 100%;
    height: 240rpx;
    overflow: hidden;
  }

  &__img {
    width: 100%;
    height: 100%;
  }

  &__info {
    padding: $spacing-sm $spacing-md;
    display: flex;
    flex-direction: column;
    gap: $spacing-xs;
  }

  &__name {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
  }

  &__family {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__tags {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-xs;
    margin-top: $spacing-xs;
  }

  &__tag {
    font-size: $font-xs;
    color: $primary-color;
    background-color: $accent-color;
    padding: 4rpx 12rpx;
    border-radius: $radius-sm;
  }
}
</style>
