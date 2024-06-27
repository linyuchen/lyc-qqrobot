import hashlib
import random
import string


def generate_random_hash(length=8):
    # 生成一个随机字符串
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # 使用 SHA-256 算法生成哈希值
    hash_object = hashlib.sha256(random_string.encode())
    hash_hex = hash_object.hexdigest()

    # 返回指定长度的哈希值
    return hash_hex[:length]