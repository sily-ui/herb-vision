<template>
  <view class="page-profile">
    <!-- 头像 -->
    <view class="avatar-section" @click="onChooseAvatar">
      <image :src="form.avatar_url || '/static/images/placeholder.png'" mode="aspectFill" class="avatar-section__img" />
      <view class="avatar-section__edit">
        <text>修改头像</text>
      </view>
    </view>

    <!-- 表单 -->
    <view class="form-section">
      <view class="form-item">
        <text class="form-item__label">昵称</text>
        <input class="form-item__input" v-model="form.nickname" placeholder="请输入昵称" />
      </view>
      <view class="form-item">
        <text class="form-item__label">手机号</text>
        <input class="form-item__input" v-model="form.phone" placeholder="请输入手机号" type="number" maxlength="11" />
      </view>
    </view>

    <!-- 保存按钮 -->
    <view class="save-btn" @click="onSave">
      <text class="save-btn__text">保存</text>
    </view>
  </view>
</template>

<script setup>
/**
 * 编辑资料页
 * 修改用户头像、昵称、手机号
 */
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { getUserProfile, updateUserProfile } from '@/api/user'

const userStore = useUserStore()

const form = ref({
  avatar_url: '',
  nickname: '',
  phone: ''
})

onLoad(() => {
  loadProfile()
})

/**
 * 加载用户信息
 */
async function loadProfile() {
  try {
    const data = await getUserProfile()
    form.value = {
      avatar_url: data.avatar_url || '',
      nickname: data.nickname || '',
      phone: data.phone || ''
    }
  } catch (err) {
    // 使用本地缓存
    form.value.nickname = userStore.nickname || ''
    form.value.avatar_url = userStore.avatar || ''
  }
}

/**
 * 选择头像
 */
function onChooseAvatar() {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      form.value.avatar_url = res.tempFilePaths[0]
    }
  })
}

/**
 * 保存
 */
async function onSave() {
  if (!form.value.nickname.trim()) {
    uni.showToast({ title: '请输入昵称', icon: 'none' })
    return
  }

  try {
    await updateUserProfile({
      nickname: form.value.nickname,
      avatar_url: form.value.avatar_url,
      phone: form.value.phone
    })
    userStore.nickname = form.value.nickname
    userStore.avatar = form.value.avatar_url
    uni.showToast({ title: '保存成功', icon: 'none' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (err) {
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.page-profile {
  min-height: 100vh;
  background-color: $bg-color;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-xl 0;
  background-color: $card-bg;

  &__img {
    width: 160rpx;
    height: 160rpx;
    border-radius: 50%;
    background-color: $border-color;
  }

  &__edit {
    margin-top: $spacing-md;
    font-size: $font-sm;
    color: $primary-color;
  }
}

/* 表单区域 */
.form-section {
  margin: $spacing-lg;
  background-color: $card-bg;
  border-radius: $radius-lg;
  overflow: hidden;
}

.form-item {
  display: flex;
  align-items: center;
  padding: $spacing-lg;
  border-bottom: 1rpx solid $border-color;

  &:last-child {
    border-bottom: none;
  }

  &__label {
    width: 140rpx;
    font-size: $font-md;
    color: $text-color;
    flex-shrink: 0;
  }

  &__input {
    flex: 1;
    font-size: $font-md;
    color: $text-color;
  }
}

/* 保存按钮 */
.save-btn {
  margin: $spacing-xl $spacing-lg;
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
