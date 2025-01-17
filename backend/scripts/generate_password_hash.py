from passlib.context import CryptContext
import os
import random
import string

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    """生成密码的哈希值"""
    return pwd_context.hash(password)


def generate_sql_commands(users_data: list) -> str:
    """生成SQL插入命令"""
    sql_commands = ["-- 清空并重新创建用户表", "TRUNCATE TABLE users;\n"]

    for index, user in enumerate(users_data):
        hashed_password = generate_password_hash(user["password"])
        sql = f"""-- 插入用户 (密码: {user["password"]})
INSERT INTO users (user_id,username, hashed_password, email,nickname,notification_type,enabled,root) VALUES 
('{index + 1}','{user["username"]}', '{hashed_password}', '{user["email"]}', '{user["nickname"]}',1,1,{1 if "root" in user["username"] else 0});
"""
        sql_commands.append(sql)

    return "\n".join(sql_commands)


def generate_user_id() -> str:
    ## 使用15位随机字符串作为用户ID
    return "".join(random.choices(string.ascii_letters + string.digits, k=15))


def main():
    # 预设用户数据
    users = [
        {
            "username": "root",
            "password": "root123",
            "email": "root@example.com",
            "nickname": "超级管理员",
        },
        {
            "username": "admin",
            "password": "admin123",
            "email": "admin@example.com",
            "nickname": "张经理",
        },
        {
            "username": "test",
            "password": "test123",
            "email": "test@example.com",
            "nickname": "李主管",
        },
        {
            "username": "user1",
            "password": "test123",
            "email": "user1@example.com",
            "nickname": "王专员",
        },
        {
            "username": "user2",
            "password": "test123",
            "email": "user2@example.com",
            "nickname": "赵助理",
        },
        {
            "username": "liujinyi",
            "password": "liujinyi",
            "email": "kkkzoz@qq.com",
            "nickname": "刘分析师",
        },
    ]

    # 生成SQL命令
    sql_content = generate_sql_commands(users)

    # 获取scripts目录的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 保存SQL文件
    sql_file_path = os.path.join(current_dir, "init_users.sql")
    with open(sql_file_path, "w", encoding="utf-8") as f:
        f.write(sql_content)

    print("文件生成完成！")
    print(f"SQL文件已保存到: {sql_file_path}")
    print("\n预设用户:")
    for user in users:
        print(f"- {user['username']} / {user['password']}")


if __name__ == "__main__":
    main()
