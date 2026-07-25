<template>
  <view class="page-index">
    <!-- 顶部品牌区：竖排辅助文字 + 大字标题 -->
    <view class="hero">
      <view class="hero__meta">
        <text class="hero__meta-line"></text>
        <text class="hero__meta-text">BĚN CǍO · 本草</text>
      </view>
      <view class="hero__title-wrap">
        <text class="hero__title">识草木</text>
        <text class="hero__title hero__title--accent">知本草</text>
      </view>
      <text class="hero__sub">AI 智能中药材鉴别 · {{ todayStr }}</text>
    </view>

    <!-- 识别入口：拍摄 / 相册 -->
    <view class="identify-row">
      <view class="identify-card identify-card--camera" @click="onTakePhoto">
        <text class="identify-card__icon">&#x1F4F7;</text>
        <view class="identify-card__body">
          <text class="identify-card__name">即时拍摄</text>
          <text class="identify-card__desc">打开相机拍摄药材</text>
        </view>
      </view>
      <view class="identify-card identify-card--album" @click="onFromAlbum">
        <text class="identify-card__icon">&#x1F4BE;</text>
        <view class="identify-card__body">
          <text class="identify-card__name">相册选取</text>
          <text class="identify-card__desc">从相册选择图片</text>
        </view>
      </view>
    </view>

    <!-- 分隔：今日推荐 -->
    <view class="section">
      <view class="section__head">
        <view class="section__title-wrap">
          <text class="section__bar"></text>
          <text class="section__title">易混药材</text>
        </view>
        <text class="section__more" @click="goCompare">查看全部 →</text>
      </view>

      <view class="compare-table">
        <view
          class="compare-row"
          v-for="(item, index) in comparePairs"
          :key="index"
          @click="goCompareDetail(item)"
        >
          <text class="compare-row__idx">{{ String(index + 1).padStart(2, '0') }}</text>
          <text class="compare-row__name">{{ item.name1 }}</text>
          <view class="compare-row__vs">
            <text class="compare-row__vs-text">易混</text>
          </view>
          <text class="compare-row__name compare-row__name--alt">{{ item.name2 }}</text>
          <text class="compare-row__arrow">→</text>
        </view>
      </view>
    </view>

    <!-- 留白尾韵 -->
    <view class="epilogue">
      <view class="epilogue__line"></view>
      <text class="epilogue__text">— 凡药之用，必明其真 —</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 首页 · 墨韵版
 * 极简东方美学：朱砂印章 + 竖排辅助 + 衬线数字
 */
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { identifyImage } from '@/api/identify'
import { compressImage } from '@/utils/common'

const userStore = useUserStore()
const uploading = ref(false)
const comparePairs = ref([
  { name1: '赤芍', name2: '白芍', id1: 1, id2: 2 },
  { name1: '黄芪', name2: '红芪', id1: 3, id2: 4 },
  { name1: '半夏', name2: '水半夏', id1: 5, id2: 6 },
  { name1: '柴胡', name2: '银柴胡', id1: 7, id2: 8 },
  { name1: '人参', name2: '党参', id1: 9, id2: 10 }
])

const todayStr = computed(() => {
  const d = new Date()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}.${m}.${day}`
})

onShow(() => {
  // 静默登录：未登录时自动获取微信 token
  userStore.checkLogin()
  if (!userStore.isLogin) {
    userStore.login().catch(() => {})
  }
})

function onTakePhoto() {
  chooseAndIdentify('camera')
}

function onFromAlbum() {
  chooseAndIdentify('album')
}

function chooseAndIdentify(sourceType) {
  if (uploading.value) return
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: [sourceType],
    success: (res) => identifySingleImage(res.tempFilePaths[0]),
    fail: (err) => {
      if (err.errMsg && !err.errMsg.includes('cancel')) {
        uni.showToast({ title: '选择图片失败', icon: 'none' })
      }
    }
  })
}

async function identifySingleImage(imagePath) {
  if (uploading.value) return
  uploading.value = true
  uni.showLoading({ title: '鉴别中…', mask: true })
  try {
    const compressedPath = await compressImage(imagePath)
    const result = await identifyImage(compressedPath)
    uni.navigateTo({
      url: `/pages/identify/result?data=${encodeURIComponent(JSON.stringify(result))}`
    })
  } catch (err) {
    uni.showToast({ title: '鉴别失败，请重试', icon: 'none' })
  } finally {
    uploading.value = false
    uni.hideLoading()
  }
}

function goCompare() {
  uni.navigateTo({ url: '/pages/compare/index' })
}
function goCompareDetail(item) {
  uni.navigateTo({ url: `/pages/compare/index?id1=${item.id1}&id2=${item.id2}` })
}
</script>

<style lang="scss" scoped>
.page-index {
  min-height: 100vh;
  background-color: $paper;
  padding: 0 $space-lg $space-3xl;
}

/* ===== Hero 品牌区 ===== */
.hero {
  padding: $space-2xl 0 $space-xl;
  display: flex;
  flex-direction: column;
  gap: $space-md;

  &__meta {
    display: flex;
    align-items: center;
    gap: $space-sm;
  }

  &__meta-line {
    width: 48rpx;
    height: 1rpx;
    background-color: $ink-light;
  }

  &__meta-text {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 4rpx;
    text-transform: uppercase;
    font-weight: $weight-medium;
  }

  &__title-wrap {
    display: flex;
    align-items: baseline;
    gap: $space-md;
    margin-top: $space-xs;
  }

  &__title {
    font-size: 96rpx;
    font-weight: $weight-bold;
    color: $ink;
    letter-spacing: 8rpx;
    line-height: 1.1;

    &--accent {
      color: $cinnabar;
      font-weight: $weight-light;
    }
  }

  &__sub {
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 2rpx;
    margin-top: $space-xs;
  }
}

/* ===== 主识别入口（朱砂印章） ===== */
.primary-action {
  display: flex;
  align-items: center;
  background-color: $card;
  padding: $space-lg;
  margin-top: $space-lg;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  gap: $space-md;
  position: relative;
  transition: all 0.2s;

  &:active {
    background-color: $paper-warm;
  }

  &__seal {
    width: 96rpx;
    height: 96rpx;
    background-color: $cinnabar;
    border-radius: $radius-sm;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4rpx 12rpx rgba(168, 54, 47, 0.25);
  }

  &__seal-char {
    font-family: $font-serif;
    font-size: 56rpx;
    color: #FFFFFF;
    font-weight: $weight-bold;
    line-height: 1;
  }

  &__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: $space-xxs;
  }

  &__title {
    font-size: $font-lg;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__desc {
    font-size: $font-sm;
    color: $ink-light;
  }

  &__arrow {
    font-size: $font-lg;
    color: $ink-light;
  }
}

/* ===== 次级入口 ===== */
.identify-row {
  display: flex;
  gap: $space-md;
  margin-top: $space-lg;
}

.identify-card {
  flex: 1;
  padding: $space-xl $space-md;
  border-radius: $radius-md;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-sm;
  transition: all 0.2s;

  &:active {
    opacity: 0.85;
    transform: scale(0.98);
  }

  &--camera {
    background-color: $ink;
  }

  &--album {
    background-color: $card;
    border: 1rpx solid $line;
  }

  &__icon {
    font-size: 56rpx;
    line-height: 1;
  }

  &__body {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $space-xs;
  }

  &__name {
    font-size: $font-md;
    font-weight: $weight-semibold;
    letter-spacing: 2rpx;

    .identify-card--camera & {
      color: #FFFFFF;
    }

    .identify-card--album & {
      color: $ink;
    }
  }

  &__desc {
    font-size: $font-xs;

    .identify-card--camera & {
      color: rgba(255, 255, 255, 0.7);
    }

    .identify-card--album & {
      color: $ink-light;
    }
  }
}

/* ===== 通用 section ===== */
.section {
  margin-top: $space-2xl;

  &__head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $space-md;
  }

  &__title-wrap {
    display: flex;
    align-items: center;
    gap: $space-sm;
  }

  &__bar {
    width: 4rpx;
    height: 28rpx;
    background-color: $cinnabar;
  }

  &__title {
    font-size: $font-lg;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__more {
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 1rpx;
  }
}

/* ===== 易混药材表格 ===== */
.compare-table {
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  overflow: hidden;
}

.compare-row {
  display: flex;
  align-items: center;
  padding: $space-md $space-lg;
  gap: $space-sm;
  border-bottom: 1rpx solid $line-soft;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background-color: $paper-warm;
  }

  &__idx {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $gold;
    width: 40rpx;
    font-weight: $weight-medium;
  }

  &__name {
    font-size: $font-md;
    color: $ink;
    font-weight: $weight-medium;
    letter-spacing: 1rpx;

    &--alt {
      color: $ink-soft;
      font-weight: $weight-regular;
    }
  }

  &__vs {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  &__vs-text {
    font-size: $font-xs;
    color: $cinnabar;
    padding: 2rpx 12rpx;
    border: 1rpx solid $cinnabar;
    border-radius: $radius-xs;
    letter-spacing: 2rpx;
  }

  &__arrow {
    font-size: $font-sm;
    color: $ink-faint;
  }
}

/* ===== 尾韵 ===== */
.epilogue {
  margin-top: $space-3xl;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-md;

  &__line {
    width: 64rpx;
    height: 1rpx;
    background-color: $line-strong;
  }

  &__text {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $ink-light;
    letter-spacing: 4rpx;
  }
}
</style>
