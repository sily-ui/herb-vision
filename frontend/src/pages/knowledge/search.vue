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
  </view>
</template>

<script setup>
/**
 * 搜索结果页
 * 搜索药材、搜索历史、热门推荐
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { searchHerbs } from '@/api/knowledge'
import { useHerbStore } from '@/store/herb'
import SearchBar from '@/components/SearchBar.vue'
import HerbCard from '@/components/HerbCard.vue'

const herbStore = useHerbStore()

const searchResults = ref([])
const searched = ref(false)
const searchHistory = ref(herbStore.searchHistory)

const hotKeywords = ref([
  '人参', '黄芪', '当归', '甘草', '白芍',
  '川芎', '茯苓', '白术', '半夏', '柴胡'
])

onLoad((query) => {
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
    searchResults.value = data.list || data || []
  } catch (err) {
    searchResults.value = []
  }
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

  > * {
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
</style>
