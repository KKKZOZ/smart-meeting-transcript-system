
TRUNCATE TABLE demo_items;

INSERT INTO demo_items (id,value) VALUES 
(1, '111'),
(2, '112'),
(3, '113'),
(4, '114'),
(5, '115');


-- 插入一个会议，由test用户创造
INSERT INTO meetings (meeting_id, title, start_time, end_time, language, creator_id,video_url)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'test_meeting', '2024-12-14 12:00:00', '2024-12-14 14:00:00', 'zh', 'JVy6aUWEnZBqCiU','https://software-project510.oss-cn-beijing.aliyuncs.com/Audio/2024-12-18-video.mp3');

-- 会议由test，admin，user1参与
INSERT INTO meeting_participants (meeting_id, participant_id)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'JVy6aUWEnZBqCiU');
INSERT INTO meeting_participants (meeting_id, participant_id)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'WZIuMvWHhZCIiJA');
INSERT INTO meeting_participants (meeting_id, participant_id)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'BL9PkGGttj4pS7J');

-- 会议转录内容
INSERT INTO transcriptions (meeting_id, task_id, task_status, content, timestamp, language,ischanged)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', NULL, NULL, NULL, '2024-12-18 07:15:41', 'zh',NULL);
