<template>
  <view class="page-knowledge">
    <!-- 顶部搜索栏 -->
    <view class="search-wrap">
      <SearchBar placeholder="搜索药材名称、功效..." @search="onSearch" />
    </view>

    <!-- 分类导航：按部位 -->
    <view class="category-section">
      <text class="category-section__title">按部位分类</text>
      <CategoryNav :categories="partCategories" @select="onPartSelect" />
    </view>

    <!-- 分类导航：按功效 -->
    <view class="category-section">
      <text class="category-section__title">按功效分类</text>
      <CategoryNav :categories="effectCategories" @select="onEffectSelect" />
    </view>

    <!-- 药材网格列表 -->
    <view class="herb-grid">
      <view class="herb-grid__item" v-for="(item, index) in herbList" :key="index">
        <HerbCard :herb="item" />
      </view>
    </view>

    <!-- 加载状态 -->
    <view class="loading-tip" v-if="loading">
      <text class="loading-tip__text">加载中...</text>
    </view>
    <view class="loading-tip" v-else-if="!herbList.length">
      <text class="loading-tip__text">暂无药材数据</text>
    </view>
    <view class="loading-tip" v-else-if="noMore">
      <text class="loading-tip__text">没有更多了</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 知识库首页
 * 搜索栏、分类导航、药材列表
 */
import { ref } from 'vue'
import { onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { getHerbs } from '@/api/knowledge'
import { useHerbStore } from '@/store/herb'
import SearchBar from '@/components/SearchBar.vue'
import CategoryNav from '@/components/CategoryNav.vue'
import HerbCard from '@/components/HerbCard.vue'

const herbStore = useHerbStore()

const herbList = ref([])
const loading = ref(false)
const noMore = ref(false)
const page = ref(1)
const pageSize = 20
const currentPart = ref('')
const currentEffect = ref('')

// 按部位分类
const partCategories = ref([
  { name: '全部', value: '' },
  { name: '根及根茎', value: 'root' },
  { name: '茎木', value: 'stem' },
  { name: '皮', value: 'bark' },
  { name: '叶', value: 'leaf' },
  { name: '花', value: 'flower' },
  { name: '果实种子', value: 'fruit' },
  { name: '全草', value: 'herb' },
  { name: '动物类', value: 'animal' },
  { name: '矿物类', value: 'mineral' }
])

// 按功效分类
const effectCategories = ref([
  { name: '全部', value: '' },
  { name: '解表药', value: 'diaphoretic' },
  { name: '清热药', value: 'heat_clearing' },
  { name: '泻下药', value: 'purgative' },
  { name: '祛风湿药', value: 'wind_damp' },
  { name: '化湿药', value: 'damp_resolving' },
  { name: '利水渗湿药', value: 'diuretic' },
  { name: '温里药', value: 'interior_warming' },
  { name: '理气药', value: 'qi_regulating' },
  { name: '消食药', value: 'digestive' },
  { name: '止血药', value: 'hemostatic' },
  { name: '活血化瘀药', value: 'blood_activating' },
  { name: '补虚药', value: 'tonifying' }
])

// 初始加载
loadHerbs()

/**
 * 加载药材列表
 */
async function loadHerbs(reset = false) {
  if (loading.value) return
  if (reset) {
    page.value = 1
    noMore.value = false
  }

  loading.value = true
  try {
    const params = {
      page: page.value,
      pageSize
    }
    if (currentPart.value) params.part = currentPart.value
    if (currentEffect.value) params.category = currentEffect.value

    const data = await getHerbs(params)
    const list = data.list || data || []

    if (reset) {
      herbList.value = list
    } else {
      herbList.value.push(...list)
    }

    if (list.length < pageSize) {
      noMore.value = true
    }
  } catch (err) {
    // 静默处理
  } finally {
    loading.value = false
  }
}

/**
 * 搜索
 */
function onSearch(keyword) {
  herbStore.addSearchHistory(keyword)
  uni.navigateTo({
    url: `/pages/knowledge/search?keyword=${encodeURIComponent(keyword)}`
  })
}

/**
 * 按部位选择
 */
function onPartSelect({ item }) {
  currentPart.value = item.value || ''
  loadHerbs(true)
}

/**
 * 按功效选择
 */
function onEffectSelect({ item }) {
  currentEffect.value = item.value || ''
  loadHerbs(true)
}

// 下拉刷新
onPullDownRefresh(() => {
  loadHerbs(true).then(() => {
    uni.stopPullDownRefresh()
  })
})

// 上拉加载更多
onReachBottom(() => {
  if (!noMore.value) {
    page.value++
    loadHerbs()
  }
})
</script>

<style lang="scss" scoped>
.page-knowledge {
  min-height: 100vh;
  background-color: $bg-color;
}

.search-wrap {
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
}

.category-section {
  padding: $spacing-sm $spacing-lg;
  background-color: $card-bg;
  margin-bottom: $spacing-sm;

  &__title {
    font-size: $font-sm;
    color: $text-secondary;
    display: block;
    margin-bottom: $spacing-xs;
  }
}

.herb-grid {
  display: flex;
  flex-wrap: wrap;
  padding: $spacing-md;
  gap: $spacing-md;

  &__item {
    width: calc(50% - 12rpx);
  }
}

.loading-tip {
  padding: $spacing-xl 0;
  text-align: center;

  &__text {
    font-size: $font-sm;
    color: $text-secondary;
  }
}
</style>
