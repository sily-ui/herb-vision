<template>
  <view class="page-identify">
    <!-- 拍照/相册选择 -->
    <view class="choose-actions" v-if="!imageList.length">
      <view class="choose-actions__item" @click="onTakePhoto">
        <text class="choose-actions__icon">&#x1F4F7;</text>
        <text class="choose-actions__name">拍照识别</text>
        <text class="choose-actions__desc">打开相机拍摄药材照片</text>
      </view>
      <view class="choose-actions__divider">
        <text class="choose-actions__or">或</text>
      </view>
      <view class="choose-actions__item" @click="onFromAlbum">
        <text class="choose-actions__icon">&#x1F5BC;</text>
        <text class="choose-actions__name">相册选择</text>
        <text class="choose-actions__desc">从手机相册选择图片</text>
      </view>
    </view>

    <!-- 图片预览区域 -->
    <view class="preview-area" v-if="imageList.length">
      <view class="preview-list">
        <view
          class="preview-item"
          v-for="(item, index) in imageList"
          :key="index"
        >
          <image :src="item" mode="aspectFill" class="preview-item__img" />
          <view class="preview-item__delete" @click="onDeleteImage(index)">
            <text>&#x2715;</text>
          </view>
        </view>
        <!-- 继续添加 -->
        <view class="preview-item preview-item--add" @click="onAddMore" v-if="imageList.length < 9">
          <text class="preview-item__add-icon">+</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-row">
        <view class="action-btn action-btn--secondary" @click="onTakePhoto">
          <text class="action-btn__icon">&#x1F4F7;</text>
          <text>拍照</text>
        </view>
        <view class="action-btn action-btn--secondary" @click="onFromAlbum">
          <text class="action-btn__icon">&#x1F5BC;</text>
          <text>相册</text>
        </view>
      </view>

      <!-- 上传进度条 -->
      <view class="progress-bar" v-if="uploading">
        <view class="progress-bar__track">
          <view class="progress-bar__fill" :style="{ width: uploadProgress + '%' }"></view>
        </view>
        <text class="progress-bar__text">上传中 {{ uploadProgress }}%</text>
      </view>

      <!-- 上传识别按钮 -->
      <view class="submit-btn" :class="{ 'submit-btn--disabled': uploading }" @click="onIdentify">
        <text class="submit-btn__text">{{ uploading ? '识别中...' : '开始识别' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 识别入口页
 * 拍照/相册选择图片，上传识别
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { identifyImage } from '@/api/identify'
import { compressImage } from '@/utils/common'

const imageList = ref([])
const uploading = ref(false)
const uploadProgress = ref(0)

onLoad((query) => {
  // 如果从首页直接进入，根据source自动触发
  if (query.source === 'camera') {
    onTakePhoto()
  } else if (query.source === 'album') {
    onFromAlbum()
  }
})

/**
 * 拍照
 */
function onTakePhoto() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['camera'],
    success: (res) => {
      imageList.value.push(...res.tempFilePaths)
    }
  })
}

/**
 * 从相册选择
 */
function onFromAlbum() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['album'],
    success: (res) => {
      imageList.value.push(...res.tempFilePaths)
    }
  })
}

/**
 * 继续添加图片
 */
function onAddMore() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      imageList.value.push(...res.tempFilePaths)
    }
  })
}

/**
 * 删除图片
 */
function onDeleteImage(index) {
  imageList.value.splice(index, 1)
}

/**
 * 开始识别
 */
async function onIdentify() {
  if (uploading.value || !imageList.value.length) return

  uploading.value = true
  uploadProgress.value = 0

  try {
    // 压缩第一张图片
    const compressedPath = await compressImage(imageList.value[0])

    // 模拟进度
    const progressTimer = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 300)

    // 上传识别
    const result = await identifyImage(compressedPath)

    clearInterval(progressTimer)
    uploadProgress.value = 100

    // 跳转结果页
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
    uni.showToast({
      title: '识别失败，请重试',
      icon: 'none'
    })
  }
}
</script>

<style lang="scss" scoped>
.page-identify {
  min-height: 100vh;
  background-color: $bg-color;
  padding: $spacing-lg;
}

/* 选择操作 */
.choose-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 120rpx;
  gap: $spacing-lg;

  &__item {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: $spacing-xl 0;
    background-color: $card-bg;
    border-radius: $radius-lg;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
    gap: $spacing-sm;
  }

  &__icon {
    font-size: 80rpx;
  }

  &__name {
    font-size: $font-xl;
    font-weight: 600;
    color: $text-color;
  }

  &__desc {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__divider {
    display: flex;
    align-items: center;
    padding: $spacing-sm 0;
  }

  &__or {
    font-size: $font-sm;
    color: $text-secondary;
  }
}

/* 预览区域 */
.preview-area {
  padding-top: $spacing-md;
}

.preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;
}

.preview-item {
  position: relative;
  width: 200rpx;
  height: 200rpx;
  border-radius: $radius-md;
  overflow: hidden;

  &--add {
    border: 2rpx dashed $border-color;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: $bg-color;
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
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-size: $font-xs;
    border-radius: 0 0 0 $radius-sm;
  }

  &__add-icon {
    font-size: 48rpx;
    color: $text-secondary;
  }
}

.action-row {
  display: flex;
  gap: $spacing-md;
  margin-top: $spacing-lg;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-xs;
  padding: $spacing-md;
  border-radius: $radius-md;
  background-color: $accent-color;
  font-size: $font-md;
  color: $primary-color;

  &__icon {
    font-size: $font-lg;
  }
}

/* 进度条 */
.progress-bar {
  margin-top: $spacing-lg;

  &__track {
    height: 12rpx;
    background-color: $border-color;
    border-radius: 6rpx;
    overflow: hidden;
  }

  &__fill {
    height: 100%;
    background: linear-gradient(90deg, $primary-color, $secondary-color);
    border-radius: 6rpx;
    transition: width 0.3s;
  }

  &__text {
    font-size: $font-sm;
    color: $text-secondary;
    margin-top: $spacing-xs;
    display: block;
    text-align: center;
  }
}

/* 提交按钮 */
.submit-btn {
  margin-top: $spacing-xl;
  padding: $spacing-lg 0;
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  border-radius: $radius-lg;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(43, 122, 120, 0.3);

  &--disabled {
    opacity: 0.6;
  }

  &__text {
    font-size: $font-lg;
    font-weight: 600;
    color: #FFFFFF;
  }
}
</style>
