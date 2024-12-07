from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/test")
async def test(current_user: User = Depends(get_current_user)):
    """
    测试接口（需要token验证）
    """
    return {"msg": "test success", "user": current_user.username}
