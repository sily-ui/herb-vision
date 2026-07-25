<template>
  <view class="page-search">
    <!-- 搜索栏 -->
    <view class="search-wrap">
      <SearchBar :placeholder="'搜索药材...'" @search="onSearch" />
    </view>

    <!-- 搜索结果列表 -->
    <view class="result-list" v-if="searchResults.length">
      <HerbCard
        v-for="(item, index) in searchResults"
        :key="index"
        :herb="item"
        :navigate="!selectMode"
        class="result-list__item"
        :class="{ 'result-list__item--selected': selectMode && selectedId === item.id }"
        @click="onHerbClick(item)"
      />
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
    <view class="select-bar" v-if="selectMode && selectedHerb.id">
      <view class="select-bar__info">
        <text class="select-bar__label">已选择</text>
        <text class="select-bar__name">{{ selectedHerb.name }}</text>
      </view>
      <view class="select-bar__btn" @click="confirmSelect">
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
const selectedHerb = ref({})
const selectedId = computed(() => selectedHerb.value.id)

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
 * 点击药材卡片
 */
function onHerbClick(item) {
  if (!selectMode.value) return
  selectedHerb.value = item
}

/**
 * 确认选择并返回对比页
 */
function confirmSelect() {
  const pages = getCurrentPages()
  const prevPage = pages[pages.length - 2]
  if (prevPage && prevPage.$vm && prevPage.$vm.onHerbSelected) {
    prevPage.$vm.onHerbSelected(selectSide.value, selectedHerb.value)
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
    width: calc(50% - 12rpx);
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

    &-text {
      font-size: $font-md;
      color: #FFFFFF;
      font-weight: 500;
    }
  }
}
</style>
