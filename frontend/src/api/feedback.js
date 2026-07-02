/**
 * 反馈相关接口
 */
import { get, post } from './request'

/**
 * 提交反馈
 * @param {object} data - 反馈数据 { type, content, herbId, images }
 */
export function submitFeedback(data) {
  return post('/api/feedback', data)
}

/**
 * 获取反馈列表
 * @param {object} params - 查询参数 { page, pageSize }
 */
export function getFeedbackList(params = {}) {
  return get('/api/feedback', params)
}
