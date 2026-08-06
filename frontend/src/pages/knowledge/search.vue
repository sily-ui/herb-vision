<template>
  <view class="page-search">
    <!-- 搜索栏 -->
    <view class="search-wrap">
      <SearchBar :placeholder="'搜索药材...'" @search="onSearch" />
    </view>

    <!-- 搜索结果列表 -->
    <view class="result-list" v-if="searchResults.length">
      <view
        v-for="(item, index) in searchResults"
        :key="index"
        class="result-list__item-wrap"
        :class="{ 'result-list__item-wrap--selected': selectedId === item.id }"
        @click="onWrapClick(item)"
      >
        <HerbCard
          :herb="item"
          :navigate="false"
          class="result-list__item"
        />
        <!-- 显式勾选框（通用选择模式或对比选择模式都显示） -->
        <view
          v-if="selectMode"
          class="select-circle"
          :class="{ 'select-circle--active': selectedId === item.id }"
          @click.stop="onWrapClick(item)"
        >
          <text v:if="selectedId === item.id" class="select-circle__icon">&#x2713;</text>
        </view>
      </view>
    </view>

    <!-- 无结果 -->
    <view class="empty-state" v-else-if="searched">
      <text class="empty-state__text">未找到相关药材</text>
    </view>

    <!-- 搜索历史+热门推荐 -->
    <view class="search-extra" v-if="!searchResults.length && !searched">
      <!-- 搜索历史 -->
      <view class="history-section" v-if="searchHistory.length">
        <view class="section-header">
          <text class="section-header__title">搜索历史</text>
          <text class="section-header__clear" @click="onClearHistory">清除</text>
        </view>
        <view class="tag-list">
          <text
            class="tag-item"
            v-for="(item, index) in searchHistory"
            :key="index"
            @click="onSearch(item)"
          >{{ item }}</text>
        </view>
      </view>

      <!-- 热门搜索 -->
      <view class="history-section">
        <view class="section-header">
          <text class="section-header__title">热门搜索</text>
        </view>
        <view class="tag-list">
          <text
            class="tag-item tag-item--hot"
            v-for="(item, index) in hotKeywords"
            :key="index"
            @click="onSearch(item)"
          >{{ item }}</text>
        </view>
      </view>
    </view>

    <!-- 选择模式底部确认栏 -->
    <view class="select-bar" v-if="selectMode">
      <view class="select-bar__info">
        <text class="select-bar__label">已选择</text>
        <text class="select-bar__name">{{ selectedName || '请勾选药材' }}</text>
      </view>
      <view
        class="select-bar__btn"
        :class="{ 'select-bar__btn--disabled': !selectedId }"
        @click="confirmSelect"
      >
        <text class="select-bar__btn-text">确认选择</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 搜索结果页
 * 搜索药材、搜索历史、热门推荐
 */
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { searchHerbs } from '@/api/knowledge'
import { useHerbStore } from '@/store/herb'
import SearchBar from '@/components/SearchBar.vue'
import HerbCard from '@/components/HerbCard.vue'

const herbStore = useHerbStore()

const searchResults = ref([])
const searched = ref(false)
const searchHistory = ref(herbStore.searchHistory)
const selectMode = ref(false)
const selectSide = ref(0)
// 用基本类型存储，避免 ref 包装对象在跨函数传值时的引用问题
const selectedId = ref(null)
const selectedName = ref('')

const hotKeywords = ref([
  '人参', '黄芪', '当归', '甘草', '白芍',
  '川芎', '茯苓', '白术', '半夏', '柴胡'
])

onLoad((query) => {
  // 支持从对比页进入选择模式：select=compare1 或 select=compare2
  if (query.select && query.select.startsWith('compare')) {
    selectMode.value = true
    selectSide.value = Number(query.select.replace('compare', '')) || 0
  }
  // 通用选择模式：来自意见反馈页等（mode=select）
  if (query.mode === 'select') {
    selectMode.value = true
    selectSide.value = 0
  }
  if (query.keyword) {
    onSearch(query.keyword)
  }
})

/**
 * 搜索
 */
async function onSearch(keyword) {
  if (!keyword || !keyword.trim()) return

  herbStore.addSearchHistory(keyword)
  searchHistory.value = herbStore.searchHistory
  searched.value = true

  try {
    const data = await searchHerbs(keyword)
    searchResults.value = data.items || data.list || data || []
  } catch (err) {
    searchResults.value = []
  }
}

/**
 * 卡片（或勾选框）点击：单选切换
 * 不再直接 confirmSelect，由底部"确认选择"统一返回
 */
function onWrapClick(item) {
  if (!selectMode.value) return
  if (!item || item.id == null) return
  // 同一卡片再次点击取消选中；不同卡片则切换
  if (selectedId.value === item.id) {
    selectedId.value = null
    selectedName.value = ''
  } else {
    selectedId.value = item.id
    selectedName.value = item.name || ''
  }
}

/**
 * 确认选择并返回上一页
 * @param {object} [herb] 兼容旧 API：直接传入药材对象
 */
function confirmSelect(herb) {
  // 优先用传入对象，否则用本地选中状态
  let data = null
  if (herb && herb.id) {
    data = { id: herb.id, name: herb.name || '' }
  } else if (selectedId.value) {
    data = { id: selectedId.value, name: selectedName.value }
  }

  if (!data || !data.id) {
    uni.showToast({ title: '请先选择药材', icon: 'none' })
    return
  }

  // 通用选择模式：写到本地存储并触发全局事件（双保险）
  if (!selectSide.value) {
    try { uni.setStorageSync('__selectedHerb', data) } catch (e) {}
    uni.$emit('selectHerb', data)
  } else {
    // 对比页选择模式：兼容旧逻辑
    const pages = getCurrentPages()
    const prevPage = pages[pages.length - 2]
    if (prevPage && prevPage.$vm && prevPage.$vm.onHerbSelected) {
      prevPage.$vm.onHerbSelected(selectSide.value, data)
    }
  }
  uni.navigateBack()
}

/**
 * 清除搜索历史
 */
function onClearHistory() {
  herbStore.clearSearchHistory()
  searchHistory.value = []
}
</script>

<style lang="scss" scoped>
.page-search {
  min-height: 100vh;
  background-color: $bg-color;
}

.search-wrap {
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
}

.result-list {
  display: flex;
  flex-wrap: wrap;
  padding: $spacing-md;
  gap: $spacing-md;

  &__item {
    width: 100%;
  }

  &__item-wrap {
    position: relative;
    width: calc(50% - 12rpx);

    &--selected {
      box-shadow: 0 0 0 4rpx $primary-color;
      border-radius: $radius-md;
    }
  }
}

/* 显式勾选框：卡片右上角 */
.select-circle {
  position: absolute;
  top: 12rpx;
  right: 12rpx;
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.95);
  border: 2rpx solid $line-strong;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.12);

  &--active {
    background-color: $primary-color;
    border-color: $primary-color;
  }

  &__icon {
    color: #FFFFFF;
    font-size: 28rpx;
    font-weight: $weight-bold;
    line-height: 1;
  }
}

.empty-state {
  padding: 80rpx 0;
  text-align: center;

  &__text {
    font-size: $font-md;
    color: $text-secondary;
  }
}

.search-extra {
  padding: $spacing-lg;
}

.history-section {
  margin-bottom: $spacing-xl;
}

.section-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: $spacing-md;

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
  }

  &__clear {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;
}

.tag-item {
  font-size: $font-sm;
  color: $text-color;
  background-color: $accent-color;
  padding: 12rpx $spacing-lg;
  border-radius: $radius-lg;

  &--hot {
    color: $primary-color;
    background-color: $accent-color;
  }
}

.result-list__item--selected {
  box-shadow: 0 0 0 4rpx $primary-color;
}

.select-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md $spacing-lg;
  padding-bottom: calc(#{$spacing-md} + env(safe-area-inset-bottom));
  background-color: $card-bg;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.06);
  z-index: 100;

  &__info {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  &__label {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__name {
    font-size: $font-lg;
    font-weight: 600;
    color: $primary-color;
  }

  &__btn {
    padding: $spacing-sm $spacing-lg;
    background-color: $primary-color;
    border-radius: $radius-lg;
    transition: opacity 0.2s;

    &--disabled {
      opacity: 0.4;
    }

    &-text {
      font-size: $font-md;
      color: #FFFFFF;
      font-weight: 500;
    }
  }
}
</style>
