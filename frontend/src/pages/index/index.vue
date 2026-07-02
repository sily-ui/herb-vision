<template>
  <view class="page-index">
    <!-- 自定义导航栏 -->
    <view class="nav-bar">
      <view class="nav-bar__content">
        <text class="nav-bar__title">AI中药识别</text>
      </view>
    </view>

    <!-- 顶部欢迎语+搜索栏 -->
    <view class="header">
      <view class="header__welcome">
        <text class="header__greeting">你好，{{ userName }}</text>
        <text class="header__desc">拍照识别中药材，获取详细信息</text>
      </view>
      <SearchBar placeholder="搜索药材名称、功效..." @search="onSearch" />
    </view>

    <!-- 识别入口按钮 -->
    <view class="identify-actions">
      <view class="identify-actions__item identify-actions__item--camera" @click="goCamera">
        <text class="identify-actions__icon">&#x1F4F7;</text>
        <text class="identify-actions__name">拍照识别</text>
        <text class="identify-actions__desc">打开相机拍摄药材</text>
      </view>
      <view class="identify-actions__item identify-actions__item--album" @click="goAlbum">
        <text class="identify-actions__icon">&#x1F5BC;</text>
        <text class="identify-actions__name">相册上传</text>
        <text class="identify-actions__desc">从相册选择图片识别</text>
      </view>
    </view>

    <!-- 常见混淆药材快捷对比 -->
    <view class="section">
      <view class="section__header">
        <text class="section__title">常见混淆药材</text>
        <text class="section__more" @click="goCompare">更多 &#x276F;</text>
      </view>
      <view class="compare-list">
        <view
          class="compare-item"
          v-for="(item, index) in comparePairs"
          :key="index"
          @click="goCompareDetail(item)"
        >
          <view class="compare-item__left">
            <text class="compare-item__name">{{ item.name1 }}</text>
          </view>
          <text class="compare-item__vs">VS</text>
          <view class="compare-item__right">
            <text class="compare-item__name">{{ item.name2 }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 最近识别记录 -->
    <view class="section">
      <view class="section__header">
        <text class="section__title">最近识别</text>
        <text class="section__more" @click="goRecords">全部 &#x276F;</text>
      </view>
      <scroll-view class="recent-scroll" scroll-x enable-flex v-if="recentRecords.length">
        <view
          class="recent-item"
          v-for="(item, index) in recentRecords"
          :key="index"
          @click="goDetail(item)"
        >
          <image :src="item.image || '/static/images/placeholder.png'" mode="aspectFill" class="recent-item__img" />
          <text class="recent-item__name">{{ item.name }}</text>
        </view>
      </scroll-view>
      <view class="empty-tip" v-else>
        <text class="empty-tip__text">暂无识别记录，快去识别吧</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 首页
 * 顶部欢迎语+搜索栏，识别入口按钮，常见混淆药材对比，最近识别记录
 */
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { useHerbStore } from '@/store/herb'
import { getRecords } from '@/api/user'
import SearchBar from '@/components/SearchBar.vue'

const userStore = useUserStore()
const herbStore = useHerbStore()

const userName = ref('药友')
const recentRecords = ref([])

// 常见混淆药材对
const comparePairs = ref([
  { name1: '赤芍', name2: '白芍', id1: 1, id2: 2 },
  { name1: '黄芪', name2: '红芪', id1: 3, id2: 4 },
  { name1: '半夏', name2: '水半夏', id1: 5, id2: 6 },
  { name1: '柴胡', name2: '银柴胡', id1: 7, id2: 8 },
  { name1: '人参', name2: '党参', id1: 9, id2: 10 }
])

onShow(() => {
  if (userStore.isLogin) {
    userName.value = userStore.nickname
    loadRecentRecords()
  }
})

/**
 * 加载最近识别记录
 */
async function loadRecentRecords() {
  try {
    const data = await getRecords({ page: 1, pageSize: 5 })
    recentRecords.value = data.list || []
  } catch (err) {
    // 静默处理
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
 * 拍照识别
 */
function goCamera() {
  uni.navigateTo({
    url: '/pages/identify/index?source=camera'
  })
}

/**
 * 相册识别
 */
function goAlbum() {
  uni.navigateTo({
    url: '/pages/identify/index?source=album'
  })
}

/**
 * 跳转对比页
 */
function goCompare() {
  uni.navigateTo({
    url: '/pages/compare/index'
  })
}

/**
 * 跳转对比详情
 */
function goCompareDetail(item) {
  uni.navigateTo({
    url: `/pages/compare/index?id1=${item.id1}&id2=${item.id2}`
  })
}

/**
 * 跳转识别记录
 */
function goRecords() {
  uni.navigateTo({
    url: '/pages/mine/records'
  })
}

/**
 * 跳转药材详情
 */
function goDetail(item) {
  if (item.herbId) {
    uni.navigateTo({
      url: `/pages/knowledge/detail?id=${item.herbId}`
    })
  }
}
</script>

<style lang="scss" scoped>
.page-index {
  min-height: 100vh;
  background-color: $bg-color;
}

/* 自定义导航栏 */
.nav-bar {
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  padding-top: var(--status-bar-height, 44rpx);

  &__content {
    height: 88rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__title {
    font-size: $font-xl;
    font-weight: 600;
    color: #FFFFFF;
  }
}

/* 头部区域 */
.header {
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  padding: 0 $spacing-lg $spacing-xl;
  border-radius: 0 0 $spacing-lg $spacing-lg;

  &__welcome {
    margin-bottom: $spacing-md;
  }

  &__greeting {
    font-size: $font-xl;
    font-weight: 600;
    color: #FFFFFF;
    display: block;
  }

  &__desc {
    font-size: $font-sm;
    color: $accent-color;
    display: block;
    margin-top: $spacing-xs;
  }
}

/* 识别入口按钮 */
.identify-actions {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-lg;
  margin: -$spacing-lg $spacing-lg 0;
  position: relative;
  z-index: 1;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: $spacing-lg $spacing-md;
    border-radius: $radius-lg;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
    gap: $spacing-xs;

    &--camera {
      background: linear-gradient(135deg, $primary-color, #3AAFA9);
    }

    &--album {
      background: linear-gradient(135deg, #3AAFA9, $secondary-color);
    }
  }

  &__icon {
    font-size: 64rpx;
  }

  &__name {
    font-size: $font-lg;
    font-weight: 600;
    color: #FFFFFF;
  }

  &__desc {
    font-size: $font-xs;
    color: $accent-color;
  }
}

/* 通用板块 */
.section {
  padding: $spacing-lg;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-md;
  }

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
  }

  &__more {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

/* 混淆药材对比 */
.compare-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.compare-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: $card-bg;
  border-radius: $radius-md;
  padding: $spacing-md $spacing-lg;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);

  &__left, &__right {
    flex: 1;
  }

  &__name {
    font-size: $font-md;
    font-weight: 500;
    color: $text-color;
  }

  &__vs {
    font-size: $font-sm;
    color: $danger-color;
    font-weight: 600;
    padding: 0 $spacing-md;
  }
}

/* 最近识别 */
.recent-scroll {
  white-space: nowrap;
}

.recent-item {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: 160rpx;
  margin-right: $spacing-md;
  flex-shrink: 0;

  &__img {
    width: 160rpx;
    height: 160rpx;
    border-radius: $radius-md;
    background-color: $border-color;
  }

  &__name {
    font-size: $font-sm;
    color: $text-color;
    margin-top: $spacing-xs;
  }
}

/* 空状态 */
.empty-tip {
  padding: $spacing-xl 0;
  text-align: center;

  &__text {
    font-size: $font-sm;
    color: $text-secondary;
  }
}
</style>
