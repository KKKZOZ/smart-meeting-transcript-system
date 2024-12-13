# app/models/__init__.py
from app.models.user import User
from app.models.meeting import Meeting, MeetingParticipants
from app.models.demo_item import DemoItem
from app.models.notifications import Notification
from app.models.tasks import Task
from app.models.transcriptions import Transcription
from app.models.summaries import Summary


def get_all_models():
    """
    导入所有模型类
    这个函数确保所有模型都被正确加载到 SQLAlchemy 的 metadata 中
    """
    return [
        User,
        Meeting,
        MeetingParticipants,
        DemoItem,
        Notification,
        Task,
        Transcription,
        Summary,
    ]  # 返回所有模型类
