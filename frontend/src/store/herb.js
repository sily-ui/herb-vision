/**
 * 药材状态管理
 */
import { defineStore } from 'pinia'

export const useHerbStore = defineStore('herb', {
  state: () => ({
    // 当前查看的药材
    currentHerb: null,
    // 搜索历史
    searchHistory: uni.getStorageSync('searchHistory') || [],
    // 最近浏览
    recentViewed: uni.getStorageSync('recentViewed') || []
  }),

  actions: {
    /**
     * 设置当前药材
     */
    setCurrentHerb(herb) {
      this.currentHerb = herb
    },

    /**
     * 添加搜索历史
     */
    addSearchHistory(keyword) {
      if (!keyword || !keyword.trim()) return
      // 去重，保留最近20条
      const list = this.searchHistory.filter(item => item !== keyword)
      list.unshift(keyword)
      if (list.length > 20) list.pop()
      this.searchHistory = list
      uni.setStorageSync('searchHistory', list)
    },

    /**
     * 清空搜索历史
     */
    clearSearchHistory() {
      this.searchHistory = []
      uni.removeStorageSync('searchHistory')
    },

    /**
     * 添加最近浏览
     */
    addRecentViewed(herb) {
      if (!herb || !herb.id) return
      // 去重，保留最近30条
      const list = this.recentViewed.filter(item => item.id !== herb.id)
      list.unshift({
        id: herb.id,
        name: herb.name,
        image: herb.image || '',
        viewedAt: Date.now()
      })
      if (list.length > 30) list.pop()
      this.recentViewed = list
      uni.setStorageSync('recentViewed', list)
    },

    /**
     * 清空最近浏览
     */
    clearRecentViewed() {
      this.recentViewed = []
      uni.removeStorageSync('recentViewed')
    }
  }
})
