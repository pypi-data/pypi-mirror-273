import base64
from Crypto.Cipher import AES
from gmssl import sm4


class AesUtil:
    """
    AES加解密
    """

    @staticmethod
    def encrypt_cbc(key, iv, plaintext):
        """
        加密
        :param key: 密钥
        :param iv: 偏移向量
        :param plaintext: 明文
        :return: base64字符串
        """
        # 字符串补位
        data = AesUtil.__pad(plaintext)
        # 初始化加密器
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
        # 加密后得到的是bytes类型的数据
        encrypt_bytes = cipher.encrypt(data.encode('utf8'))
        # 使用Base64进行编码,返回byte字符串
        encode_strs = base64.b64encode(encrypt_bytes)
        # 对byte字符串按utf-8进行解码
        ciphertext = encode_strs.decode('utf8')
        return ciphertext

    @staticmethod
    def decrypt_cbc(key, iv, ciphertext):
        """
        解密
        :param key: 密钥
        :param iv: 偏移向量
        :param ciphertext: base64加密串
        :return: 解密后字符串
        """
        # 对字符串按utf-8进行编码
        data = ciphertext.encode('utf8')
        # 将加密数据转换位bytes类型数据
        decode_bytes = base64.decodebytes(data)
        # 初始化加密器
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
        # 解密
        text_decrypted = cipher.decrypt(decode_bytes)
        # 去补位
        text_decrypted = AesUtil.__un_pad(text_decrypted)
        # 对byte字符串按utf-8进行解码
        plaintext = text_decrypted.decode('utf8')
        return plaintext

    @staticmethod
    def __pad(s):
        """
        字符串补位
        :param s: 待处理字符串
        :return:
        """
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    @staticmethod
    def __un_pad(s):
        """
        去掉字符串最后一个字符
        :param s: 待处理字符串
        :return:
        """
        return s[0:-s[-1]]


class Sm4Util:
    """
    SM4加解密
    """

    @staticmethod
    def encrypt_ecb(key, plaintext):
        """
        加密
        :param key: 密钥
        :param plaintext: 明文
        :return: base64加密串
        """
        sm4_alg = sm4.CryptSM4()  # 实例化sm4
        sm4_alg.set_key(key.encode(), sm4.SM4_ENCRYPT)  # 设置密钥
        datastr = str(plaintext)
        res = sm4_alg.crypt_ecb(datastr.encode('utf8'))  # 开始加密,bytes类型，ecb模式
        # 加密后得到的是bytes类型的数据
        encode_strs = base64.b64encode(res)
        # 使用Base64进行编码,返回byte字符串
        ciphertext = encode_strs.decode('utf8')
        return ciphertext  # 返回加密串

    @staticmethod
    def decrypt_ecb(key, ciphertext):
        """
        解密
        :param key: 密钥
        :param ciphertext: base64加密串
        :return: 明文
        """
        ciphertext = ciphertext.encode('utf8')
        encode_bytes = base64.decodebytes(ciphertext)
        sm4_alg = sm4.CryptSM4()  # 实例化sm4
        sm4_alg.set_key(key.encode(), sm4.SM4_DECRYPT)  # 设置密钥
        res = sm4_alg.crypt_ecb(encode_bytes)  # 开始解密。十六进制类型,ecb模式
        plaintext = res.decode('utf8')
        return plaintext


if __name__ == '__main__':
    text = "123"
    print()
    aes_key = "91a055ac42b41132"
    aes_iv = "b5a836c453b982a2"
    aes_ciphertext = AesUtil.encrypt_cbc(aes_key, aes_iv, text)
    print("AES加密后===", aes_ciphertext)
    aes_plaintext = AesUtil.decrypt_cbc(aes_key, aes_iv, aes_ciphertext)
    print("AES解密后===", aes_plaintext)

    sm4_key = "86C63180C2806ED1"
    sm4_ciphertext = Sm4Util.encrypt_ecb(sm4_key, text)
    print("SM4加密后===", sm4_ciphertext)
    sm4_plaintext = Sm4Util.decrypt_ecb(sm4_key, sm4_ciphertext)
    print("SM4解密后===", sm4_plaintext)
