/**
 * 离线缓存工具
 * 使用 uni.setStorageSync / uni.getStorageSync 实现本地缓存
 */

const CACHE_PREFIX = 'herb_cache_'
const CACHE_INDEX_KEY = 'herb_cache_index'

/**
 * 缓存药材数据
 * @param {object} herb - 药材对象，必须包含id
 */
export function saveHerbCache(herb) {
  if (!herb || !herb.id) return
  try {
    const key = CACHE_PREFIX + herb.id
    const cacheData = {
      ...herb,
      cachedAt: Date.now()
    }
    uni.setStorageSync(key, cacheData)
    // 更新缓存索引
    const index = getCacheIndex()
    if (!index.includes(herb.id)) {
      index.push(herb.id)
      uni.setStorageSync(CACHE_INDEX_KEY, index)
    }
  } catch (err) {
    console.error('缓存保存失败:', err)
  }
}

/**
 * 获取缓存的药材数据
 * @param {string|number} id - 药材ID
 * @returns {object|null} 缓存的药材数据
 */
export function getHerbCache(id) {
  try {
    const key = CACHE_PREFIX + id
    return uni.getStorageSync(key) || null
  } catch (err) {
    console.error('缓存读取失败:', err)
    return null
  }
}

/**
 * 获取所有缓存的药材
 * @returns {array} 缓存的药材列表
 */
export function getAllCachedHerbs() {
  try {
    const index = getCacheIndex()
    return index.map(id => getHerbCache(id)).filter(Boolean)
  } catch (err) {
    console.error('获取缓存列表失败:', err)
    return []
  }
}

/**
 * 删除指定药材缓存
 * @param {string|number} id - 药材ID
 */
export function removeHerbCache(id) {
  try {
    const key = CACHE_PREFIX + id
    uni.removeStorageSync(key)
    const index = getCacheIndex()
    const newIndex = index.filter(item => item !== id)
    uni.setStorageSync(CACHE_INDEX_KEY, newIndex)
  } catch (err) {
    console.error('缓存删除失败:', err)
  }
}

/**
 * 清除所有缓存
 */
export function clearAllCache() {
  try {
    const index = getCacheIndex()
    index.forEach(id => {
      uni.removeStorageSync(CACHE_PREFIX + id)
    })
    uni.removeStorageSync(CACHE_INDEX_KEY)
  } catch (err) {
    console.error('清除缓存失败:', err)
  }
}

/**
 * 获取缓存大小（条数）
 * @returns {number} 缓存条数
 */
export function getCacheSize() {
  return getCacheIndex().length
}

/**
 * 检测网络状态
 * @returns {boolean} 是否在线
 */
export function isOnline() {
  return new Promise((resolve) => {
    uni.getNetworkType({
      success: (res) => {
        resolve(res.networkType !== 'none')
      },
      fail: () => {
        resolve(false)
      }
    })
  })
}

/**
 * 获取缓存索引
 * @returns {array} 缓存ID列表
 */
function getCacheIndex() {
  try {
    return uni.getStorageSync(CACHE_INDEX_KEY) || []
  } catch (err) {
    return []
  }
}
