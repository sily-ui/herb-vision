<template>
  <view class="image-uploader">
    <!-- 图片预览列表 -->
    <view class="image-uploader__list">
      <view
        class="image-uploader__item"
        v-for="(item, index) in imageList"
        :key="index"
      >
        <image :src="item" mode="aspectFill" class="image-uploader__preview" />
        <view class="image-uploader__delete" @click="onDelete(index)">
          <text class="image-uploader__delete-icon">&#x2715;</text>
        </view>
        <!-- 上传进度 -->
        <view class="image-uploader__progress" v-if="uploading && index === imageList.length - 1">
          <text class="image-uploader__progress-text">{{ progress }}%</text>
        </view>
      </view>

      <!-- 添加按钮 -->
      <view class="image-uploader__add" v-if="imageList.length < maxCount" @click="onChoose">
        <text class="image-uploader__add-icon">+</text>
        <text class="image-uploader__add-text">添加图片</text>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="image-uploader__actions" v-if="imageList.length > 0">
      <view class="image-uploader__btn image-uploader__btn--camera" @click="onTakePhoto">
        <text class="image-uploader__btn-icon">&#x1F4F7;</text>
        <text class="image-uploader__btn-text">拍照</text>
      </view>
      <view class="image-uploader__btn image-uploader__btn--album" @click="onFromAlbum">
        <text class="image-uploader__btn-icon">&#x1F5BC;</text>
        <text class="image-uploader__btn-text">相册</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 图片上传组件
 * 支持拍照、相册选择、多图预览、删除、上传进度
 */
import { ref, watch } from 'vue'

const props = defineProps({
  maxCount: {
    type: Number,
    default: 9
  },
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['change', 'update:modelValue'])

const imageList = ref([...props.modelValue])
const uploading = ref(false)
const progress = ref(0)

watch(() => props.modelValue, (val) => {
  imageList.value = [...val]
})

/**
 * 选择图片（通用）
 */
function onChoose() {
  const remaining = props.maxCount - imageList.value.length
  if (remaining <= 0) return

  uni.chooseImage({
    count: remaining,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      addImages(res.tempFilePaths)
    }
  })
}

/**
 * 拍照
 */
function onTakePhoto() {
  const remaining = props.maxCount - imageList.value.length
  if (remaining <= 0) {
    uni.showToast({ title: `最多上传${props.maxCount}张`, icon: 'none' })
    return
  }

  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['camera'],
    success: (res) => {
      addImages(res.tempFilePaths)
    }
  })
}

/**
 * 从相册选择
 */
function onFromAlbum() {
  const remaining = props.maxCount - imageList.value.length
  if (remaining <= 0) {
    uni.showToast({ title: `最多上传${props.maxCount}张`, icon: 'none' })
    return
  }

  uni.chooseImage({
    count: remaining,
    sizeType: ['compressed'],
    sourceType: ['album'],
    success: (res) => {
      addImages(res.tempFilePaths)
    }
  })
}

/**
 * 添加图片到列表
 */
function addImages(paths) {
  imageList.value.push(...paths)
  emit('change', imageList.value)
  emit('update:modelValue', imageList.value)
}

/**
 * 删除图片
 */
function onDelete(index) {
  imageList.value.splice(index, 1)
  emit('change', imageList.value)
  emit('update:modelValue', imageList.value)
}

/**
 * 设置上传进度（供外部调用）
 */
function setProgress(val) {
  progress.value = val
  if (val >= 100) {
    setTimeout(() => {
      uploading.value = false
      progress.value = 0
    }, 500)
  }
}

/**
 * 设置上传状态
 */
function setUploading(val) {
  uploading.value = val
}

defineExpose({
  setProgress,
  setUploading
})
</script>

<style lang="scss" scoped>
.image-uploader {
  &__list {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;
  }

  &__item {
    position: relative;
    width: 200rpx;
    height: 200rpx;
    border-radius: $radius-md;
    overflow: hidden;
  }

  &__preview {
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
    border-radius: 0 0 0 $radius-sm;
  }

  &__delete-icon {
    color: #FFFFFF;
    font-size: $font-xs;
  }

  &__progress {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40rpx;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__progress-text {
    color: #FFFFFF;
    font-size: $font-xs;
  }

  &__add {
    width: 200rpx;
    height: 200rpx;
    border: 2rpx dashed $border-color;
    border-radius: $radius-md;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: $spacing-xs;
    background-color: $bg-color;
  }

  &__add-icon {
    font-size: 48rpx;
    color: $text-secondary;
  }

  &__add-text {
    font-size: $font-xs;
    color: $text-secondary;
  }

  &__actions {
    display: flex;
    gap: $spacing-md;
    margin-top: $spacing-md;
  }

  &__btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: $spacing-md;
    border-radius: $radius-md;
    background-color: $card-bg;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
    gap: $spacing-xs;

    &--camera {
      background-color: $accent-color;
    }

    &--album {
      background-color: $accent-color;
    }
  }

  &__btn-icon {
    font-size: 48rpx;
  }

  &__btn-text {
    font-size: $font-sm;
    color: $text-color;
  }
}
</style>
