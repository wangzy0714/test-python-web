# 通过上下文管理进行封装，达到自动关闭数据库连接的效果
import redis
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
import pymysql
from config import *  # 导入所有得属性

# 通过pymsql模拟mysqldb
pymysql.install_as_MySQLdb()

# 实例化连接对象
engine = create_engine(
    f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{my_db}"
)
# 创建游标对象
Session = sessionmaker(bind=engine)


class R:
    def __enter__(self):
        self.r = redis.Redis(decode_responses=True)
        return self.r
        # 关闭数据库连接

    def __exit__(self, *args):
        self.r.close()


if __name__ == "__main__":
    with Session() as db:
        res = db.execute(text("select * FROM user")).fetchall()
    print(res)
