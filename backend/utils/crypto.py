from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json

# 使用与前端相同的16字节密钥
SECRET_KEY = b'ABCDEF0123456789'

def decrypt_data(encrypted_data):
    try:
        # Base64解码
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # 创建AES-ECB模式的cipher
        cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
        
        # 解密并去除填充
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        
        # 转换为字符串并解析JSON
        decrypted_str = decrypted_bytes.decode('utf-8')
        return json.loads(decrypted_str)
    except Exception as e:
        print(f"解密失败: {e}")
        print(f"加密数据: {encrypted_data}")
        return None 