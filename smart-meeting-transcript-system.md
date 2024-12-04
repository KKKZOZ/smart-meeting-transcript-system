# 智能会议记录系统





## 关系模型

+ 整个系统中有多个会议
+  一个会议可以有多个参与者
+  一个会议有 **多** 条转录记录
+  一个会议可以生成 **多** 个摘要
+  一个会议可以产生多个任务
+  一个用户可以收到多个通知
+  一个用户可以有一个通知设置



1. 用户表

```sql
CREATE TABLE Users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
);
```



2. 会议表

```sql
CREATE TABLE Meetings (
    meeting_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    creator_id VARCHAR(50) REFERENCES Users(user_id),
);
```



3. 会议参与者表

```sql
CREATE TABLE Meeting_Participants (
    meeting_id VARCHAR(50) REFERENCES Meetings(meeting_id),
    user_id VARCHAR(50) REFERENCES Users(user_id),
  	participant_id VARCHAR(50)
    ## role VARCHAR(20), -- 主持人/参与者
    PRIMARY KEY (meeting_id, user_id)
);
```



4. 转录记录表

```sql
CREATE TABLE Transcriptions (
    meeting_id VARCHAR(50) PRIMARY KEY REFERENCES Meetings(meeting_id),
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    language VARCHAR(10)
);
```



5. 会议摘要表

```sql
CREATE TABLE Summaries (
    meeting_id VARCHAR(50) PRIMARY KEY REFERENCES Meetings(meeting_id),
    content TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);
```



6. 任务表

```sql
CREATE TABLE Tasks (
    task_id VARCHAR(50) PRIMARY KEY,
    meeting_id VARCHAR(50) REFERENCES Meetings(meeting_id),
    description TEXT NOT NULL,
    assignee_id VARCHAR(50) REFERENCES Users(user_id),
    due_date DATE,
    status VARCHAR(20), -- 待处理/进行中/已完成
);
```



7. 通知表

```sql
CREATE TABLE Notifications (
    notification_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES Users(user_id),
    task_id VARCHAR(50) REFERENCES Tasks(task_id),
    content TEXT NOT NULL,
  	ddl TIMESTAMP,
    status VARCHAR(20), -- 未读/已读
);
```



8. 用户通知设置表

```sql
CREATE TABLE Notification_Settings (
    user_id VARCHAR(50) PRIMARY KEY REFERENCES Users(user_id),
    notification_type VARCHAR(20),
    frequency VARCHAR(20), -- 立即/每日/每周
    enabled BOOLEAN DEFAULT true
);
```



## API

### 协作与通知模块

#### HTTP API

1. 通知设置管理

```json
GET /api/notification/settings
描述：获取当前用户的通知设置
响应：
{
  	"code": 200,
    "message": "success",
    "data": {
        "frequency": "immediate",    // immediate/daily/weekly
        "email_enabled": true,
        "in_app_enabled": true
    }
}
```

```json
PUT /api/notification/settings
描述：更新用户的通知设置
请求体：
{
    "frequency": "immediate",
    "email_enabled": true,
    "in_app_enabled": true
}
响应：
{
    "code": "200",
    "message": "Notification settings updated successfully"
}
```

2. 通知管理

```json
GET /api/notifications
描述：获取用户的通知列表
查询参数：
    - status: 通知状态(unread/read/all)
响应：
{
  	“code”: 200,
    "message": "success",
    "data": {
        "notifications": [
            {
                "notification_id": "xxx",
                "type": "task",
                "content": "您被分配了新任务：准备周会报告",
                "created_at": "2024-12-04T10:00:00Z",
                "status": "unread",
                "task_id": "xxx"
            }
        ],
        "total": 100,
        "unread_count": 5
    }
}
```

```json
PUT /api/notifications/{notification_id}/read
描述：将通知标记为已读
响应：
{
    "code": "200",
    "message": "Notification marked as read"
}
```



#### Internal API

1. 任务分配时需要创建通知(**任务与行动项提取模块** => **协作与通知模块**)

```py
create_task_notification(task_data: dict): None

task_data:
  - userId
  - taskId
 	- content
  - ddl
```



2 转录完成后需要创建通知（给所有会议参与者发通知）

```py
get_user_notifications(user_id=user.id,status='unread')
```



## Framework

前端 Vue 模版？



后端使用 Fastapi 时的项目架构