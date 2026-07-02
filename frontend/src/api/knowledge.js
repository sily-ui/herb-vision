/**
 * 知识库相关接口
 */
import { get, post } from './request'

/**
 * 获取药材列表
 * @param {object} params - 查询参数 { page, pageSize, category, part }
 */
export function getHerbs(params = {}) {
  return get('/api/herbs', params)
}

/**
 * 获取药材详情
 * @param {string|number} id - 药材ID
 */
export function getHerbDetail(id) {
  return get(`/api/herbs/${id}`)
}

/**
 * 搜索药材
 * @param {string} keyword - 搜索关键词
 */
export function searchHerbs(keyword) {
  return get('/api/herbs/search', { keyword })
}

/**
 * 对比两个药材
 * @param {string|number} id1 - 药材1 ID
 * @param {string|number} id2 - 药材2 ID
 */
export function compareHerbs(id1, id2) {
  return get('/api/herbs/compare', { id1, id2 })
}

/**
 * 模糊搜索（通过描述搜索）
 * @param {string} description - 描述文字
 */
export function fuzzySearch(description) {
  return post('/api/herbs/fuzzy-search', { description })
}
