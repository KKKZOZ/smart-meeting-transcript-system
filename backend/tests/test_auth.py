import requests

# 服务器地址
BASE_URL = "http://localhost:8000"

def test_register_success():
    """测试正常注册"""
    response = requests.post(
        f"{BASE_URL}/api/register",
        json={
            "username": "testuser",
            "password": "testpass",
            "phone": "13800138000"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_duplicate_username():
    """测试重复用户名注册"""
    # 先注册一个用户
    requests.post(
        f"{BASE_URL}/api/register",
        json={
            "username": "user1",
            "password": "testpass",
            "phone": "13800138001"
        }
    )
    
    # 尝试使用相同用户名注册
    response = requests.post(
        f"{BASE_URL}/api/register",
        json={
            "username": "user1",
            "password": "testpass",
            "phone": "13800138002"
        }
    )
    assert response.status_code == 400
    assert "用户名已存在" in response.json()["detail"]

def test_login_success():
    """测试正常登录"""
    response = requests.post(
        f"{BASE_URL}/api/login",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    """测试密码错误"""
    response = requests.post(
        f"{BASE_URL}/api/login",
        data={
            "username": "admin",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    
    
if __name__ == "__main__":
    # test_register_success();
    test_login_success()
    test_login_wrong_password()
    print("测试完成！")
