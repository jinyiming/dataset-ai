<template>
  <div class="settings-page">
    <div class="settings-container">
      <div class="settings-header">
        <div class="header-content">
          <svg class="settings-icon" viewBox="0 0 24 24" fill="none">
            <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke="currentColor" stroke-width="2"/>
            <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <h1>系统设置</h1>
        </div>
      </div>

      <div class="settings-content">
        <div class="settings-section">
          <h3>问答模板设置</h3>
          <!-- 这里可以添加设置内容 -->
        </div>
      </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.settings-page {
  min-height: 100vh;
  background: #f9fafb;
  padding: 20px;
}

.settings-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.settings-header {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(to right, #10a37f, #34d399);
  border-radius: 12px 12px 0 0;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.settings-icon {
  width: 32px;
  height: 32px;
  color: white;
}

.settings-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.settings-content {
  padding: 24px;
}

.settings-section h3 {
  margin: 0 0 16px 0;
  font-size: 1.2rem;
  color: #374151;
}
</style> 