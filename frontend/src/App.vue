<script setup>
import { onLaunch } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

onLaunch(() => {
  console.log('App Launch')
  // 检查登录态
  const userStore = useUserStore()
  userStore.checkLogin()
})
</script>

<style>
/* 全局样式 */
page {
  background-color: #F7F8FA;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #17252A;
  font-size: 28rpx;
}
</style>
