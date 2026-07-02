<template>
  <view class="page-mine">
    <!-- 用户信息区 -->
    <view class="user-section" v-if="userStore.isLogin">
      <image :src="userStore.avatar || '/static/images/placeholder.png'" mode="aspectFill" class="user-section__avatar" />
      <view class="user-section__info">
        <text class="user-section__name">{{ userStore.nickname }}</text>
        <text class="user-section__id">ID: {{ userStore.userInfo.id || '-' }}</text>
      </view>
      <view class="user-section__edit" @click="goProfile">
        <text>编辑</text>
      </view>
    </view>
    <view class="user-section user-section--nologin" v-else>
      <view class="user-section__avatar-placeholder">&#x1F464;</view>
      <view class="user-section__info">
        <text class="user-section__name">未登录</text>
      </view>
      <view class="login-btn" @click="onLogin">
        <text class="login-btn__text">微信一键登录</text>
      </view>
    </view>

    <!-- 功能列表 -->
    <view class="menu-list">
      <view class="menu-item" @click="goRecords">
        <text class="menu-item__icon">&#x1F4CB;</text>
        <text class="menu-item__name">识别记录</text>
        <text class="menu-item__arrow">&#x276F;</text>
      </view>
      <view class="menu-item" @click="goFavorites">
        <text class="menu-item__icon">&#x2B50;</text>
        <text class="menu-item__name">我的收藏</text>
        <text class="menu-item__arrow">&#x276F;</text>
      </view>
      <view class="menu-item" @click="goCacheManage">
        <text class="menu-item__icon">&#x1F4BE;</text>
        <text class="menu-item__name">离线缓存管理</text>
        <text class="menu-item__extra">{{ cacheCount }} 条</text>
        <text class="menu-item__arrow">&#x276F;</text>
      </view>
      <view class="menu-item" @click="onClearCache">
        <text class="menu-item__icon">&#x1F5D1;</text>
        <text class="menu-item__name">清除缓存</text>
        <text class="menu-item__arrow">&#x276F;</text>
      </view>
      <view class="menu-item" @click="goFeedback">
        <text class="menu-item__icon">&#x1F4DD;</text>
        <text class="menu-item__name">意见反馈</text>
        <text class="menu-item__arrow">&#x276F;</text>
      </view>
      <view class="menu-item" @click="goAbout">
        <text class="menu-item__icon">&#x2139;</text>
        <text class="menu-item__name">关于</text>
        <text class="menu-item__arrow">&#x276F;</text>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-btn" v-if="userStore.isLogin" @click="onLogout">
      <text class="logout-btn__text">退出登录</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 个人中心
 * 用户信息、功能列表、退出登录
 */
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { getCacheSize, clearAllCache } from '@/utils/cache'

const userStore = useUserStore()
const cacheCount = ref(0)

onShow(() => {
  cacheCount.value = getCacheSize()
})

/**
 * 微信登录
 */
async function onLogin() {
  try {
    await userStore.login()
    uni.showToast({ title: '登录成功', icon: 'none' })
  } catch (err) {
    uni.showToast({ title: '登录失败', icon: 'none' })
  }
}

/**
 * 退出登录
 */
function onLogout() {
  uni.showModal({
    title: '提示',
    content: '确定退出登录？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.showToast({ title: '已退出', icon: 'none' })
      }
    }
  })
}

/**
 * 清除缓存
 */
function onClearCache() {
  uni.showModal({
    title: '提示',
    content: '确定清除所有缓存数据？',
    success: (res) => {
      if (res.confirm) {
        clearAllCache()
        cacheCount.value = 0
        uni.showToast({ title: '缓存已清除', icon: 'none' })
      }
    }
  })
}

function goProfile() {
  uni.navigateTo({ url: '/pages/mine/profile' })
}

function goRecords() {
  uni.navigateTo({ url: '/pages/mine/records' })
}

function goFavorites() {
  uni.navigateTo({ url: '/pages/learn/favorites' })
}

function goCacheManage() {
  uni.showToast({ title: '缓存管理', icon: 'none' })
}

function goFeedback() {
  uni.navigateTo({ url: '/pages/feedback/index' })
}

function goAbout() {
  uni.showToast({ title: 'AI中药识别 v1.0.0', icon: 'none' })
}
</script>

<style lang="scss" scoped>
.page-mine {
  min-height: 100vh;
  background-color: $bg-color;
}

/* 用户信息区 */
.user-section {
  display: flex;
  align-items: center;
  padding: $spacing-xl $spacing-lg;
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  gap: $spacing-md;

  &--nologin {
    padding: $spacing-xl $spacing-lg;
  }

  &__avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background-color: $accent-color;
    flex-shrink: 0;
  }

  &__avatar-placeholder {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background-color: $accent-color;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 64rpx;
    flex-shrink: 0;
  }

  &__info {
    flex: 1;
  }

  &__name {
    font-size: $font-xl;
    font-weight: 600;
    color: #FFFFFF;
    display: block;
  }

  &__id {
    font-size: $font-sm;
    color: $accent-color;
    display: block;
    margin-top: $spacing-xs;
  }

  &__edit {
    padding: $spacing-sm $spacing-md;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: $radius-lg;
    color: #FFFFFF;
    font-size: $font-sm;
  }
}

.login-btn {
  padding: $spacing-sm $spacing-lg;
  background-color: #FFFFFF;
  border-radius: $radius-lg;

  &__text {
    font-size: $font-md;
    color: $primary-color;
    font-weight: 600;
  }
}

/* 功能列表 */
.menu-list {
  margin: $spacing-lg $spacing-lg 0;
  background-color: $card-bg;
  border-radius: $radius-lg;
  overflow: hidden;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: $spacing-lg;
  border-bottom: 1rpx solid $border-color;
  gap: $spacing-md;

  &:last-child {
    border-bottom: none;
  }

  &__icon {
    font-size: 40rpx;
  }

  &__name {
    flex: 1;
    font-size: $font-md;
    color: $text-color;
  }

  &__extra {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__arrow {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

/* 退出登录 */
.logout-btn {
  margin: $spacing-xl $spacing-lg;
  padding: $spacing-lg 0;
  background-color: $card-bg;
  border-radius: $radius-lg;
  text-align: center;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);

  &__text {
    font-size: $font-lg;
    color: $danger-color;
    font-weight: 500;
  }
}
</style>
