import os
from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base

from app.models import get_all_models


def execute_sql_file(file_path: str, conn) -> bool:
    """
    执行SQL文件
    :param file_path: SQL文件路径
    :param conn: 数据库连接
    :return: 是否执行成功
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_commands = [cmd.strip() for cmd in f.read().split(";") if cmd.strip()]

        for cmd in sql_commands:
            if cmd:
                conn.execute(text(cmd))
        conn.commit()
        return True

    except Exception as e:
        print(f"执行SQL文件 {file_path} 时出错：{str(e)}")
        raise


def init_db():
    """
    初始化数据库
    1. 检查并删除已存在的表
    2. 创建所有表
    3. 执行用户初始化SQL
    4. 执行其他初始化SQL
    """

    get_all_models()  # 通过调用此函数，显式导入所有的模型类，确保所有模型都已加载

    print(f"使用的数据库URL: {engine.url}")
    table_names = list(Base.metadata.tables.keys())
    print("准备创建的表：")
    for table_name in table_names:
        print(f"- {table_name}")

    # 检查并删除已存在的表
    with engine.connect() as conn:
        # 因为有外键约束，所以如果已经存在表的话，不按顺序删除会导致失败，因此设置不检查
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        for table_name in Base.metadata.tables.keys():
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                print(f"删除表 {table_name}")
            except Exception as e:
                print(f"删除表 {table_name} 时出错：{str(e)}")
        conn.commit()

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("所有表创建完成")

    try:
        # 获取SQL文件的绝对路径
        current_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        scripts_dir = os.path.join(current_dir, "scripts")

        with engine.connect() as conn:
            # 遍历 scripts 目录下的所有 .sql 文件
            for filename in os.listdir(scripts_dir):
                if filename.endswith(".sql"):
                    sql_path = os.path.join(scripts_dir, filename)
                    if execute_sql_file(sql_path, conn):
                        print(f"文件 {filename} 执行完成！")

        print("数据库初始化完成！")

    except Exception as e:
        print(f"初始化数据库时出错：{str(e)}")
        raise
