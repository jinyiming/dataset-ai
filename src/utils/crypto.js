import CryptoJS from 'crypto-js'

// 使用固定的16字节密钥
const SECRET_KEY = 'ABCDEF0123456789'

export const encrypt = (data) => {
  try {
    // 将数据转换为JSON字符串
    const jsonStr = JSON.stringify(data)
    
    // 使用AES-ECB模式加密
    const encrypted = CryptoJS.AES.encrypt(jsonStr, SECRET_KEY, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7
    })
    
    // 返回Base64编码的密文
    return encrypted.toString()
  } catch (error) {
    console.error('加密失败:', error)
    return null
  }
}

export const decrypt = (encryptedData) => {
  try {
    // AES 解密
    const bytes = CryptoJS.AES.decrypt(encryptedData, SECRET_KEY)
    const decrypted = bytes.toString(CryptoJS.enc.Utf8)
    return JSON.parse(decrypted)
  } catch (error) {
    console.error('解密失败:', error)
    return null
  }
} 