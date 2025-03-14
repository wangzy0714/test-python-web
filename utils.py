# 工具库
import smtplib

# 用于创建 纯文本 或 HTML 格式 的邮件正文。
from email.mime.text import MIMEText

# 允许邮件包含多个部分（文本、图片、附件）
from email.mime.multipart import MIMEMultipart
import string
import random
from database import r
from flask import session
import datetime


# 正则模块
import re

# 导入哈希算法
import hashlib

# 导入图片绘制库
from PIL import ImageDraw, Image, ImageFont

# 导入jwt库
import jwt


class MyJwT:
    def __init__(self):
        # 密钥
        self.secret = "1234"

    # 加入生命周期的加密方法
    def encode_time(self, userInfo, lifetime=300):
        payload = {
            "exp": int(  # 转换为整数时间戳
                (datetime.datetime.now() + datetime.timedelta(seconds=lifetime)).timestamp()
            ),
            "data": userInfo,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    # 加密方法
    def encode(self, userInfo):
        res = jwt.encode(userInfo, self.secret, algorithm="HS256")
        return res

    # 解密方法
    def decode(self, jwt_str):
        res = jwt.decode(jwt_str, self.secret, algorithms=["HS256"])
        return res


# md5加密算法
def make_password(psw):
    # 生成md5对象
    md5 = hashlib.md5()
    # 生成签名
    sign_utf8 = str(psw).encode(encoding="utf-8")
    # 加密
    md5.update(sign_utf8)
    # 返回32位密文
    return md5.hexdigest()


# 验证邮箱
def is_valid_email(email):
    # 生成正则
    ex_email = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    res = ex_email.match(email)
    return res


# 发送邮件
class SendEmail:
    def __init__(self):
        self.EMAIL_USER = "1047708823@qq.com"  # 发送人邮箱

        self.EMAIL_PASS = "zjeunnvmhsgxbfhh"  # 发送人授权码

    def send_mail(self, _touser, _title, _content):

        # 构建邮件体
        msg = MIMEMultipart()

        # 邮件标题
        msg["Subject"] = _title

        # 发件人
        msg["From"] = self.EMAIL_USER

        # 收件人
        msg["to"] = _touser

        # 构建内容
        part = MIMEText(f"您的验证码为：{_content}", "html", "utf-8")
        msg.attach(part)

        # 发送逻辑
        # 建立连接
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)

        # 登录邮箱
        s.login(self.EMAIL_USER, self.EMAIL_PASS)
        # 发送邮件
        s.sendmail(self.EMAIL_USER, _touser, msg.as_string())

        # 关闭链接
        s.close()


# 随机码
def random_string(length=4):
    str = string.ascii_letters + string.digits
    return "".join(random.choices(str, k=length))


# 随机码存储
def save_code(email, code, lifetime=300):
    # r.set(email, code)
    # 设置生命周期
    # r.expire(email, lifetime)

    # 原子性操作 存储+设置生命周期
    return r.setex(email, lifetime, code)


# 随机码存储 session
def save_code_session(email, code):
    session[email] = code


# 绘图类
class DrawCode:
    img_size = (130, 70)

    # 静态方法
    @staticmethod
    def image_code_valid(email, code):
        # 从redis中获取验证码
        redis_code = r.get(email + "_img")
        if not redis_code:
            return False
        elif redis_code != code:
            return False
        else:
            return True

    # 类方法
    @classmethod
    def draw_code(cls):
        # 创建画布
        img = Image.new("RGB", cls.img_size, "white")
        try:
            font = ImageFont.truetype("fonts/arial.ttf", 36)  # 使用更大的字号
        except IOError:
            font = ImageFont.load_default()  # 回退到默认字体
        # 创建画笔
        draw = ImageDraw.Draw(img)
        # 生成随机验证码
        code = random_string()
        # 绘制文字
        x = 10
        for char in code:
            y_offset = random.randint(-5, 5)
            draw.text((x, 15 + y_offset), char, fill=(0, 0, 0), font=font)
            x += 30
        return {"code": code, "img": img}


if __name__ == "__main__":
 res =   make_password(123)
 print(res)
