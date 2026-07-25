/**
 * 请求封装 - 基于 uni.request
 */

// 开发环境基础地址
const BASE_URL = 'http://localhost:8000'

// 请求超时时间
const TIMEOUT = 15000

/**
 * 统一请求拦截 - 自动注入token
 */
function getRequestHeader() {
  const header = {
    'Content-Type': 'application/json'
  }
  const token = uni.getStorageSync('token')
  if (token) {
    header['Authorization'] = `Bearer ${token}`
  }
  return header
}

/**
 * 统一响应拦截 - 兼容两种返回格式：
 *   1) 业务包装: { code, data, message }
 *   2) 裸字典:   { items, total, page, page_size, ... }
 * 同时对 401 仅做静默处理，由业务层决定是否跳转登录。
 */
function handleResponse(response) {
  const { statusCode, data } = response

  if (statusCode === 401) {
    uni.removeStorageSync('token')
    const err = new Error('未登录')
    err.code = 401
    err.silent = true
    return Promise.reject(err)
  }

  if (statusCode < 200 || statusCode >= 300) {
    const err = new Error(`请求错误(${statusCode})`)
    err.code = statusCode
    return Promise.reject(err)
  }

  if (data === null || data === undefined) return Promise.resolve({})

  if (typeof data === 'object' && 'code' in data) {
    if (data.code === 0 || data.code === 200) {
      return Promise.resolve(data.data === undefined ? data : data.data)
    }
    const err = new Error(data.message || '请求失败')
    err.code = data.code
    return Promise.reject(err)
  }

  return Promise.resolve(data)
}

/**
 * GET请求
 */
export function get(url, params = {}, options = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method: 'GET',
      data: params,
      header: getRequestHeader(),
      timeout: options.timeout || TIMEOUT,
      success: (res) => {
        handleResponse(res).then(resolve).catch(reject)
      },
      fail: (err) => {
        const e = new Error('网络请求失败')
        e.code = -1
        if (!options.silent) {
          uni.showToast({ title: '网络请求失败', icon: 'none' })
        }
        reject(e)
      }
    })
  })
}

/**
 * POST请求
 */
export function post(url, data = {}, options = {}) {
  return new Promise((resolve, reject) => {
    // 将 query 参数拼到 URL 上（POST 也支持 query）
    let fullUrl = BASE_URL + url
    if (options.params && Object.keys(options.params).length) {
      const qs = Object.entries(options.params)
        .filter(([, v]) => v !== undefined && v !== null && v !== '')
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&')
      if (qs) fullUrl += (fullUrl.includes('?') ? '&' : '?') + qs
    }

    uni.request({
      url: fullUrl,
      method: 'POST',
      data,
      header: getRequestHeader(),
      timeout: options.timeout || TIMEOUT,
      success: (res) => {
        handleResponse(res).then(resolve).catch(reject)
      },
      fail: (err) => {
        const e = new Error('网络请求失败')
        e.code = -1
        if (!options.silent) {
          uni.showToast({ title: '网络请求失败', icon: 'none' })
        }
        reject(e)
      }
    })
  })
}

/**
 * 文件上传 - 基于 uni.uploadFile
 */
export function upload(url, filePath, name = 'file', formData = {}, options = {}) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')
    const header = {}
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }

    uni.uploadFile({
      url: BASE_URL + url,
      filePath,
      name,
      formData,
      header,
      timeout: options.timeout || TIMEOUT,
      success: (res) => {
        const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data
        handleResponse({ statusCode: res.statusCode, data }).then(resolve).catch(reject)
      },
      fail: (err) => {
        const e = new Error('网络请求失败')
        e.code = -1
        if (!options.silent) {
          uni.showToast({ title: '网络请求失败', icon: 'none' })
        }
        reject(e)
      }
    })
  })
}
