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
  return upload('/api/identify', imagePath, 'image')
}
