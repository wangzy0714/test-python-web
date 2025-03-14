from flask import Blueprint, request, jsonify
from database import db, r
from config import *  # 导入所有得属性
from flask.views import MethodView
from utils import (
    is_valid_email,
    random_string,
    SendEmail,
    save_code,
    make_password,
    DrawCode,
    MyJwT,
)
from sqlalchemy import text
from models import User, m1  # 导入模型


# 导入文件流库
import io

# 导入flask输出组件
from flask import make_response

import random

# 用户蓝图
user_view = Blueprint("user_view", __name__)


# 图像验证码接口
class CaptchaApi(MethodView):
    def get(self):

        email = request.args.get("email", None)
        if not email:
            return jsonify({"code": 400, "msg": "请输入邮箱"})
        # 生成图片验证码
        draw_code = DrawCode.draw_code()
        # 存储到redis
        r.setex(email + "_img", 300, draw_code["code"])
        # 将图像保存到字节流
        buf = io.BytesIO()
        draw_code["img"].save(buf, format="PNG")
        # 定制化返回值
        response = make_response(buf.getvalue())
        response.headers["Content-Type"] = "image/png"

        return response


user_view.add_url_rule("/captcha", view_func=CaptchaApi.as_view("CaptchaApi"))


# 发送验证码
class SendCodeApi(MethodView):
    def get(self):
        email = request.args.get("email", None)
        if not email:
            return jsonify({"code": 400, "msg": "请输入邮箱"})
        if not is_valid_email(email):
            return jsonify({"code": 400, "msg": "邮箱不合法"})

        # 获取计数器并检查发送次数
        count_key = f"{email}_count"
        count = r.get(count_key)
        if count and int(count) > 3:
            return jsonify({"code": 400, "msg": "验证码发送次数过多"})

        # 检查是否已发送验证码
        if r.get(email):
            return jsonify({"code": 400, "msg": "验证码已发送"})

        # 生成验证码并发送邮件
        code = random_string()
        sm = SendEmail()
        try:
            sm.send_mail(email, "python项目验证码", code)
        except Exception as e:
            # 假设有 logging 模块记录异常
            logging.error(f"邮件发送失败: {e}")
            return jsonify({"code": 400, "msg": "邮件发送失败"})

        # 保存验证码并更新计数器
        if save_code(email, code):
            r.incr(count_key) if count else r.set(count_key, 1)
            return jsonify({"code": 200, "msg": "验证码已发送"})
        else:
            return jsonify({"code": 400, "msg": "邮件发送失败"})


user_view.add_url_rule("/sendcode", view_func=SendCodeApi.as_view("SendCodeApi"))


# 注册和登录
class UserApi(MethodView):
    def get(self):
        email = request.args.get("email")
        password = request.args.get("password")
        if not email:
            return jsonify({"code": 400, "msg": "请输入邮箱"})
        if not password:
            return jsonify({"code": 400, "msg": "请输入密码"})
        # 查询黑名单
        if r.get(email + "_black"):
            return jsonify({"code": 400, "msg": "账号已锁定30分钟"})
        user = (
            db.session.query(User)
            .filter(User.email == email, User.password == make_password(password))
            .first()
        )

        if user:
            mj = MyJwT()
            jwt_str = mj.encode({"id": user.id})
            return jsonify(
                {
                    "code": 200,
                    "msg": "登录成功",
                    "token": jwt_str,
                    "userInfo": user.email,
                }
            )
        else:
            # 验证失败，返回错误信息
            attempts = r.get(email)
            if attempts:
                if int(attempts) >= 3:
                    r.setex(email + "_black", 1800, 1)
                    return jsonify({"code": 400, "msg": "账号已锁定30分钟"})
                else:
                    r.incr(email)
            else:
                r.setex(email, 300, 1)
            return jsonify({"code": 400, "msg": "用户名或密码错误"})

    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        code = data.get("code")
        redis_code = r.get(email)
        # print(code, redis_code)
        if code.lower() == redis_code.lower():
            # _sql = f"insert into `user` (`email`,`password`) values ('{email}','{make_password(password)}') "
            new_user = User(email=email, password=make_password(password))
            try:
                db.session.add(new_user)
                # db.session.execute(text(_sql))
                db.session.commit()
                return jsonify({"code": 200, "msg": "注册成功"})
            except Exception as e:
                return jsonify({"code": 400, "msg": "邮箱已经注册"})

        else:
            return jsonify({"code": 400, "msg": "验证码不正确"})


user_view.add_url_rule("/user", view_func=UserApi.as_view("UserApi"))
