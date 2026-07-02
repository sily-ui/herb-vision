<template>
  <view class="search-bar">
    <view class="search-bar__inner">
      <text class="search-bar__icon">&#x1F50D;</text>
      <input
        class="search-bar__input"
        :placeholder="placeholder"
        :value="keyword"
        confirm-type="search"
        @input="onInput"
        @confirm="onSearch"
      />
      <view class="search-bar__btn" v-if="keyword" @click="onClear">
        <text class="search-bar__clear">&#x2715;</text>
      </view>
    </view>
    <view class="search-bar__action" @click="onSearch">
      <text class="search-bar__action-text">搜索</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 搜索栏组件
 * 支持输入关键词、搜索按钮、placeholder可配置
 */
import { ref } from 'vue'

const props = defineProps({
  placeholder: {
    type: String,
    default: '搜索药材名称、功效...'
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['search', 'update:modelValue'])

const keyword = ref(props.modelValue)

function onInput(e) {
  keyword.value = e.detail.value
  emit('update:modelValue', e.detail.value)
}

function onSearch() {
  if (keyword.value.trim()) {
    emit('search', keyword.value.trim())
  }
}

function onClear() {
  keyword.value = ''
  emit('update:modelValue', '')
}
</script>

<style lang="scss" scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: $spacing-sm;

  &__inner {
    flex: 1;
    display: flex;
    align-items: center;
    background-color: $bg-color;
    border-radius: $radius-lg;
    padding: 0 $spacing-md;
    height: 72rpx;
    gap: $spacing-sm;
  }

  &__icon {
    font-size: $font-lg;
  }

  &__input {
    flex: 1;
    font-size: $font-md;
    color: $text-color;
    height: 72rpx;
  }

  &__clear {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__btn {
    padding: 8rpx;
  }

  &__action {
    padding: 0 $spacing-md;
    height: 72rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__action-text {
    font-size: $font-md;
    color: $primary-color;
    font-weight: 500;
  }
}
</style>
