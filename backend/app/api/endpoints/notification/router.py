from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/test")
async def test():
    return {"msg": "test success"}
