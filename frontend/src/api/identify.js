/**
 * 识别相关接口
 */
import { upload } from './request'

/**
 * 上传图片进行AI识别
 * @param {string} imagePath - 图片本地路径
 * @returns {Promise} 识别结果
 */
export function identifyImage(imagePath) {
  // 后端期望字段名为 file；AI 识别较慢，超时设为 90 秒
  return upload('/api/identify', imagePath, 'file', {}, { timeout: 90000 })
}
