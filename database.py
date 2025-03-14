# 数据库实例文件
from flask_sqlalchemy import SQLAlchemy
import pymysql
import redis

# 通过pymsql模拟mysqldb
pymysql.install_as_MySQLdb()
conn = pymysql.connect(
    host="localhost", user="root", password="123456", db="social", port=3306
)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 实例化mysql对象
db = SQLAlchemy()

# 实例化redis对象
r = redis.Redis(decode_responses=True)
