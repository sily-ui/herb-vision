<script setup>
import { onLaunch } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App Launch')
})
</script>

<style lang="scss">
/* ============================================================
 * 全局基础样式 · 墨韵（硬编码，因为非 scoped style 不自动注入 uni.scss）
 * ============================================================ */

page {
  background-color: #FAF8F3;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Source Han Sans CN", sans-serif;
  color: #1A1A1A;
  font-size: 26rpx;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 0.4rpx;
}

/* 全局衬线字（用于数字、特殊标题） */
.font-serif {
  font-family: "Songti SC", "STSong", "Source Han Serif CN", "Noto Serif CJK SC", "SimSun", serif;
}

/* 通用工具类 */
.text-ink { color: #1A1A1A; }
.text-soft { color: #4A4A4A; }
.text-light { color: #8C8C8C; }
.text-cinnabar { color: #A8362F; }
.text-bamboo { color: #3D5A4A; }
.text-gold { color: #A88A5C; }

.font-xs { font-size: 20rpx; }
.font-sm { font-size: 22rpx; }
.font-md { font-size: 26rpx; }
.font-lg { font-size: 30rpx; }
.font-xl { font-size: 36rpx; }
.font-2xl { font-size: 44rpx; }

.weight-light { font-weight: 300; }
.weight-regular { font-weight: 400; }
.weight-medium { font-weight: 500; }
.weight-semibold { font-weight: 600; }
.weight-bold { font-weight: 700; }

/* 章节标题装饰：左侧朱砂竖线 */
.section-title {
  display: flex;
  align-items: center;
  font-size: 30rpx;
  font-weight: 600;
  color: #1A1A1A;
  letter-spacing: 1rpx;
}

.section-title::before {
  content: "";
  display: inline-block;
  width: 4rpx;
  height: 28rpx;
  background-color: #A8362F;
  margin-right: 16rpx;
}

/* 印章风格徽章 */
.seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4rpx 12rpx;
  background-color: #A8362F;
  color: #FFFFFF;
  font-size: 20rpx;
  font-weight: 500;
  border-radius: 2rpx;
  letter-spacing: 2rpx;
}

/* 细线分割 */
.hairline-top { border-top: 1rpx solid #E5DFD2; }
.hairline-bottom { border-bottom: 1rpx solid #E5DFD2; }
</style>
