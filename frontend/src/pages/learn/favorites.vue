<template>
  <view class="page-favorites">
    <!-- 分类筛选 -->
    <view class="filter-bar">
      <CategoryNav :categories="filterCategories" @select="onFilterSelect" />
    </view>

    <!-- 收藏列表 -->
    <view class="fav-list" v-if="favoriteList.length">
      <view
        class="fav-item"
        v-for="(item, index) in favoriteList"
        :key="index"
        @click="goDetail(item)"
      >
        <image :src="item.image || '/static/images/placeholder.png'" mode="aspectFill" class="fav-item__img" />
        <view class="fav-item__info">
          <text class="fav-item__name">{{ item.name }}</text>
          <text class="fav-item__family">{{ item.family || '' }}</text>
        </view>
        <view class="fav-item__action" @click.stop="onRemoveFavorite(item, index)">
          <text class="fav-item__remove">&#x2715;</text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-else-if="!loading">
      <text class="empty-state__icon">&#x2B50;</text>
      <text class="empty-state__text">{{ userStore.isLogin ? '还没有收藏任何药材' : '请先登录' }}</text>
      <text class="empty-state__hint">{{ userStore.isLogin ? '去知识库浏览并收藏感兴趣的药材吧' : '登录后查看收藏的药材' }}</text>
    </view>

    <!-- 加载状态 -->
    <view class="loading-tip" v-if="loading">
      <text class="loading-tip__text">加载中...</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 收藏夹
 * 按分类筛选、取消收藏
 */
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { getFavorites, removeFavorite } from '@/api/user'
import { resolveImageUrl } from '@/utils/common'
import CategoryNav from '@/components/CategoryNav.vue'

const userStore = useUserStore()
const favoriteList = ref([])
const loading = ref(false)
const currentFilter = ref('')

const filterCategories = ref([
  { name: '全部', value: '' },
  { name: '根及根茎', value: '根及根茎' },
  { name: '花', value: '花' },
  { name: '果实种子', value: '果实种子' },
  { name: '全草或叶', value: '全草或叶' }
])

onShow(() => {
  userStore.checkLogin()
  if (userStore.isLogin) {
    loadFavorites()
  } else {
    favoriteList.value = []
    loading.value = false
  }
})

/**
 * 加载收藏列表
 */
async function loadFavorites() {
  loading.value = true
  try {
    const params = { page: 1, pageSize: 50 }
    if (currentFilter.value) params.category = currentFilter.value
    const data = await getFavorites(params)
    const list = data.items || data.list || data || []
    favoriteList.value = list.map((item) => ({
      ...item,
      image: resolveImageUrl(item.image_main || item.image)
    }))
  } catch (err) {
    favoriteList.value = []
  } finally {
    loading.value = false
  }
}

/**
 * 筛选选择
 */
function onFilterSelect({ item }) {
  currentFilter.value = item.value || ''
  loadFavorites()
}

/**
 * 取消收藏
 */
async function onRemoveFavorite(item, index) {
  try {
    await removeFavorite(item.herb_id)
    favoriteList.value.splice(index, 1)
    uni.showToast({ title: '已取消收藏', icon: 'none' })
  } catch (err) {
    // 静默处理
  }
}

/**
 * 跳转详情
 */
function goDetail(item) {
  uni.navigateTo({
    url: `/pages/knowledge/detail?id=${item.herb_id}`
  })
}
</script>

<style lang="scss" scoped>
.page-favorites {
  min-height: 100vh;
  background-color: $bg-color;
}

.filter-bar {
  padding: $spacing-sm $spacing-lg;
  background-color: $card-bg;
}

.fav-list {
  padding: $spacing-md $spacing-lg;
}

.fav-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  background-color: $card-bg;
  border-radius: $radius-md;
  margin-bottom: $spacing-md;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
  gap: $spacing-md;

  &__img {
    width: 120rpx;
    height: 120rpx;
    border-radius: $radius-sm;
    background-color: $border-color;
    flex-shrink: 0;
  }

  &__info {
    flex: 1;
  }

  &__name {
    font-size: $font-lg;
    font-weight: 500;
    color: $text-color;
    display: block;
  }

  &__family {
    font-size: $font-sm;
    color: $text-secondary;
    display: block;
    margin-top: $spacing-xs;
  }

  &__action {
    padding: $spacing-sm;
  }

  &__remove {
    font-size: $font-lg;
    color: $text-secondary;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 0;
  gap: $spacing-md;

  &__icon {
    font-size: 80rpx;
  }

  &__text {
    font-size: $font-lg;
    color: $text-color;
    font-weight: 500;
  }

  &__hint {
    font-size: $font-sm;
    color: $text-secondary;
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
