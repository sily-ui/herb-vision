/**
 * 通用工具函数
 */

/**
 * 解析后端图片路径为完整 URL
 * 后端返回 /static/images/herbs/xxx.png 这样的相对路径，
 * 前端需要拼接 BASE_URL 才能正常加载
 * @param {string} path - 图片路径
 * @returns {string} 完整 URL 或本地占位图路径
 */
export function resolveImageUrl(path) {
  if (!path) return '/static/images/placeholder.png'
  if (path.startsWith('http')) return path
  // 后端返回的药材图片等资源路径，拼接 BASE_URL
  if (path.includes('/images/herbs/') || path.includes('/images/identify/')) {
    const BASE_URL = import.meta.env.VITE_BASE_URL || 'http://localhost:8000'
    return `${BASE_URL}${path}`
  }
  // 小程序本地 static 资源
  return path
}

/**
 * 格式化日期
 * @param {number|string|Date} timestamp - 时间戳或日期对象
 * @param {string} format - 格式类型 'full'|'date'|'time'|'relative'
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(timestamp, format = 'full') {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  switch (format) {
    case 'date':
      return `${year}-${month}-${day}`
    case 'time':
      return `${hours}:${minutes}:${seconds}`
    case 'relative':
      return getRelativeTime(date)
    case 'full':
    default:
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
  }
}

/**
 * 获取相对时间（如：刚刚、5分钟前、1小时前）
 */
function getRelativeTime(date) {
  const now = Date.now()
  const diff = now - date.getTime()
  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour

  if (diff < minute) return '刚刚'
  if (diff < hour) return `${Math.floor(diff / minute)}分钟前`
  if (diff < day) return `${Math.floor(diff / hour)}小时前`
  if (diff < 30 * day) return `${Math.floor(diff / day)}天前`
  return formatDate(date.getTime(), 'date')
}

/**
 * 压缩图片
 * @param {string} path - 图片路径
 * @param {object} options - 压缩选项 { quality, width, height }
 * @returns {Promise<string>} 压缩后的图片路径
 */
export function compressImage(path, options = {}) {
  const { quality = 80, width = 1080 } = options
  return new Promise((resolve, reject) => {
    uni.compressImage({
      src: path,
      quality,
      compressedWidth: width,
      success: (res) => {
        resolve(res.tempFilePath)
      },
      fail: (err) => {
        // 压缩失败返回原图
        console.warn('图片压缩失败，使用原图:', err)
        resolve(path)
      }
    })
  })
}

/**
 * 节流函数
 * @param {function} fn - 需要节流的函数
 * @param {number} delay - 节流时间(ms)
 * @returns {function} 节流后的函数
 */
export function throttle(fn, delay = 300) {
  let last = 0
  return function (...args) {
    const now = Date.now()
    if (now - last >= delay) {
      last = now
      return fn.apply(this, args)
    }
  }
}

/**
 * 防抖函数
 * @param {function} fn - 需要防抖的函数
 * @param {number} delay - 防抖时间(ms)
 * @returns {function} 防抖后的函数
 */
export function debounce(fn, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
      timer = null
    }, delay)
  }
}
