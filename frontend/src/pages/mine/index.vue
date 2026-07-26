<template>
  <view class="page-mine">
    <!-- 用户区 -->
    <view class="user-block" v-if="userStore.isLogin">
      <view class="user-block__avatar-wrap">
        <image :src="userStore.avatar || '/static/images/placeholder.png'" mode="aspectFill" class="user-block__avatar" />
      </view>
      <view class="user-block__info">
        <text class="user-block__name">{{ userStore.nickname }}</text>
        <text class="user-block__id">No.{{ String(userStore.userInfo.id || 0).padStart(4, '0') }}</text>
      </view>
      <view class="user-block__edit" @click="goProfile">
        <text class="user-block__edit-text">编辑</text>
      </view>
    </view>


    <!-- 学习足迹 -->
    <view class="stats-card">
      <view class="stats-card__item" @click="goRecords">
        <text class="stats-card__num">{{ stats.records }}</text>
        <text class="stats-card__label">识别记录</text>
      </view>
      <view class="stats-card__divider"></view>
      <view class="stats-card__item" @click="goFavorites">
        <text class="stats-card__num">{{ stats.favorites }}</text>
        <text class="stats-card__label">我的收藏</text>
      </view>
    </view>

    <!-- 功能列表 -->
    <view class="menu">
      <view class="menu__head">
        <text class="menu__head-text">我的</text>
      </view>
      <view class="menu__item" @click="goRecords">
        <text class="menu__num">01</text>
        <text class="menu__name">识别记录</text>
        <text class="menu__arrow">→</text>
      </view>
      <view class="menu__item" @click="goFavorites">
        <text class="menu__num">02</text>
        <text class="menu__name">我的收藏</text>
        <text class="menu__arrow">→</text>
      </view>
      <view class="menu__item" @click="goFeedback">
        <text class="menu__num">03</text>
        <text class="menu__name">意见反馈</text>
        <text class="menu__arrow">→</text>
      </view>
      <view class="menu__item" @click="goAbout">
        <text class="menu__num">04</text>
        <text class="menu__name">关于本草</text>
        <text class="menu__arrow">→</text>
      </view>
      <view class="menu__item" @click="onClearCache">
        <text class="menu__num">05</text>
        <text class="menu__name">清除缓存</text>
        <text class="menu__arrow">→</text>
      </view>
    </view>

    <!-- 退出 -->
    <view class="logout" v-if="userStore.isLogin" @click="onLogout">
      <text class="logout__text">退出登录</text>
    </view>

    <!-- 尾签 -->
    <view class="sign">
      <view class="sign__line"></view>
      <text class="sign__text">本草 · v1.0.0</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 我 · 墨韵版
 */
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { getRecords, getFavorites } from '@/api/user'

const userStore = useUserStore()

const stats = ref({
  records: 0,
  favorites: 0,
})

onShow(() => {
  userStore.checkLogin()
  if (userStore.isLogin) {
    loadStats()
  }
})

/**
 * 加载学习足迹统计
 */
async function loadStats() {
  try {
    const [recordsData, favoritesData] = await Promise.all([
      getRecords({ page: 1, pageSize: 1 }),
      getFavorites({ page: 1, pageSize: 1 })
    ])
    stats.value.records = recordsData.total || 0
    stats.value.favorites = favoritesData.total || 0
  } catch (err) {
    // 静默处理
  }
}

function onLogout() {
  uni.showModal({
    title: '提示',
    content: '确定退出登录？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.showToast({ title: '已退出', icon: 'none' })
        setTimeout(() => {
          uni.reLaunch({ url: '/pages/login/index' })
        }, 300)
      }
    }
  })
}

function onClearCache() {
  uni.showModal({
    title: '提示',
    content: '确定清除所有缓存数据？',
    success: (res) => {
      if (res.confirm) {
        uni.showToast({ title: '缓存已清除', icon: 'none' })
      }
    }
  })
}

function goProfile() { uni.navigateTo({ url: '/pages/mine/profile' }) }
function goRecords() { uni.navigateTo({ url: '/pages/mine/records' }) }
function goFavorites() { uni.navigateTo({ url: '/pages/learn/favorites' }) }
function goFeedback() { uni.navigateTo({ url: '/pages/feedback/index' }) }
function goAbout() { uni.showToast({ title: '本草 v1.0.0', icon: 'none' }) }
</script>

<style lang="scss" scoped>
.page-mine {
  min-height: 100vh;
  background-color: $paper;
  padding: 0 $space-lg $space-3xl;
}

/* ===== 用户区 ===== */
.user-block {
  display: flex;
  align-items: center;
  padding: $space-2xl 0 $space-xl;
  gap: $space-md;

  &__avatar-wrap {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    overflow: hidden;
    background-color: $paper-deep;
    border: 1rpx solid $line;
    flex-shrink: 0;

    &--placeholder {
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: $ink;
    }
  }

  &__avatar {
    width: 100%;
    height: 100%;
  }

  &__avatar-char {
    font-family: $font-serif;
    font-size: 56rpx;
    color: #FFFFFF;
    font-weight: $weight-medium;
  }

  &__info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: $space-xxs;
  }

  &__name {
    font-size: $font-xl;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__id {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 2rpx;
  }

  &__edit {
    padding: $space-xs $space-md;
    border: 1rpx solid $line-strong;
    border-radius: $radius-sm;
  }

  &__edit-text {
    font-size: $font-sm;
    color: $ink-soft;
    letter-spacing: 1rpx;
  }

  &__login {
    padding: $space-xs $space-md;
    background-color: $ink;
    border-radius: $radius-sm;
  }

  &__login-text {
    font-size: $font-sm;
    color: #FFFFFF;
    letter-spacing: 2rpx;
    font-weight: $weight-medium;
  }
}

/* ===== 菜单 ===== */
.menu {
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  overflow: hidden;

  &__head {
    padding: $space-md $space-lg;
    border-bottom: 1rpx solid $line-soft;
    background-color: $paper-warm;
  }

  &__head-text {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 4rpx;
  }

  &__item {
    display: flex;
    align-items: center;
    padding: $space-md $space-lg;
    gap: $space-md;
    border-bottom: 1rpx solid $line-soft;

    &:last-child {
      border-bottom: none;
    }

    &:active {
      background-color: $paper-warm;
    }
  }

  &__num {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $gold;
    width: 40rpx;
    font-weight: $weight-medium;
    letter-spacing: 1rpx;
  }

  &__name {
    flex: 1;
    font-size: $font-md;
    color: $ink;
    letter-spacing: 1rpx;
  }

  &__extra {
    font-size: $font-sm;
    color: $ink-light;
  }

  &__arrow {
    font-size: $font-sm;
    color: $ink-faint;
  }
}

/* ===== 退出 ===== */
.logout {
  margin-top: $space-xl;
  padding: $space-md 0;
  text-align: center;
  border: 1rpx solid $cinnabar;
  border-radius: $radius-sm;

  &__text {
    font-size: $font-md;
    color: $cinnabar;
    font-weight: $weight-medium;
    letter-spacing: 2rpx;
  }
}

/* ===== 尾签 ===== */
.sign {
  margin-top: $space-3xl;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-sm;

  &__line {
    width: 32rpx;
    height: 1rpx;
    background-color: $line-strong;
  }

  &__text {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $ink-faint;
    letter-spacing: 4rpx;
  }
}

.stats-card {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  padding: $space-lg 0;
  margin-bottom: $space-lg;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $space-xs;
  }

  &__divider {
    width: 1rpx;
    height: 60rpx;
    background-color: $line-soft;
  }

  &__num {
    font-family: $font-serif;
    font-size: $font-xl;
    color: $ink;
    font-weight: $weight-semibold;
  }

  &__label {
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 2rpx;
  }
}
</style>
