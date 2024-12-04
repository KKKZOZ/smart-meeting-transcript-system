from passlib.context import CryptContext
import json
import os

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    """生成密码的哈希值"""
    return pwd_context.hash(password)

def generate_sql_commands(users_data: list) -> str:
    """生成SQL插入命令"""
    sql_commands = ["-- 清空并重新创建用户表", "TRUNCATE TABLE users;\n"]
    
    for user in users_data:
        hashed_password = generate_password_hash(user["password"])
        sql = f"""-- 插入用户 (密码: {user["password"]})
INSERT INTO users (username, hashed_password, phone) VALUES 
('{user["username"]}', '{hashed_password}', '{user["phone"]}');
"""
        sql_commands.append(sql)
    
    return "\n".join(sql_commands)

def main():
    # 预设用户数据
    users = [
        {"username": "admin", "password": "admin123", "phone": "13800000000"},
        {"username": "test", "password": "test123", "phone": "13800000001"},
        {"username": "user1", "password": "test123", "phone": "13800000002"},
        {"username": "user2", "password": "test123", "phone": "13800000003"}
    ]
    
    # 生成SQL命令
    sql_content = generate_sql_commands(users)
    
    # 获取scripts目录的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 保存SQL文件
    sql_file_path = os.path.join(current_dir, 'init_users.sql')
    with open(sql_file_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    # 同时保存一个用户信息的JSON文件，方便查看
    users_file_path = os.path.join(current_dir, 'users.json')
    with open(users_file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    print("文件生成完成！")
    print(f"SQL文件已保存到: {sql_file_path}")
    print(f"用户信息已保存到: {users_file_path}")
    print("\n预设用户:")
    for user in users:
        print(f"- {user['username']} / {user['password']}")

if __name__ == "__main__":
    main() 