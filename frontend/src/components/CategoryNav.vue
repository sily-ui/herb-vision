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
 * 分类导航组件
 * 横向滚动展示分类标签，点击选中
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
  padding: $spacing-sm 0;
  display: flex;
  gap: $spacing-sm;

  &__item {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12rpx $spacing-lg;
    border-radius: $radius-lg;
    background-color: $bg-color;
    flex-shrink: 0;

    &--active {
      background-color: $primary-color;

      .category-nav__text {
        color: #FFFFFF;
      }
    }
  }

  &__text {
    font-size: $font-md;
    color: $text-color;
  }
}
</style>
