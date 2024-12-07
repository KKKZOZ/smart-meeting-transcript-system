# app/models/__init__.py
from app.models.user import User
from app.models.demo_item import DemoItem


def get_all_models():
    return [User, DemoItem]
