<template>
  <view class="page-identify">
    <!-- 空状态：双入口 -->
    <view class="choose" v-if="!imageList.length">
      <view class="choose__meta">
        <text class="choose__meta-line"></text>
        <text class="choose__meta-text">AI IDENTIFICATION · 智能鉴别</text>
      </view>
      <text class="choose__title">辨物识药</text>
      <text class="choose__desc">拍摄或选取药材图像，AI 即刻比对辨析</text>

      <view class="choose__cards">
        <view class="choose-card" @click="onTakePhoto">
          <view class="choose-card__seal">
            <text class="choose-card__seal-char">摄</text>
          </view>
          <text class="choose-card__name">即时拍摄</text>
          <text class="choose-card__desc">调用相机拍摄药材</text>
        </view>
        <view class="choose-card choose-card--alt" @click="onFromAlbum">
          <view class="choose-card__seal choose-card__seal--alt">
            <text class="choose-card__seal-char">选</text>
          </view>
          <text class="choose-card__name">相册选取</text>
          <text class="choose-card__desc">从相册选择图片</text>
        </view>
      </view>

      <view class="choose__tip">
        <text class="choose__tip-line"></text>
        <text class="choose__tip-text">建议拍摄清晰药材外观</text>
        <text class="choose__tip-line"></text>
      </view>
    </view>

    <!-- 预览状态 -->
    <view class="preview" v-else>
      <view class="preview__meta">
        <text class="preview__meta-line"></text>
        <text class="preview__meta-text">已选 {{ imageList.length }} 张</text>
      </view>

      <view class="preview-list">
        <view class="preview-item" v-for="(item, index) in imageList" :key="index">
          <image :src="item" mode="aspectFill" class="preview-item__img" />
          <view class="preview-item__delete" @click="onDeleteImage(index)">
            <text class="preview-item__delete-icon">✕</text>
          </view>
          <view class="preview-item__idx" v-if="index === 0">
            <text class="preview-item__idx-text">主图</text>
          </view>
        </view>
        <view class="preview-item preview-item--add" v-if="imageList.length < 9" @click="onAddMore">
          <text class="preview-item__add-icon">+</text>
          <text class="preview-item__add-text">追加</text>
        </view>
      </view>

      <!-- 进度条 -->
      <view class="progress" v-if="uploading">
        <view class="progress__track">
          <view class="progress__fill" :style="{ width: uploadProgress + '%' }"></view>
        </view>
        <text class="progress__text">鉴別中 {{ uploadProgress }}%</text>
      </view>

      <!-- 提交按钮 -->
      <view class="submit" :class="{ 'submit--disabled': uploading }" @click="onIdentify">
        <text class="submit__text">{{ uploading ? '鉴别中…' : '开始鉴别' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 智能识别 · 墨韵版
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { identifyImage } from '@/api/identify'
import { compressImage } from '@/utils/common'

const imageList = ref([])
const uploading = ref(false)
const uploadProgress = ref(0)

onLoad((query) => {
  if (query.source === 'camera') onTakePhoto()
  else if (query.source === 'album') onFromAlbum()
})

function onTakePhoto() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['camera'],
    success: (res) => imageList.value.push(...res.tempFilePaths)
  })
}

function onFromAlbum() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['album'],
    success: (res) => imageList.value.push(...res.tempFilePaths)
  })
}

function onAddMore() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => imageList.value.push(...res.tempFilePaths)
  })
}

function onDeleteImage(index) {
  imageList.value.splice(index, 1)
}

async function onIdentify() {
  if (uploading.value || !imageList.value.length) return

  uploading.value = true
  uploadProgress.value = 0

  try {
    const compressedPath = await compressImage(imageList.value[0])

    const progressTimer = setInterval(() => {
      if (uploadProgress.value < 90) uploadProgress.value += 10
    }, 300)

    const result = await identifyImage(compressedPath)

    clearInterval(progressTimer)
    uploadProgress.value = 100

    setTimeout(() => {
      uploading.value = false
      uploadProgress.value = 0
      uni.navigateTo({
        url: `/pages/identify/result?data=${encodeURIComponent(JSON.stringify(result))}`
      })
    }, 500)
  } catch (err) {
    uploading.value = false
    uploadProgress.value = 0
    uni.showToast({ title: '鉴别失败，请重试', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.page-identify {
  min-height: 100vh;
  background-color: $paper;
  padding: 0 $space-lg $space-3xl;
}

/* ===== 空状态 ===== */
.choose {
  padding-top: $space-2xl;

  &__meta {
    display: flex;
    align-items: center;
    gap: $space-sm;
    margin-bottom: $space-md;
  }

  &__meta-line {
    width: 32rpx;
    height: 1rpx;
    background-color: $ink-light;
  }

  &__meta-text {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 3rpx;
    font-weight: $weight-medium;
  }

  &__title {
    font-size: 80rpx;
    font-weight: $weight-bold;
    color: $ink;
    letter-spacing: 8rpx;
    display: block;
  }

  &__desc {
    font-size: $font-sm;
    color: $ink-light;
    margin-top: $space-sm;
    display: block;
    letter-spacing: 1rpx;
  }

  &__cards {
    display: flex;
    gap: $space-sm;
    margin-top: $space-2xl;
  }

  &__tip {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: $space-md;
    margin-top: $space-2xl;
  }

  &__tip-line {
    width: 40rpx;
    height: 1rpx;
    background-color: $line-strong;
  }

  &__tip-text {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 2rpx;
  }
}

.choose-card {
  flex: 1;
  padding: $space-xl $space-md;
  background-color: $card;
  border: 1rpx solid $line;
  border-radius: $radius-md;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-sm;

  &--alt {
    background-color: transparent;
    border-style: dashed;
  }

  &__seal {
    width: 96rpx;
    height: 96rpx;
    background-color: $cinnabar;
    border-radius: $radius-sm;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: $space-xs;
    box-shadow: 0 4rpx 12rpx rgba(168, 54, 47, 0.2);

    &--alt {
      background-color: $ink;
      box-shadow: 0 4rpx 12rpx rgba(26, 26, 26, 0.2);
    }
  }

  &__seal-char {
    font-family: $font-serif;
    font-size: 48rpx;
    color: #FFFFFF;
    font-weight: $weight-bold;
    line-height: 1;
  }

  &__name {
    font-size: $font-md;
    font-weight: $weight-semibold;
    color: $ink;
    letter-spacing: 2rpx;
  }

  &__desc {
    font-size: $font-xs;
    color: $ink-light;
  }
}

/* ===== 预览状态 ===== */
.preview {
  padding-top: $space-xl;

  &__meta {
    display: flex;
    align-items: center;
    gap: $space-sm;
    margin-bottom: $space-md;
  }

  &__meta-line {
    width: 32rpx;
    height: 1rpx;
    background-color: $ink-light;
  }

  &__meta-text {
    font-family: $font-serif;
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 2rpx;
  }
}

.preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: $space-sm;
}

.preview-item {
  position: relative;
  width: 220rpx;
  height: 220rpx;
  border: 1rpx solid $line;
  border-radius: $radius-sm;
  overflow: hidden;
  background-color: $paper-deep;

  &--add {
    border-style: dashed;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: $space-xs;
    background-color: transparent;
  }

  &__img {
    width: 100%;
    height: 100%;
  }

  &__delete {
    position: absolute;
    top: 0;
    right: 0;
    width: 44rpx;
    height: 44rpx;
    background-color: rgba(26, 26, 26, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0 0 0 $radius-xs;
  }

  &__delete-icon {
    color: #FFFFFF;
    font-size: $font-xs;
  }

  &__idx {
    position: absolute;
    bottom: 0;
    left: 0;
    padding: 2rpx 12rpx;
    background-color: $cinnabar;
    border-radius: 0 $radius-xs 0 0;
  }

  &__idx-text {
    font-size: $font-xs;
    color: #FFFFFF;
    letter-spacing: 1rpx;
  }

  &__add-icon {
    font-size: 48rpx;
    color: $ink-light;
  }

  &__add-text {
    font-size: $font-xs;
    color: $ink-light;
    letter-spacing: 2rpx;
  }
}

/* ===== 进度条 ===== */
.progress {
  margin-top: $space-xl;

  &__track {
    height: 4rpx;
    background-color: $line;
    overflow: hidden;
  }

  &__fill {
    height: 100%;
    background-color: $cinnabar;
    transition: width 0.3s;
  }

  &__text {
    font-family: $font-serif;
    font-size: $font-sm;
    color: $ink-soft;
    margin-top: $space-sm;
    display: block;
    text-align: center;
    letter-spacing: 2rpx;
  }
}

/* ===== 提交按钮 ===== */
.submit {
  margin-top: $space-2xl;
  padding: $space-lg 0;
  background-color: $ink;
  text-align: center;
  border-radius: $radius-sm;

  &--disabled {
    opacity: 0.5;
  }

  &__text {
    font-size: $font-md;
    color: #FFFFFF;
    font-weight: $weight-medium;
    letter-spacing: 4rpx;
  }
}
</style>
