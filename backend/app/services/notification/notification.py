from sqlalchemy.orm import Session
from app.models.notifications import Notification, NotificationStatus
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)
from typing import List, Optional
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_notification_email(notification: Notification, recipient_email: str) -> bool:
    """
    发送通知邮件

    Args:
        notification: Notification 实例
        recipient_email: 接收者邮箱地址

    Returns:
        bool: 发送是否成功
    """

    # 163邮箱配置
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD

    if not all([smtp_server, smtp_port, sender_email, sender_password]):
        raise ValueError("Missing email configuration in environment variables")

    # 创建邮件内容
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "新通知提醒"

    # 构建邮件正文
    body = f"""
    您有一个新的通知：
    
    内容：{notification.content}
    
    截止时间：{notification.ddl.strftime("%Y-%m-%d %H:%M:%S")}
    
    状态：{notification.status.value}
    
    通知ID：{notification.notification_id}
    任务ID：{notification.task_id}
    
    请及时查看和处理！
    """

    msg.attach(MIMEText(body, "plain", "utf-8"))  # 指定编码为utf-8

    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls()  # 启用TLS加密

        # 登录
        server.login(sender_email, sender_password)

        # 发送邮件
        server.send_message(msg)

        # 关闭连接
        server.quit()

        return True
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        return False


def create_notification(
    db: Session, notification_in: NotificationCreate, user_id: str
) -> Notification:
    """创建通知"""
    new_notification = Notification(
        notification_id=str(uuid.uuid4()),
        user_id=user_id,
        meeting_id=notification_in.meeting_id,
        task_id=notification_in.task_id,
        content=notification_in.content,
        ddl=notification_in.ddl,
        status=NotificationStatus.UNREAD,
    )

    user = db.query(User).filter(User.user_id == user_id).first()
    print(f"User: {user}")

    try:
        # 发送邮件通知
        send_notification_email(new_notification, user.email)
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def get_notification(db: Session, notification_id: str) -> Optional[Notification]:
    """获取单个通知"""
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    print(db_notification)
    return db_notification


def get_notifications(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Notification]:
    """获取通知列表"""
    return db.query(Notification).offset(skip).limit(limit).all()


def update_notification(
    db: Session, notification_id: str, notification_in: NotificationUpdate
) -> Optional[Notification]:
    """更新通知"""
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    if not db_notification:
        return None

    if notification_in.content is not None:
        db_notification.content = notification_in.content
    if notification_in.ddl is not None:
        db_notification.ddl = notification_in.ddl
    if notification_in.status is not None:
        db_notification.status = notification_in.status

    db.commit()
    db.refresh(db_notification)
    return db_notification


def delete_notification(db: Session, notification_id: str) -> bool:
    """删除通知"""
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    if not db_notification:
        return False

    db.delete(db_notification)
    db.commit()
    return True


def update_notification_status(
    db: Session, notification_id: str, status: NotificationStatus
) -> Optional[Notification]:
    """根据 notification_id 修改通知已读/未读状态"""
    print(notification_id)
    print(
        db.query(Notification).filter(Notification.notification_id == notification_id)
    )
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    # print("in function" + db_notification)
    # if not db_notification:
    #     print("Will return None")
    if not db_notification:
        return None

    db_notification.status = status
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_notifications_by_user_id(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
) -> List[Notification]:
    """根据 user_id 获取通知列表"""
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_notifications_by_task_id(
    db: Session, task_id: str, skip: int = 0, limit: int = 100
) -> List[Notification]:
    """根据 task_id 获取通知列表"""
    return (
        db.query(Notification)
        .filter(Notification.task_id == task_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
