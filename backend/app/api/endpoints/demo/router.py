from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.demo_item import DemoItem
from app.schemas.demo_item import DemoItemCreate, DemoItemUpdate, DemoItemResponse

router = APIRouter()


@router.post("/demo", response_model=DemoItemResponse)
async def create_demo_item(item_in: DemoItemCreate, db: Session = Depends(get_db)):
    """创建演示项"""
    # 检查指定 id 是否已存在
    exists = db.query(DemoItem).filter(DemoItem.id == item_in.id).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"ID {item_in.id} 已存在"
        )

    demo_item = DemoItem(id=item_in.id, value=item_in.value)
    db.add(demo_item)
    db.commit()
    db.refresh(demo_item)
    return demo_item


@router.get("/demo/{item_id}", response_model=DemoItemResponse)
async def read_demo_item(item_id: int, db: Session = Depends(get_db)):
    """获取单个演示项"""
    demo_item = db.query(DemoItem).filter(DemoItem.id == item_id).first()
    if not demo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="演示项不存在"
        )
    return demo_item


@router.get("/demo", response_model=List[DemoItemResponse])
async def read_demo_items(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """获取演示项列表"""
    demo_items = db.query(DemoItem).offset(skip).limit(limit).all()
    return demo_items


@router.put("/demo/{item_id}", response_model=DemoItemResponse)
async def update_demo_item(
    item_id: int, item_in: DemoItemUpdate, db: Session = Depends(get_db)
):
    """更新演示项"""
    demo_item = db.query(DemoItem).filter(DemoItem.id == item_id).first()
    if not demo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="演示项不存在"
        )

    if item_in.value is not None:
        demo_item.value = item_in.value

    db.commit()
    db.refresh(demo_item)
    return demo_item


@router.delete("/demo/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_demo_item(item_id: int, db: Session = Depends(get_db)):
    """删除演示项"""
    demo_item = db.query(DemoItem).filter(DemoItem.id == item_id).first()
    if not demo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="演示项不存在"
        )

    db.delete(demo_item)
    db.commit()
    return None
