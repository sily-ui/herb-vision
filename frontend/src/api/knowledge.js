/**
 * 知识库相关接口
 */
import { get, post } from './request'

/**
 * 获取药材列表（分页+筛选）
 * @param {object} params - 查询参数 { page, pageSize, categoryPart, categoryEfficacy, keyword }
 */
export function getHerbs(params = {}) {
  const { page, pageSize, categoryPart, categoryEfficacy, keyword } = params
  const query = {}
  if (page) query.page = page
  if (pageSize) query.page_size = pageSize
  if (categoryPart) query.category_part = categoryPart
  if (categoryEfficacy) query.category_efficacy = categoryEfficacy
  if (keyword) query.keyword = keyword
  return get('/api/herbs', query)
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
  return get('/api/herbs/compare', { q: `${id1},${id2}` }, { timeout: 60000 })
}

/**
 * AI 智能对比两个药材
 * @param {string|number} id1 - 药材1 ID
 * @param {string|number} id2 - 药材2 ID
 */
export function aiCompareHerbs(id1, id2) {
  return get('/api/herbs/ai-compare', { q: `${id1},${id2}` }, { timeout: 60000 })
}

/**
 * 模糊搜索（通过描述搜索）
 * @param {string} description - 描述文字
 */
export function fuzzySearch(description) {
  return post('/api/herbs/fuzzy-search', { description })
}
