import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import get_password_hash
from app.models.user import User
from app.db.session import engine, SessionLocal
from app.db.base import Base

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
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_commands = [cmd.strip() for cmd in f.read().split(';') if cmd.strip()]
        
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
    1. 创建所有表
    2. 执行用户初始化SQL
    3. 执行其他初始化SQL
    """
    print(f"使用的数据库URL: {engine.url}")
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    try:
        # 获取SQL文件的绝对路径
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scripts_dir = os.path.join(current_dir, 'scripts')
        
        with engine.connect() as conn:
            # 执行用户初始化SQL
            user_sql_path = os.path.join(scripts_dir, 'init_users.sql')
            if execute_sql_file(user_sql_path, conn):
                print("用户初始化完成！")
            
            # 执行其他初始化SQL
            init_sql_path = os.path.join(scripts_dir, 'init.sql')
            if execute_sql_file(init_sql_path, conn):
                print("其他初始化完成！")
            
        print("数据库初始化完成！")
            
    except Exception as e:
        print(f"初始化数据库时出错：{str(e)}")
        raise