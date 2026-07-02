/**
 * 登录鉴权工具
 */

const TOKEN_KEY = 'token'

/**
 * 获取token
 * @returns {string} token
 */
export function getToken() {
  return uni.getStorageSync(TOKEN_KEY) || ''
}

/**
 * 设置token
 * @param {string} token
 */
export function setToken(token) {
  uni.setStorageSync(TOKEN_KEY, token)
}

/**
 * 移除token
 */
export function removeToken() {
  uni.removeStorageSync(TOKEN_KEY)
}

/**
 * 检查登录态，未登录跳转到个人中心页
 * @param {boolean} redirect - 是否跳转
 * @returns {boolean} 是否已登录
 */
export function checkLogin(redirect = true) {
  const token = getToken()
  if (!token) {
    if (redirect) {
      uni.showToast({
        title: '请先登录',
        icon: 'none'
      })
      setTimeout(() => {
        uni.switchTab({
          url: '/pages/mine/index'
        })
      }, 1500)
    }
    return false
  }
  return true
}
