<template>
  <div v-if="show" class="screensaver" @click="hideScreensaver">
    <!-- 添加中心背景 GIF -->
    <div class="center-gif">
      <img src="@/assets/center.gif" alt="background animation">
    </div>

    <!-- 时钟组件 -->
    <div class="clock-widget">
      <div class="time">{{ currentTime }}</div>
      <div class="date">{{ currentDate }}</div>
    </div>

    <!-- 名言名句 -->
    <div class="quote-container">
      <transition-group 
        name="fade" 
        tag="div"
        class="quotes-wrapper"
      >
        <div 
          v-for="(quote, index) in quotes" 
          :key="index"
          class="quote"
          v-show="currentQuoteIndex === index"
        >
          <div class="quote-content">{{ quote.content }}</div>
          <div class="quote-author">—— {{ quote.author }}</div>
        </div>
      </transition-group>
    </div>

    <!-- 左右两个 GIF -->
    <div class="corner-gif left">
      <img src="@/assets/car.gif" alt="left animation">
    </div>
    <div class="corner-gif right">
      <img src="@/assets/coffee.gif" alt="right animation">
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])

// 时钟相关
const currentTime = ref('')
const currentDate = ref('')
let clockTimer = null

// 更新时间函数
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { 
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
  currentDate.value = now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

// 名言数组
const quotes = ref([

  {
    content: "勇敢的人，先享受世界。",
    author: "靳益铭"
  },
 
])

const currentQuoteIndex = ref(0)
let quoteTimer = null
let inactivityTimer = null
let lastActivityTime = Date.now()

// 检查用户活动
const checkInactivity = () => {
  const now = Date.now()
  if (now - lastActivityTime > 5 * 60 * 1000) { // 5分钟
    emit('show')
  }
}

// 重置活动计时器
const resetActivityTimer = () => {
  lastActivityTime = Date.now()
}

onMounted(() => {
  // 启动时钟
  updateTime()
  clockTimer = setInterval(updateTime, 1000)

  // 随机选择名言
  const shuffled = [...quotes.value].sort(() => 0.5 - Math.random())
  quotes.value = shuffled.slice(0, 3)

  // 启动名言切换定时器
  quoteTimer = setInterval(() => {
    currentQuoteIndex.value = (currentQuoteIndex.value + 1) % quotes.value.length
  }, 12000) // 延长到12秒

  // 监听用户活动
  document.addEventListener('mousemove', resetActivityTimer)
  document.addEventListener('keydown', resetActivityTimer)
  document.addEventListener('click', resetActivityTimer)
  
  // 启动不活动检查
  inactivityTimer = setInterval(checkInactivity, 10000) // 每10秒检��一次
})

onBeforeUnmount(() => {
  if (clockTimer) clearInterval(clockTimer)
  if (quoteTimer) clearInterval(quoteTimer)
  if (inactivityTimer) clearInterval(inactivityTimer)
  
  document.removeEventListener('mousemove', resetActivityTimer)
  document.removeEventListener('keydown', resetActivityTimer)
  document.removeEventListener('click', resetActivityTimer)
})

const hideScreensaver = () => {
  emit('close')
}
</script>

<style scoped>
.screensaver {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.98);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 90;
  cursor: pointer;
}

/* 时钟样式 */
.clock-widget {
  position: relative;
  z-index: 2;
  top: 15%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  animation: clockFloat 2s ease-in-out infinite;
}

.time {
  font-size: 5rem;
  font-weight: 700;
  color: #10a37f;
  font-family: 'Arial Black', sans-serif;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: 6px;
  background: linear-gradient(45deg, #10a37f, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientText 5s ease infinite;
}

.date {
  font-size: 1.8rem;
  color: #4b5563;
  font-family: 'STXingkai', 'KaiTi', serif;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.05);
  letter-spacing: 2px;
}

/* 名言样式 */
.quote-container {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 10%;
  margin-top: -3%;
}

.quotes-wrapper {
  position: relative;
  width: 100%;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.quote {
  position: absolute;
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.quote-content {
  font-size: 3.5rem;
  color: #000000;
  font-family: 'STXingkai', 'KaiTi', serif;
  font-weight: 500;
  line-height: 1.8;
  letter-spacing: 4px;
}

.quote-author {
  font-size: 2rem;
  color: #666666;
  font-family: 'STXingkai', 'KaiTi', serif;
  margin-top: 20px;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: all 3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

@keyframes clockFloat {
  0% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

@keyframes gradientText {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .quote-content {
    font-size: 2.5rem;
  }
  
  .quote-author {
    font-size: 1.5rem;
  }
  
  .time {
    font-size: 3.5rem;
  }
  
  .date {
    font-size: 1.2rem;
  }
}

/* 添加 GIF 相关样式 */
.corner-gif {
  position: fixed;
  bottom: 20px;
  z-index: 2;
}

.corner-gif.left {
  left: 20px;
}

.corner-gif.right {
  right: 20px;
}

.corner-gif img {
  width: 320px;
  height: auto;
  border-radius: 8px;
}

/* 添加中心 GIF 样式 */
.center-gif {
  position: fixed;
  top: 50%;
  left: 73%;
  transform: translate(-50%, -50%);
  z-index: 1;
  opacity: 1.3;  /* 降低透明度，避免干扰文字 */
}

.center-gif img {
  width: 400px;
  height: auto;
}

/* 确保其他元素在 GIF 上层 */
.clock-widget {
  position: relative;
  z-index: 2;
}

.quote-container {
  position: relative;
  z-index: 2;
}

.corner-gif {
  position: fixed;
  bottom: 20px;
  z-index: 2;
}
</style> 