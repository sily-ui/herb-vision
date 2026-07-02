/**
 * 用户相关接口
 */
import { get, post } from './request'

/**
 * 微信登录
 * @param {string} code - 微信登录code
 */
export function wxLogin(code) {
  return post('/api/user/login', { code })
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
  return get('/api/user/records', params)
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
  return get('/api/user/favorites', params)
}

/**
 * 添加收藏
 * @param {string|number} recordId - 记录/药材ID
 */
export function addFavorite(recordId) {
  return post('/api/user/favorites', { recordId })
}

/**
 * 取消收藏
 * @param {string|number} recordId - 记录/药材ID
 */
export function removeFavorite(recordId) {
  return post(`/api/user/favorites/${recordId}/delete`)
}
