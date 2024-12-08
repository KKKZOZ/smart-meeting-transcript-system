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

1. 在本地部署数据库:

> 如果有 Docker，可以直接用下面的命令部署一个 MySQL 数据库
>
> ```shell
> docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql
> ```

2. 首先在MySQL中创建数据库:

> 如果使用的是 Docker，也可以使用以下命令创建数据库 `meeting_system`:
>
> ```shell
> docker exec mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS meeting_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
> ```

```sql
CREATE DATABASE IF NOT EXISTS meeting_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 修改 `.env` 文件中的数据库连接信息：

```
DATABASE_URL=mysql+pymysql://root:123456@localhost/meeting_system
```

4. 运行初始化脚本：

```bash
# Windows
python .\scripts\init_database.py

# Linux/MacOS
python ./scripts/init_database.py
```

初始化后会创建以下账号：

+ 管理员账号：admin / admin123
+ 测试账号：test / test123

## 运行应用

启动 FastAPI 应用：

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

1. 在 `app/api/endpoints` 中创建对应功能的文件夹，文件夹应该包含一个 `router.py` 文件和 `__init__.py` 文件。在 `router.py` 文件中定义路由。在 `__init__.py` 文件中导入 `router.py` 中定义的路由
2. 路由中需要调用的一些简单方法可以直接在其文件夹中定义，也可以移动至 `core` 文件夹中定义
3. 路由中的输入参数使用 `Pydantic` 模型定义，定义在 `app/schemas` 文件夹中
4. 数据库模型定义在 `app/models` 文件夹中，初始化数据库在 `app/db/init_db.py` 文件中。初始化过程不由主函数进行，而是通过脚本执行。`init_db` 会先根据 `models` 创建数据表，然后执行文件夹内的sql文件
5. 在主函数中将路由进行注册
6. 在`tests`文件夹中编写 test 文件对特定路由进行测试
7. `scripts` 文件夹存放一些工具脚本

路由格式可以参考登录/注册的 auth 文件夹以及测试文件 `test_auth.py`
