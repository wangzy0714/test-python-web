from database import db
from datetime import datetime  # 导入 datetime 模块


class User(db.Model):
    # 指定表名（必须与数据库中的实际表名一致）
    __tablename__ = "user"

    # 定义列（字段名、类型、约束需与表一致）
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 可选：添加关系或自定义方法
    def __repr__(self):
        return f"<User {self.email}>"
