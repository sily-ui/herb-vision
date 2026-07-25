<template>
  <view class="page-knowledge">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <SearchBar placeholder="检索药材名、功效、性状..." @search="onSearch" />
    </view>

    <!-- 分类筛选 -->
    <view class="filter">
      <!-- 部位 -->
      <view class="filter__row">
        <text class="filter__label">部位</text>
        <scroll-view class="filter__scroll" scroll-x enable-flex>
          <view
            v-for="(item, index) in partCategories"
            :key="'p'+index"
            class="filter__chip"
            :class="{ 'filter__chip--active': partIndex === index }"
            @click="onPartSelect(index, item)"
          >
            <text class="filter__chip-text">{{ item.name }}</text>
          </view>
        </scroll-view>
      </view>

      <!-- 功效 -->
      <view class="filter__row">
        <text class="filter__label">功效</text>
        <scroll-view class="filter__scroll" scroll-x enable-flex>
          <view
            v-for="(item, index) in effectCategories"
            :key="'e'+index"
            class="filter__chip"
            :class="{ 'filter__chip--active': effectIndex === index }"
            @click="onEffectSelect(index, item)"
          >
            <text class="filter__chip-text">{{ item.name }}</text>
          </view>
        </scroll-view>
      </view>
    </view>

    <!-- 数量 + 视图切换 -->
    <view class="count">
      <text class="count__text">共 {{ total }} 味</text>
      <text class="count__toggle" @click="viewMode = viewMode === 'grid' ? 'table' : 'grid'">
        {{ viewMode === 'grid' ? '表格' : '卡片' }}
      </text>
    </view>

    <!-- 列表 -->
    <view v-if="herbList.length">
      <view v-if="viewMode === 'grid'" class="herb-grid">
        <view
          v-for="item in herbList"
          :key="item.id"
          class="herb-grid__item"
        >
          <HerbCard :herb="item" />
        </view>
      </view>

      <view v-else class="herb-table">
        <view class="herb-table__head">
          <text class="herb-table__col herb-table__col--idx">#</text>
          <text class="herb-table__col herb-table__col--name">药材名</text>
          <text class="herb-table__col herb-table__col--part">部位</text>
          <text class="herb-table__col herb-table__col--effect">功效</text>
        </view>
        <view
          v-for="(item, index) in herbList"
          :key="item.id"
          class="herb-table__row"
          @click="goDetail(item)"
        >
          <text class="herb-table__col herb-table__col--idx">{{ index + 1 }}</text>
          <text class="herb-table__col herb-table__col--name">{{ item.name }}</text>
          <text class="herb-table__col herb-table__col--part">{{ item.category_part || '-' }}</text>
          <text class="herb-table__col herb-table__col--effect">{{ item.category_efficacy || '-' }}</text>
        </view>
      </view>
    </view>

    <!-- 状态 -->
    <view v-if="loading" class="status">
      <text class="status__text">采撷中…</text>
    </view>

    <view v-else-if="!herbList.length && loadError" class="status">
      <text class="status__text">{{ loadError }}</text>
      <view class="status__retry" @click="loadHerbs(true)">
        <text class="status__retry-text">点击重试</text>
      </view>
    </view>

    <view v-else-if="!herbList.length" class="status">
      <text class="status__text">本类暂无记录</text>
    </view>

    <view v-else-if="!noMore" class="status" @click="loadMore">
      <text class="status__text status__text--clickable">点击加载更多</text>
    </view>

    <view v-else class="status">
      <text class="status__text">— 已至卷末 —</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 知识库 · 按分类罗列
 */
import { ref } from 'vue'
import { onShow, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { getHerbs } from '@/api/knowledge'
import { useHerbStore } from '@/store/herb'
import SearchBar from '@/components/SearchBar.vue'
import HerbCard from '@/components/HerbCard.vue'

const herbStore = useHerbStore()

const herbList = ref([])
const loading = ref(false)
const loadError = ref('')
const noMore = ref(false)
const page = ref(1)
const total = ref(0)
const pageSize = 20
const viewMode = ref('grid')

// 部位（value 须与后端 herbs.category_part 一致）
const partCategories = ref([
  { name: '全部', value: '' },
  { name: '根及根茎', value: '根及根茎' },
  { name: '茎木', value: '茎木' },
  { name: '皮', value: '皮' },
  { name: '叶', value: '叶' },
  { name: '花', value: '花' },
  { name: '果实种子', value: '果实种子' },
  { name: '全草', value: '全草' },
  { name: '动物类', value: '动物类' },
  { name: '矿物类', value: '矿物类' }
])

// 功效（value 须与后端 herbs.category_efficacy 一致）
const effectCategories = ref([
  { name: '全部', value: '' },
  { name: '解表', value: '解表' },
  { name: '清热', value: '清热' },
  { name: '泻下', value: '泻下' },
  { name: '祛风湿', value: '祛风湿' },
  { name: '化湿', value: '化湿' },
  { name: '利水渗湿', value: '利水渗湿' },
  { name: '温里', value: '温里' },
  { name: '理气', value: '理气' },
  { name: '消食', value: '消食' },
  { name: '止血', value: '止血' },
  { name: '活血化瘀', value: '活血化瘀' },
  { name: '补益', value: '补益' }
])

const currentPart = ref('')
const currentEffect = ref('')
const partIndex = ref(0)
const effectIndex = ref(0)

onShow(() => {
  if (!herbList.value.length) {
    loadHerbs(true)
  }
})

onPullDownRefresh(() => {
  loadHerbs(true).finally(() => uni.stopPullDownRefresh())
})

onReachBottom(() => {
  if (!noMore.value && !loading.value) {
    loadMore()
  }
})

async function loadHerbs(reset = false) {
  if (loading.value) return
  if (reset) {
    page.value = 1
    noMore.value = false
    loadError.value = ''
  }

  loading.value = true
  try {
    const data = await getHerbs({
      page: page.value,
      pageSize,
      categoryPart: currentPart.value || undefined,
      categoryEfficacy: currentEffect.value || undefined
    })
    const list = data.items || data.list || data || []
    if (reset) {
      herbList.value = list
    } else {
      herbList.value.push(...list)
    }
    total.value = data.total || list.length
    if (list.length < pageSize) noMore.value = true
  } catch (err) {
    if (reset) {
      herbList.value = []
      total.value = 0
    }
    loadError.value = '连接服务失败，请确认后端已启动'
  } finally {
    loading.value = false
  }
}

function loadMore() {
  page.value += 1
  loadHerbs()
}

function onSearch(keyword) {
  if (!keyword || !keyword.trim()) return
  herbStore.addSearchHistory(keyword)
  uni.navigateTo({
    url: `/pages/knowledge/search?keyword=${encodeURIComponent(keyword)}`
  })
}

function onPartSelect(index, item) {
  partIndex.value = index
  currentPart.value = item.value || ''
  loadHerbs(true)
}

function onEffectSelect(index, item) {
  effectIndex.value = index
  currentEffect.value = item.value || ''
  loadHerbs(true)
}

function goDetail(item) {
  uni.navigateTo({ url: `/pages/knowledge/detail?id=${item.id}` })
}
</script>

<style lang="scss" scoped>
.page-knowledge {
  min-height: 100vh;
  background-color: $paper;
  padding-bottom: $space-3xl;
}

/* 搜索栏 */
.search-bar {
  padding: $space-md $space-lg;
  background-color: $paper;
}

/* 分类筛选 */
.filter {
  background-color: $paper;
  padding: 0 $space-lg $space-sm;

  &__row {
    display: flex;
    align-items: center;
    padding: $space-sm 0;
  }

  &__label {
    font-size: $font-sm;
    color: $ink-light;
    width: 56rpx;
    flex-shrink: 0;
    letter-spacing: 1rpx;
  }

  &__scroll {
    flex: 1;
    white-space: nowrap;
  }

  &__chip {
    display: inline-flex;
    align-items: center;
    padding: 8rpx 22rpx;
    margin-right: 16rpx;
    border-radius: 100rpx;
    background-color: $card;
    border: 1rpx solid $line;
    transition: all 0.2s;
    flex-shrink: 0;

    &--active {
      background-color: $ink;
      border-color: $ink;

      .filter__chip-text {
        color: $card;
        font-weight: $weight-medium;
      }
    }
  }

  &__chip-text {
    font-size: $font-sm;
    color: $ink-soft;
    letter-spacing: 1rpx;
  }
}

/* 数量 */
.count {
  padding: $space-md $space-lg $space-sm;

  &__text {
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 1rpx;
  }
}

/* 列表 */
.herb-grid {
  display: flex;
  flex-wrap: wrap;
  padding: 0 $space-lg;
  gap: $space-md;

  &__item {
    width: calc(50% - 12rpx);
  }
}

/* 表格 */
.herb-table {
  margin: 0 $space-lg;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  overflow: hidden;

  &__head {
    display: flex;
    background-color: $paper-deep;
    padding: $space-sm $space-md;
    border-bottom: 1rpx solid $line;
  }

  &__row {
    display: flex;
    padding: $space-md;
    border-bottom: 1rpx solid $line;
    background-color: $card;
    transition: background-color 0.2s;

    &:last-child {
      border-bottom: none;
    }

    &:active {
      background-color: $paper-warm;
    }
  }

  &__col {
    font-size: $font-sm;
    color: $ink;
    letter-spacing: 1rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;

    &--idx {
      width: 64rpx;
      flex-shrink: 0;
      text-align: center;
      font-family: $font-serif;
      color: $ink-light;
    }

    &--name {
      flex: 2;
      font-weight: $weight-semibold;
    }

    &--part {
      flex: 1;
      color: $ink-soft;
    }

    &--effect {
      flex: 2;
      color: $ink-soft;
    }
  }
}

/* 状态 */
.status {
  padding: $space-2xl 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-md;

  &__text {
    font-size: $font-sm;
    color: $ink-faint;
    letter-spacing: 2rpx;

    &--clickable {
      color: $ink-light;
    }
  }

  &__retry {
    padding: 12rpx 32rpx;
    border: 1rpx solid $line;
    border-radius: $radius-sm;
    background-color: $card;
  }

  &__retry-text {
    font-size: $font-sm;
    color: $ink-soft;
    letter-spacing: 2rpx;
  }
}
</style>
