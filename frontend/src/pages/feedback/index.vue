<template>
  <view class="page-feedback">
    <!-- 反馈类型 -->
    <view class="type-section">
      <text class="type-section__title">反馈类型</text>
      <view class="type-section__list">
        <view
          class="type-item"
          :class="{ 'type-item--active': form.feedback_type === item.value }"
          v-for="(item, index) in feedbackTypes"
          :key="index"
          @click="form.feedback_type = item.value"
        >
          <text>{{ item.label }}</text>
        </view>
      </view>
    </view>

    <!-- 关联药材 -->
    <view class="herb-section" @click="onSelectHerb">
      <text class="herb-section__label">关联药材</text>
      <text class="herb-section__value">{{ selectedHerbName || '点击选择（可选）' }}</text>
      <text class="herb-section__arrow">&#x276F;</text>
    </view>

    <!-- 反馈内容 -->
    <view class="content-section">
      <text class="content-section__title">反馈内容</text>
      <textarea
        class="content-section__textarea"
        v-model="form.content"
        placeholder="请详细描述您遇到的问题..."
        maxlength="500"
      />
      <text class="content-section__count">{{ form.content.length }}/500</text>
    </view>

    <!-- 图片上传 -->
    <view class="image-section">
      <text class="image-section__title">上传图片（可选，最多3张）</text>
      <view class="image-section__list">
        <view class="image-item" v-for="(img, index) in imageList" :key="index">
          <image :src="img" mode="aspectFill" class="image-item__img" />
          <view class="image-item__delete" @click="removeImage(index)">&#x2715;</view>
        </view>
        <view class="image-add" v-if="imageList.length < 3" @click="onChooseImage">
          <text class="image-add__icon">+</text>
        </view>
      </view>
    </view>

    <!-- 提交按钮 -->
    <view class="submit-btn" @click="onSubmit">
      <text class="submit-btn__text">提交反馈</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 意见反馈页
 * 用户提交识别错误、资料缺失等反馈
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { submitFeedback } from '@/api/feedback'
import { upload } from '@/api/request'

const feedbackTypes = [
  { label: '识别错误', value: 'identify_error' },
  { label: '资料缺失', value: 'data_missing' },
  { label: '其他', value: 'other' }
]

const form = ref({
  feedback_type: 'identify_error',
  herb_id: null,
  content: ''
})

const selectedHerbName = ref('')
const imageList = ref([])

onLoad((query) => {
  if (query.herbId) {
    form.value.herb_id = parseInt(query.herbId)
  }
})

/**
 * 选择关联药材
 */
function onSelectHerb() {
  uni.navigateTo({
    url: '/pages/knowledge/search?mode=select',
    events: {
      selectHerb: (data) => {
        form.value.herb_id = data.id
        selectedHerbName.value = data.name
      }
    }
  })
}

/**
 * 选择图片
 */
function onChooseImage() {
  uni.chooseImage({
    count: 3 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      imageList.value.push(...res.tempFilePaths)
    }
  })
}

/**
 * 移除图片
 */
function removeImage(index) {
  imageList.value.splice(index, 1)
}

/**
 * 提交反馈
 */
async function onSubmit() {
  if (!form.value.content.trim()) {
    uni.showToast({ title: '请输入反馈内容', icon: 'none' })
    return
  }

  uni.showLoading({ title: '提交中...' })

  try {
    // 上传图片
    const imagePaths = []
    for (const img of imageList.value) {
      try {
        const res = await upload('/api/upload', img)
        imagePaths.push(res.path)
      } catch (err) {
        // 上传失败跳过
      }
    }

    await submitFeedback({
      feedback_type: form.value.feedback_type,
      herb_id: form.value.herb_id,
      content: form.value.content,
      image_paths: imagePaths
    })

    uni.hideLoading()
    uni.showToast({ title: '提交成功，感谢反馈', icon: 'none' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (err) {
    uni.hideLoading()
    uni.showToast({ title: '提交失败，请重试', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.page-feedback {
  min-height: 100vh;
  background-color: $bg-color;
  padding: $spacing-lg;
}

/* 反馈类型 */
.type-section {
  background-color: $card-bg;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
    display: block;
    margin-bottom: $spacing-md;
  }

  &__list {
    display: flex;
    gap: $spacing-md;
  }
}

.type-item {
  flex: 1;
  text-align: center;
  padding: $spacing-md 0;
  border: 2rpx solid $border-color;
  border-radius: $radius-md;
  font-size: $font-md;
  color: $text-secondary;

  &--active {
    border-color: $primary-color;
    color: $primary-color;
    background-color: $accent-color;
  }
}

/* 关联药材 */
.herb-section {
  display: flex;
  align-items: center;
  background-color: $card-bg;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;

  &__label {
    font-size: $font-md;
    color: $text-color;
    flex-shrink: 0;
  }

  &__value {
    flex: 1;
    font-size: $font-md;
    color: $text-secondary;
    margin-left: $spacing-md;
    text-align: right;
  }

  &__arrow {
    font-size: $font-sm;
    color: $text-secondary;
    margin-left: $spacing-sm;
  }
}

/* 反馈内容 */
.content-section {
  background-color: $card-bg;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;

  &__title {
    font-size: $font-lg;
    font-weight: 600;
    color: $text-color;
    display: block;
    margin-bottom: $spacing-md;
  }

  &__textarea {
    width: 100%;
    height: 240rpx;
    font-size: $font-md;
    color: $text-color;
    line-height: 1.6;
  }

  &__count {
    font-size: $font-xs;
    color: $text-secondary;
    display: block;
    text-align: right;
    margin-top: $spacing-sm;
  }
}

/* 图片上传 */
.image-section {
  background-color: $card-bg;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-xl;

  &__title {
    font-size: $font-md;
    color: $text-color;
    display: block;
    margin-bottom: $spacing-md;
  }

  &__list {
    display: flex;
    gap: $spacing-md;
    flex-wrap: wrap;
  }
}

.image-item {
  position: relative;
  width: 180rpx;
  height: 180rpx;

  &__img {
    width: 100%;
    height: 100%;
    border-radius: $radius-md;
  }

  &__delete {
    position: absolute;
    top: -10rpx;
    right: -10rpx;
    width: 40rpx;
    height: 40rpx;
    background-color: $danger-color;
    border-radius: 50%;
    color: #FFFFFF;
    font-size: $font-xs;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.image-add {
  width: 180rpx;
  height: 180rpx;
  border: 2rpx dashed $border-color;
  border-radius: $radius-md;
  display: flex;
  align-items: center;
  justify-content: center;

  &__icon {
    font-size: 60rpx;
    color: $text-secondary;
  }
}

/* 提交按钮 */
.submit-btn {
  padding: $spacing-lg 0;
  background: linear-gradient(135deg, $primary-color, $secondary-color);
  border-radius: $radius-lg;
  text-align: center;

  &__text {
    font-size: $font-lg;
    font-weight: 600;
    color: #FFFFFF;
  }
}
</style>
