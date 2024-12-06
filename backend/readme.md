# 安装python后端依赖

## 创建并激活虚拟环境

+ Using `conda`

```bash
cd backend
# anaconda创建虚拟环境
conda create -n gjrg python=3.9

# 激活虚拟环境
conda activate gjrg

# 安装依赖包
pip install -r requirements.txt
```

+ Using `uv`

```bash
# 创建虚拟环境
uv venv --python 3.9

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖包
uv pip install -r requirements.txt
```

## 数据库初始化

0. 如果有 Docker，可以本地部署一个作为最基础的测试

```shell
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql
```


1. 首先在MySQL中创建数据库：

如果使用的是 Docker，可以使用以下命令直接创建数据库:

```shell
docker exec mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS meeting_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

```sql
CREATE DATABASE IF NOT EXISTS meeting_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

1. 修改.env文件中的数据库连接信息：

```
DATABASE_URL=mysql+pymysql://root:123456@localhost/meeting_system
```

3. 运行初始化脚本：

```bash
# Windows
python .\scripts\init_database.py

# Linux/MacOS
python ./scripts/init_database.py
```

初始化后会创建以下账号：

- 管理员账号：admin / admin123
- 测试账号：test / test123

## 运行应用

启动FastAPI应用：

```bash
# 开发模式启动（自动重载）
uvicorn main:app --reload --port 8000
# 生产模式启动
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 运行测试

```bash
# 运行所有测试
pytest tests/test_auth.py -v

# 或者直接运行测试文件
python tests/test_auth.py
```

# 开发方法

1. 在app/api/endpoints中创建对应功能的文件夹，文件夹应该包含一个router.py文件和__init__.py文件。
   在router.py文件中定义路由。在__init__.py文件中导入router.py中定义的路由。
   你可以定义多个路由文件。
2. 路由中需要调用的一些简单方法可以直接在其文件夹中定义，也可以移动至core文件夹中定义。
3. 路由中的输入参数使用Pydantic模型定义，定义在app/schemas文件夹中。
4. 数据库模型定义在app/models文件夹中，初始化数据库在app/db/init_db.py文件中。初始化过程不由主函数进行，而是通过脚本执行。init_db会先根据models创建数据表，然后执行文件夹内的sql文件
5. 在主函数中将路由进行注册
6. 在tests文件夹中编写test文件对特定路由进行测试
7. scripts文件夹存放一些工具脚本。

路由格式可以参考登录/注册的auth文件夹以及测试文件test_auth.py。
