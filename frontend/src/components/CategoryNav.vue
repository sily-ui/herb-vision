<template>
  <scroll-view class="category-nav" scroll-x enable-flex>
    <view
      class="category-nav__item"
      :class="{ 'category-nav__item--active': activeIndex === index }"
      v-for="(item, index) in categories"
      :key="index"
      @click="onSelect(index, item)"
    >
      <text class="category-nav__text">{{ item.name || item }}</text>
    </view>
  </scroll-view>
</template>

<script setup>
/**
 * 分类导航 · 墨韵版
 * 文字下划线式选中态（无背景色块）
 */
import { ref } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  active: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['select'])

const activeIndex = ref(props.active)

function onSelect(index, item) {
  activeIndex.value = index
  emit('select', { index, item })
}
</script>

<style lang="scss" scoped>
.category-nav {
  white-space: nowrap;
  padding: $space-sm $space-md;
  display: flex;

  &__item {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: $space-xs $space-md;
    margin-right: $space-sm;
    flex-shrink: 0;
    position: relative;

    &:last-child {
      margin-right: 0;
    }

    &--active {
      .category-nav__text {
        color: $ink;
        font-weight: $weight-semibold;
      }

      &::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 32rpx;
        height: 2rpx;
        background-color: $cinnabar;
      }
    }
  }

  &__text {
    font-size: $font-md;
    color: $ink-light;
    letter-spacing: 1rpx;
  }
}
</style>
