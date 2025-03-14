from flask import Flask, jsonify, request, session
from flask_cors import CORS
from database import db, r
from sqlalchemy import text
from models import User, m1  # 导入模型
from config import *  # 导入所有得属性
from flask.views import MethodView
from user import user_view
from datetime import timedelta


app = Flask(__name__)

# 配置转码
app.config["JSON_AS_ASCII"] = False

# 配置跨域
CORS(app, supports_credentials=True, origins="http://localhost")

# 配置mysql数据库
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{my_db}"  # 使用 SQLite 数据库
)
# 自动提交sql请求
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

#配置session的密钥
app.config["SECRET_KEY"] = "123"
#配置session的有效期
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=60*5)

# 初始化操作
db.init_app(app)

# 注册蓝图
app.register_blueprint(user_view)


# 类视图

# class BaseApi(MethodView):
#     def get_user(self):
#         print("该用户合法")

# class MangeApi(BaseApi):
#     def get(self):
#         id = request.args.get("id", None)
#         _sql = " select * from `user` where `id` = :id "
#         self.get_user()
#         # 原生 SQL 查询 (text() + db.session.execute):返回的结果通常是 元组 解决方法如下
#         columns = [
#             column[0]
#             for column in db.session.execute(text(_sql), {"id": 1}).cursor.description
#         ]
#         result = db.session.execute(text(_sql), {"id": 1}).fetchone()
#         if result:
#             user_data = dict(zip(columns, result))
#             print(user_data)
#             return jsonify({"code": 400, "data": user_data})
#         else:
#             return jsonify({"code": 400, "msg": "查询的内容不存在"})

# app.add_url_rule("/", view_func=MangeApi.as_view("MangeApi"))

# 插入
# @app.route("/insert", methods=["POST"])
# def insert_into():
#     email = request.form.get("email", None)
#     password = request.form.get("password", None)
#     _sql = f" insert into `user` (`email`,`password`) values ('{email}','{password}')"
#     print(_sql)
#     db.session.execute(text(_sql))
#     db.session.commit()
#     return jsonify({"msg": "成功"})

# 修改
# @app.route("/modify", methods=["PUT"])
# def modify():
# 修改update 表名 set 字段 where 检索条件
# email = request.form.get("email", None)
# password = request.form.get("password", None)
# _sql = "update `user` set password = :password where `email` = :email"
# db.session.execute(text(_sql), {"password": password, "email": email})
# db.session.commit()
# return jsonify({"msg": "修改成功"})


# 删除
# @app.route("/delete/<email>", methods=["DELETE"])
# def delete_into(email):
#     # email = request.args.get("email", None)
#     # 删除 delete from 表名 where 检索条件
#     _sql = " delete from user where `email` = :email "
#     db.session.execute(text(_sql), {"email": email})
#     db.session.commit()
#     return jsonify({"msg": "删除成功"})


# 配置路由
@app.route("/", methods=["GET"])
def index():
    # 获取接口参数
    # id = request.args.get("id", None)
    # print(f"请求的参数{id}")

    # # 创建一个新的 User 实例
    # new_user = User(email="john@example.com", password="4444")

    # # 将新用户添加到会话
    # db.session.add(new_user)

    # # 提交事务
    # db.session.commit()
    # 修改数据
    # user = User.query.get(2)
    # user.email = "1047708823"
    # db.session.commit()
    # db.session.execute(text("update user set password = '5555' where id = 2"))
    # db.session.commit()

    # redis操作
    # r.set("123", "123")
    # print(r.get("123"))

    # 查询数据库
    # users = User.query.all()
    # 返回 JSON 数据

    session["code"] = "123"
    code = session.get("code", None)
    return jsonify(
        {
            "data": [
                {"session": code, "msg": "成功"},
            ]
        }
    )


if __name__ == "__main__":
    # debug 调试模式
    app.run(debug=True, host="0.0.0.0", port="5000")
# 数据库操作
# 增加 insert into(字段) values(值)
# 删除 delete from 表名 where 检索条件
# 修改update 表名 set 字段 where 检索条件
# 查询select*from 表名 where 检索条件
