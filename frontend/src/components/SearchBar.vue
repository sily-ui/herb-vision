<template>
  <view class="search-bar">
    <view class="search-bar__inner">
      <text class="search-bar__icon">⌕</text>
      <input
        class="search-bar__input"
        :placeholder="placeholder"
        :placeholder-class="'search-bar__placeholder'"
        :value="keyword"
        confirm-type="search"
        @input="onInput"
        @confirm="onSearch"
      />
      <view class="search-bar__btn" v-if="keyword" @click="onClear">
        <text class="search-bar__clear">✕</text>
      </view>
    </view>
    <view class="search-bar__action" @click="onSearch">
      <text class="search-bar__action-text">检索</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 搜索栏 · 墨韵版
 * 细线输入框 + 朱砂"检索"按钮
 */
import { ref } from 'vue'

const props = defineProps({
  placeholder: {
    type: String,
    default: '输入药材名、功效或性状...'
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
  gap: $space-sm;

  &__inner {
    flex: 1;
    display: flex;
    align-items: center;
    background-color: $card;
    border: 1rpx solid $line;
    border-radius: $radius-sm;
    padding: 0 $space-md;
    height: 72rpx;
    gap: $space-sm;
  }

  &__icon {
    font-size: $font-lg;
    color: $ink-light;
  }

  &__input {
    flex: 1;
    font-size: $font-md;
    color: $ink;
    height: 72rpx;
    letter-spacing: 1rpx;
  }

  &__placeholder {
    color: $ink-faint;
  }

  &__clear {
    font-size: $font-sm;
    color: $ink-light;
  }

  &__btn {
    padding: $space-xxs;
  }

  &__action {
    padding: 0 $space-md;
    height: 72rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__action-text {
    font-size: $font-md;
    color: $cinnabar;
    font-weight: $weight-medium;
    letter-spacing: 2rpx;
  }
}
</style>
