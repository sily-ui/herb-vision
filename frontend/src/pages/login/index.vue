<template>
  <view class="page-login">
    <!-- 宣纸纹理背景 -->
    <view class="page-login__texture"></view>

    <!-- 顶部装饰：药性纲目 -->
    <view class="top-ornament">
      <text class="top-ornament__text">药性 · 纲目 · 辨真</text>
    </view>

    <!-- 主视觉 -->
    <view class="hero">
      <view class="logo">
        <view class="logo__leaf">
          <view class="logo__vein"></view>
        </view>
        <view class="logo__stem"></view>
        <view class="logo__root"></view>
      </view>
      <view class="brand">
        <text class="brand__title">本草</text>
        <text class="brand__subtitle">识鉴</text>
      </view>
      <text class="hero__motto">取草木之形，辨真伪之道</text>
    </view>

    <!-- 功能入口 -->
    <view class="feature-ring">
      <view class="feature-ring__item">
        <view class="feature-ring__dot feature-ring__dot--photo"></view>
        <text class="feature-ring__label">识药</text>
      </view>
      <view class="feature-ring__line"></view>
      <view class="feature-ring__item">
        <view class="feature-ring__dot feature-ring__dot--book"></view>
        <text class="feature-ring__label">辨伪</text>
      </view>
      <view class="feature-ring__line"></view>
      <view class="feature-ring__item">
        <view class="feature-ring__dot feature-ring__dot--foot"></view>
        <text class="feature-ring__label">习录</text>
      </view>
    </view>

    <!-- 底部操作 -->
    <view class="action">
      <button
        class="login-btn"
        :loading="loading"
        :disabled="loading"
        @click="onWxLogin"
      >
        <view class="login-btn__inner">
          <text class="login-btn__icon">&#x263A;</text>
          <text class="login-btn__text">微信一键登录</text>
        </view>
      </button>
      <text class="action__hint">登录后同步收藏与学习足迹</text>
    </view>

    <!-- 底款 -->
    <view class="seal-mark">
      <view class="seal-mark__border">
        <text class="seal-mark__text">本草 v1.0</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 本草识鉴 · 登录页
 * 东方药学美学：草木为形，墨色为底，朱砂点睛
 */
import { ref } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const loading = ref(false)

async function onWxLogin() {
  if (loading.value) return
  loading.value = true
  try {
    await userStore.login()
    uni.showToast({ title: '登录成功', icon: 'none' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 400)
  } catch (err) {
    uni.showToast({ title: '登录失败，请重试', icon: 'none' })
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.page-login {
  position: relative;
  min-height: 100vh;
  background-color: $paper;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 60rpx 80rpx;
  box-sizing: border-box;
  overflow: hidden;

  &__texture {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.35;
    background-image:
      radial-gradient(circle at 18% 22%, rgba(168, 54, 47, 0.04) 0%, transparent 28%),
      radial-gradient(circle at 82% 68%, rgba(61, 90, 74, 0.05) 0%, transparent 32%),
      radial-gradient(circle at 64% 14%, rgba(168, 138, 92, 0.04) 0%, transparent 20%);
  }
}

.top-ornament {
  align-self: flex-end;
  padding: 8rpx 20rpx;
  border-top: 1rpx solid $line-strong;
  border-bottom: 1rpx solid $line-strong;

  &__text {
    font-family: $font-serif;
    font-size: 20rpx;
    color: $ink-light;
    letter-spacing: 8rpx;
  }
}

.hero {
  margin-top: 120rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32rpx;
}

.logo {
  position: relative;
  width: 160rpx;
  height: 200rpx;

  &__leaf {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 120rpx;
    height: 120rpx;
    background: linear-gradient(135deg, $bamboo 0%, darken($bamboo, 12%) 100%);
    border-radius: 0 80% 0 80%;
    box-shadow: 0 12rpx 32rpx rgba(61, 90, 74, 0.22);
  }

  &__vein {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 2rpx;
    height: 80rpx;
    background: rgba(255, 255, 255, 0.35);
    transform: translate(-50%, -50%) rotate(45deg);

    &::before,
    &::after {
      content: '';
      position: absolute;
      width: 2rpx;
      height: 40rpx;
      background: rgba(255, 255, 255, 0.28);
      left: 50%;
      transform-origin: top center;
    }

    &::before {
      top: 20rpx;
      transform: translateX(-50%) rotate(-35deg);
    }

    &::after {
      top: 28rpx;
      transform: translateX(-50%) rotate(35deg);
    }
  }

  &__stem {
    position: absolute;
    top: 108rpx;
    left: 50%;
    transform: translateX(-50%);
    width: 6rpx;
    height: 56rpx;
    background: linear-gradient(to bottom, $bamboo, darken($bamboo, 15%));
    border-radius: 4rpx;
  }

  &__root {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 64rpx;
    height: 40rpx;
    border: 4rpx solid $cinnabar;
    border-top: none;
    border-radius: 0 0 32rpx 32rpx;

    &::before {
      content: '';
      position: absolute;
      top: -8rpx;
      left: 50%;
      transform: translateX(-50%);
      width: 8rpx;
      height: 16rpx;
      background: $cinnabar;
      border-radius: 0 0 4rpx 4rpx;
    }
  }
}

.brand {
  display: flex;
  align-items: baseline;
  gap: 12rpx;

  &__title {
    font-family: $font-serif;
    font-size: 76rpx;
    font-weight: $weight-bold;
    color: $ink;
    letter-spacing: 10rpx;
  }

  &__subtitle {
    font-family: $font-serif;
    font-size: 44rpx;
    font-weight: $weight-medium;
    color: $cinnabar;
    letter-spacing: 6rpx;
    padding-bottom: 8rpx;
    border-bottom: 2rpx solid $cinnabar;
  }
}

.hero__motto {
  font-size: $font-md;
  color: $ink-light;
  letter-spacing: 4rpx;
  margin-top: 8rpx;
}

.feature-ring {
  margin-top: 100rpx;
  display: flex;
  align-items: center;
  gap: 24rpx;

  &__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14rpx;
  }

  &__dot {
    width: 72rpx;
    height: 72rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.06);

    &--photo {
      background: linear-gradient(135deg, #E8F0E9 0%, #D4E4D6 100%);
    }

    &--book {
      background: linear-gradient(135deg, #F5EDE8 0%, #EADFD6 100%);
    }

    &--foot {
      background: linear-gradient(135deg, #F3EDE5 0%, #E5DCD0 100%);
    }

    &::before {
      font-family: $font-serif;
      font-size: 30rpx;
      color: $ink-soft;
    }

    &--photo::before { content: '识'; }
    &--book::before { content: '辨'; }
    &--foot::before { content: '习'; }
  }

  &__label {
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 2rpx;
  }

  &__line {
    width: 48rpx;
    height: 1rpx;
    background-color: $line-strong;
  }
}

.action {
  margin-top: auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
  padding-bottom: 40rpx;
}

.login-btn {
  width: 100%;
  height: 104rpx;
  padding: 0;
  background: transparent;
  border: none;

  &::after {
    border: none;
  }

  &[disabled] {
    opacity: 0.75;
  }

  &__inner {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16rpx;
    background: linear-gradient(135deg, $ink 0%, #2D2D2D 100%);
    border-radius: 52rpx;
    box-shadow: 0 16rpx 40rpx rgba(26, 26, 26, 0.18);
  }

  &__icon {
    font-size: $font-xl;
    color: #FFFFFF;
  }

  &__text {
    font-size: $font-lg;
    color: #FFFFFF;
    font-weight: $weight-medium;
    letter-spacing: 4rpx;
  }
}

.action__hint {
  font-size: $font-sm;
  color: $ink-light;
  letter-spacing: 2rpx;
}

.seal-mark {
  margin-top: 48rpx;

  &__border {
    padding: 8rpx 20rpx;
    border: 1rpx solid $line-strong;
  }

  &__text {
    font-family: $font-serif;
    font-size: 20rpx;
    color: $ink-faint;
    letter-spacing: 4rpx;
  }
}
</style>
