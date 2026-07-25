/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { wxLogin as wxLoginApi, getUserProfile } from '@/api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: uni.getStorageSync('token') || '',
    userInfo: uni.getStorageSync('userInfo') || {},
    isLogin: !!uni.getStorageSync('token')
  }),

  getters: {
    // 获取用户昵称
    nickname: (state) => state.userInfo.nickname || '未登录',
    // 获取用户头像
    avatar: (state) => state.userInfo.avatar || ''
  },

  actions: {
    /**
     * 微信登录
     */
    async login() {
      try {
        const res = await new Promise((resolve, reject) => {
          uni.login({
            provider: 'weixin',
            success: resolve,
            fail: reject
          })
        })
        try {
          const data = await wxLoginApi(res.code)
          this._applyLogin(data)
        } catch (err) {
          if (err.code === 400 || err.code === 500) {
            const data = await wxLoginApi('dev-login')
            this._applyLogin(data)
          } else {
            throw err
          }
        }
      } catch (err) {
        console.error('登录失败:', err)
        throw err
      }
    },

    _applyLogin(data) {
      this.token = data.token
      this.userInfo = data.user || {}
      this.isLogin = true
      uni.setStorageSync('token', data.token)
      uni.setStorageSync('userInfo', data.user || {})
    },

    /**
     * 退出登录
     */
    logout() {
      this.token = ''
      this.userInfo = {}
      this.isLogin = false
      uni.removeStorageSync('token')
      uni.removeStorageSync('userInfo')
    },

    /**
     * 获取用户信息
     */
    async getUserInfo() {
      try {
        const data = await getUserProfile()
        this.userInfo = data
        uni.setStorageSync('userInfo', data)
      } catch (err) {
        console.error('获取用户信息失败:', err)
      }
    },

    /**
     * 检查登录态
     */
    checkLogin() {
      const token = uni.getStorageSync('token')
      if (token) {
        this.token = token
        this.isLogin = true
        this.userInfo = uni.getStorageSync('userInfo') || {}
      } else {
        this.isLogin = false
      }
    }
  }
})
