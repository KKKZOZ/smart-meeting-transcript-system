-- 1. user_id: 1, task_id: 1, status: unread
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '1', '1', '用户1的任务1的通知', CURRENT_TIMESTAMP, 'unread');

-- 2. user_id: 2, task_id: 1, status: read
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '2', '1', '用户2的任务1的通知', CURRENT_TIMESTAMP, 'read');

-- 3. user_id: 3, task_id: 2, status: unread
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '3', '2', '用户3的任务2的通知', CURRENT_TIMESTAMP, 'unread');

-- 4. user_id: 4, task_id: 3, status: read
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '4', '3', '用户4的任务3的通知', CURRENT_TIMESTAMP, 'read');

-- 5. user_id: 1, task_id: 4, status: unread
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '1', '4', '用户1的任务4的通知', CURRENT_TIMESTAMP, 'unread');

-- 6. user_id: 2, task_id: 2, status: read
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '2', '2', '用户2的任务2的通知', CURRENT_TIMESTAMP, 'read');

-- 7. user_id: 3, task_id: 4, status: unread
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '3', '4', '用户3的任务4的通知', CURRENT_TIMESTAMP, 'unread');

-- 8. user_id: 4, task_id: 1, status: read
INSERT INTO notifications (notification_id, user_id, task_id, content, ddl, status)
VALUES (UUID(), '4', '1', '用户4的任务1的通知', CURRENT_TIMESTAMP, 'read');
