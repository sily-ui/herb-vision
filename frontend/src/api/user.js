/**
 * 用户相关接口
 */
import { get, post } from './request'

/**
 * 微信登录
 * @param {string} code - 微信登录code
 */
export function wxLogin(code) {
  return post('/api/auth/wx-login', { code })
}

/**
 * 获取用户信息
 */
export function getUserProfile() {
  return get('/api/user/profile')
}

/**
 * 更新用户信息
 * @param {object} data - 用户信息 { nickname, avatar }
 */
export function updateUserProfile(data) {
  return post('/api/user/profile', data)
}

/**
 * 获取识别记录
 * @param {object} params - 查询参数 { page, pageSize }
 */
export function getRecords(params = {}) {
  const { page, pageSize } = params
  return get('/api/user/records', {
    page: page || 1,
    page_size: pageSize || 20
  })
}

/**
 * 删除识别记录
 * @param {string|number} id - 记录ID
 */
export function deleteRecord(id) {
  return post(`/api/user/records/${id}/delete`)
}

/**
 * 获取收藏列表
 * @param {object} params - 查询参数 { page, pageSize }
 */
export function getFavorites(params = {}) {
  const { page, pageSize } = params
  return get('/api/user/favorites', {
    page: page || 1,
    page_size: pageSize || 20
  })
}

/**
 * 添加收藏（后端期望 query 参数 record_id）
 * @param {string|number} recordId - 记录/药材ID
 */
export function addFavorite(recordId) {
  return post('/api/user/favorites', null, { params: { record_id: recordId } })
}

/**
 * 取消收藏
 * @param {string|number} recordId - 记录/药材ID
 */
export function removeFavorite(recordId) {
  return post(`/api/user/favorites/${recordId}/delete`)
}
