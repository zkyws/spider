import math
import random
import base64
from Crypto.Cipher import AES
import codecs
import requests
class Func(object):
    @staticmethod
    def EncryptData(page):
        param1 = "{{rid:\"\", offset:\"{p}\", total:\"true\", limit:\"20\", csrf_token:\"\"}}".format(p=(page-1)*20)
        print(param1)
        param2 = "010001"
        param3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        param4 = "0CoJUm6Qyw8W8jud"

        # 返回两个参数的函数
        def asrses(p1, p2, p3, p4):
            data = {}
            temp = b(p1, p4)
            temp2 = a(16)
            data["params"] = b(temp, temp2)
            data["encSecKey"] = c(temp2, p2, p3)
            return data

        # 加密函数a   -----   随机生成16个字符
        def a(p1):
            string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            # 控制次数参数i
            i = 0
            # 初始化随机字符串
            random_strs = ""
            while i < p1:
                e = random.random() * len(string)
                # 向下取整
                e = math.floor(e)
                random_strs = random_strs + list(string)[e]
                i = i + 1
            return random_strs

        # 加密函数b    AES加密，加密模式为CBC，初始向量为iv
        def b(p1, p2):
            # 如果不是16的倍数则进行填充(paddiing)
            padding = 16 - len(p1) % 16
            msg = p1 + padding * chr(padding)
            # 用来加密或者解密的初始向量(必须是16位)
            iv = "0102030405060708"
            # 所有参数进行二进制编码，不然会报错，说str不能转为C
            iv = iv.encode("utf-8")
            p2 = p2.encode("utf-8")
            msg = msg.encode("utf-8")
            cipher = AES.new(p2, AES.MODE_CBC, iv)
            # 加密后得到的是bytes类型的数据
            encryptedbytes = cipher.encrypt(msg)
            # 使用Base64进行编码,返回byte字符串
            encodestrs = base64.b64encode(encryptedbytes)
            # 对byte字符串按utf-8进行解码
            enctext = encodestrs.decode('utf-8')
            return enctext

        # 加密函数c  RSA加密
        def c(p1, p2, p3):
            # 随机字符串逆序排列
            string = p1[::-1]
            # 将随机字符串转换成byte类型数据
            text = bytes(string, 'utf-8')
            seckey = int(codecs.encode(text, encoding='hex'), 16) ** int(p2, 16) % int(p3, 16)
            return format(seckey, 'x').zfill(256)

        # 返回
        return asrses(param1, param2, param3, param4)

# url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_1381755293?csrf_token="
# headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Language': 'en',
#         }
# yy = Func.EncryptData(252)
# x = requests.post(url=url,headers=headers,data=yy)
# print(x.text)