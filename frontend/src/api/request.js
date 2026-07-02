/**
 * 请求封装 - 基于 uni.request
 */

// 开发环境基础地址（与后端 FastAPI 端口一致）
const BASE_URL = 'http://localhost:8000'

// 请求超时时间
const TIMEOUT = 30000

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
 * 统一响应拦截 - 处理错误和401
 */
function handleResponse(response) {
  const { statusCode, data } = response

  if (statusCode === 401) {
    // token过期，跳转登录
    uni.removeStorageSync('token')
    uni.showToast({
      title: '登录已过期，请重新登录',
      icon: 'none'
    })
    setTimeout(() => {
      uni.reLaunch({
        url: '/pages/mine/index'
      })
    }, 1500)
    return Promise.reject(new Error('登录已过期'))
  }

  if (statusCode >= 200 && statusCode < 300) {
    // 后端返回格式 { code, data, message }
    if (data.code === 0 || data.code === 200) {
      return data.data
    }
    // 业务错误
    uni.showToast({
      title: data.message || '请求失败',
      icon: 'none'
    })
    return Promise.reject(new Error(data.message || '请求失败'))
  }

  // HTTP错误
  uni.showToast({
    title: `请求错误(${statusCode})`,
    icon: 'none'
  })
  return Promise.reject(new Error(`请求错误(${statusCode})`))
}

/**
 * GET请求
 */
export function get(url, params = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method: 'GET',
      data: params,
      header: getRequestHeader(),
      timeout: TIMEOUT,
      success: (res) => {
        handleResponse(res).then(resolve).catch(reject)
      },
      fail: (err) => {
        uni.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

/**
 * POST请求
 */
export function post(url, data = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method: 'POST',
      data,
      header: getRequestHeader(),
      timeout: TIMEOUT,
      success: (res) => {
        handleResponse(res).then(resolve).catch(reject)
      },
      fail: (err) => {
        uni.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

/**
 * 文件上传 - 基于 uni.uploadFile
 */
export function upload(url, filePath, name = 'file', formData = {}) {
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
      timeout: TIMEOUT,
      success: (res) => {
        // uploadFile 返回的 data 是字符串，需要解析
        const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data
        if (res.statusCode >= 200 && res.statusCode < 300) {
          if (data.code === 0 || data.code === 200) {
            resolve(data.data)
          } else {
            uni.showToast({
              title: data.message || '上传失败',
              icon: 'none'
            })
            reject(new Error(data.message || '上传失败'))
          }
        } else {
          reject(new Error(`上传错误(${res.statusCode})`))
        }
      },
      fail: (err) => {
        uni.showToast({
          title: '上传失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}
