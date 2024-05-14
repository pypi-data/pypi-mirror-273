import hmac
import uuid
import hashlib


# 实现HmacSHA1加密
def hmac_sha1(key, data):
    # return hmac.new(key.encode(), data.encode(), 'sha1').hexdigest()
    key_bytes = bytes(key, 'utf-8')
    message_bytes = bytes(data, 'utf-8')

    # 创建新的 hmac 对象，指定 key 和 SHA1 算法
    hmac_object = hmac.new(key_bytes, message_bytes, hashlib.sha1)

    # 获取 HMAC 结果的十六进制表示
    hmac_hex = hmac_object.hexdigest()

    return hmac_hex


# 获取机器码
def get_machine_code():
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return mac_address
