<template>
  <view class="page-records">
    <!-- 顶部操作栏 -->
    <view class="top-bar">
      <text class="top-bar__count">共 {{ records.length }} 条记录</text>
      <view class="top-bar__btn" @click="toggleBatchMode">
        <text>{{ isBatchMode ? '取消' : '批量删除' }}</text>
      </view>
    </view>

    <!-- 记录列表 -->
    <view class="record-list" v-if="records.length">
      <view
        class="record-item"
        v-for="(item, index) in records"
        :key="index"
        @click="onItemClick(item)"
      >
        <!-- 批量选择框 -->
        <view class="record-item__check" v-if="isBatchMode" @click.stop="toggleSelect(item)">
          <text class="record-item__check-icon">{{ selectedIds.includes(item.id) ? '&#x2611;' : '&#x2610;' }}</text>
        </view>
        <image :src="item.image_path || '/static/images/placeholder.png'" mode="aspectFill" class="record-item__img" />
        <view class="record-item__info">
          <text class="record-item__name">{{ item.herb_name || '未知药材' }}</text>
          <text class="record-item__time">{{ item.created_at }}</text>
        </view>
        <view class="record-item__fav" @click.stop="onToggleFav(item)">
          <text>{{ item.is_favorited ? '&#x2B50;' : '&#x2606;' }}</text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-else>
      <text class="empty-state__icon">&#x1F4CB;</text>
      <text class="empty-state__text">暂无识别记录</text>
      <text class="empty-state__hint">快去首页拍照识别吧</text>
    </view>

    <!-- 批量删除底部栏 -->
    <view class="batch-bar" v-if="isBatchMode">
      <view class="batch-bar__select-all" @click="selectAll">
        <text>{{ isAllSelected ? '取消全选' : '全选' }}</text>
      </view>
      <view class="batch-bar__delete" :class="{ 'batch-bar__delete--disabled': !selectedIds.length }" @click="batchDelete">
        <text>删除({{ selectedIds.length }})</text>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 识别记录页
 * 展示历史识别记录，支持删除和收藏
 */
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getRecords, deleteRecord, addFavorite, removeFavorite } from '@/api/user'

const records = ref([])
const isBatchMode = ref(false)
const selectedIds = ref([])
const page = ref(1)
const pageSize = 20
const hasMore = ref(true)

const isAllSelected = computed(() => {
  return records.value.length > 0 && selectedIds.value.length === records.value.length
})

onShow(() => {
  loadRecords()
})

/**
 * 加载识别记录
 */
async function loadRecords() {
  try {
    const data = await getRecords({ page: page.value, pageSize })
    if (page.value === 1) {
      records.value = data.list || []
    } else {
      records.value.push(...(data.list || []))
    }
    hasMore.value = (data.list || []).length >= pageSize
  } catch (err) {
    // 静默处理
  }
}

/**
 * 切换批量模式
 */
function toggleBatchMode() {
  isBatchMode.value = !isBatchMode.value
  selectedIds.value = []
}

/**
 * 切换选择
 */
function toggleSelect(item) {
  const idx = selectedIds.value.indexOf(item.id)
  if (idx > -1) {
    selectedIds.value.splice(idx, 1)
  } else {
    selectedIds.value.push(item.id)
  }
}

/**
 * 全选/取消全选
 */
function selectAll() {
  if (isAllSelected.value) {
    selectedIds.value = []
  } else {
    selectedIds.value = records.value.map(item => item.id)
  }
}

/**
 * 批量删除
 */
async function batchDelete() {
  if (!selectedIds.value.length) return

  uni.showModal({
    title: '提示',
    content: `确定删除选中的${selectedIds.value.length}条记录？`,
    success: async (res) => {
      if (res.confirm) {
        try {
          for (const id of selectedIds.value) {
            await deleteRecord(id)
          }
          records.value = records.value.filter(item => !selectedIds.value.includes(item.id))
          selectedIds.value = []
          isBatchMode.value = false
          uni.showToast({ title: '删除成功', icon: 'none' })
        } catch (err) {
          uni.showToast({ title: '删除失败', icon: 'none' })
        }
      }
    }
  })
}

/**
 * 点击记录项
 */
function onItemClick(item) {
  if (isBatchMode.value) {
    toggleSelect(item)
    return
  }
  // 查看识别结果详情
  if (item.herb_id) {
    uni.navigateTo({
      url: `/pages/knowledge/detail?id=${item.herb_id}`
    })
  }
}

/**
 * 切换收藏
 */
async function onToggleFav(item) {
  try {
    if (item.is_favorited) {
      await removeFavorite(item.id)
      item.is_favorited = false
      uni.showToast({ title: '已取消收藏', icon: 'none' })
    } else {
      await addFavorite(item.id)
      item.is_favorited = true
      uni.showToast({ title: '收藏成功', icon: 'none' })
    }
  } catch (err) {
    // 静默处理
  }
}
</script>

<style lang="scss" scoped>
.page-records {
  min-height: 100vh;
  background-color: $bg-color;
  padding-bottom: 120rpx;
}

/* 顶部操作栏 */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
  border-bottom: 1rpx solid $border-color;

  &__count {
    font-size: $font-sm;
    color: $text-secondary;
  }

  &__btn {
    font-size: $font-sm;
    color: $primary-color;
    padding: 8rpx $spacing-md;
    border: 1rpx solid $primary-color;
    border-radius: $radius-sm;
  }
}

/* 记录列表 */
.record-list {
  padding: $spacing-md $spacing-lg;
}

.record-item {
  display: flex;
  align-items: center;
  background-color: $card-bg;
  border-radius: $radius-md;
  padding: $spacing-md;
  margin-bottom: $spacing-md;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
  gap: $spacing-md;

  &__check {
    flex-shrink: 0;

    &-icon {
      font-size: 44rpx;
    }
  }

  &__img {
    width: 120rpx;
    height: 120rpx;
    border-radius: $radius-md;
    background-color: $border-color;
    flex-shrink: 0;
  }

  &__info {
    flex: 1;
  }

  &__name {
    font-size: $font-lg;
    font-weight: 500;
    color: $text-color;
    display: block;
  }

  &__time {
    font-size: $font-xs;
    color: $text-secondary;
    display: block;
    margin-top: $spacing-xs;
  }

  &__fav {
    font-size: 40rpx;
    flex-shrink: 0;
  }
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 200rpx;

  &__icon {
    font-size: 100rpx;
  }

  &__text {
    font-size: $font-lg;
    color: $text-secondary;
    margin-top: $spacing-lg;
  }

  &__hint {
    font-size: $font-sm;
    color: $text-secondary;
    margin-top: $spacing-sm;
  }
}

/* 批量删除栏 */
.batch-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md $spacing-lg;
  padding-bottom: calc(#{$spacing-md} + env(safe-area-inset-bottom));
  background-color: $card-bg;
  box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.06);
  z-index: 100;

  &__select-all {
    font-size: $font-md;
    color: $primary-color;
  }

  &__delete {
    padding: $spacing-sm $spacing-lg;
    background: linear-gradient(135deg, $danger-color, #F78989);
    border-radius: $radius-lg;
    color: #FFFFFF;
    font-size: $font-md;
    font-weight: 600;

    &--disabled {
      opacity: 0.5;
    }
  }
}
</style>
