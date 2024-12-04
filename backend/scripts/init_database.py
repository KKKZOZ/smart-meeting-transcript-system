import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.init_db import init_db

if __name__ == "__main__":
    print("开始初始化数据库...")
    init_db() 