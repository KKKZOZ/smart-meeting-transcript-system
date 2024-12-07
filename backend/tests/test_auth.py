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

def test_login_success():
    """测试正常登录"""
    response = requests.post(
        f"{BASE_URL}/api/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_endpoint():
    """测试需要token验证的接口"""
    # 1. 先登录获取token
    login_response = requests.post(
        f"{BASE_URL}/api/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 2. 使用token请求受保护的接口
    headers = {
        "Authorization": f"Bearer {token}"
    }
    test_response = requests.get(
        f"{BASE_URL}/api/test",
        headers=headers
    )
    
    # 3. 验证响应
    assert test_response.status_code == 200
    data = test_response.json()
    assert data["msg"] == "test success"
    assert data["user"] == "admin"  # 验证返回的用户名是否正确

if __name__ == "__main__":
    # test_register_success()
    test_protected_endpoint()
    print("测试完成！")
