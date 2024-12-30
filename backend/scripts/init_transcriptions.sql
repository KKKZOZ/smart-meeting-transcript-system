-- 插入一个会议，由test用户创造
INSERT INTO meetings (meeting_id, title, start_time, end_time, language, creator_id, video_url)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'test_meeting', '2024-12-14 12:00:00', '2024-12-14 14:00:00', 'zh', 'JVy6aUWEnZBqCiU','https://software-project510.oss-cn-beijing.aliyuncs.com/Audio/2024-12-18-video.mp3');

-- 会议由test，admin，user1参与
INSERT INTO meeting_participants (meeting_id, participant_id)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'JVy6aUWEnZBqCiU');
INSERT INTO meeting_participants (meeting_id, participant_id)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'WZIuMvWHhZCIiJA');
INSERT INTO meeting_participants (meeting_id, participant_id)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', 'BL9PkGGttj4pS7J');

-- 会议转录内容
INSERT INTO transcriptions (meeting_id, task_id, task_status, content, timestamp, language, speaker_count, ischanged)
VALUES ('f885f4e5-b450-477d-8efa-436ac4b41c0c', NULL, NULL, "张经理：大家好，感谢大家抽出时间参加这次会议。今天的主要议题是讨论客户服务流程的改进。首先，我想听听大家对目前服务流程的看法。李主管：我认为我们目前的响应时间还有待提高。有些客户反馈，他们的咨询没有得到及时回复。王专员：我同意李主管的观点。此外，我们的服务流程可以更加标准化，比如设立常见问题解答库，这样能提高我们解决问题的效率。赵助理：我觉得我们可以利用一些客服软件，实现多渠道接入，这样客户可以通过他们喜欢的方式与我们沟通。刘分析师：我分析了客户反馈数据，发现很多客户对我们的售后服务满意度不高。我们可以考虑延长售后服务时间，并提供更灵活的解决方案。张经理：很好，大家提出了很多有建设性的意见。那么，我们来布置一下任务。李主管，您负责牵头优化响应时间，制定具体措施，并监督执行。李主管：好的，我会尽快拿出方案。张经理：王专员，您负责建立常见问题解答库，并与相关部门协作，确保内容的准确性和实用性。王专员：明白了，我会着手进行。张经理：赵助理，您调研一下市场上的客服软件，看看哪款更适合我们，并准备一份推荐报告。赵助理：好的，我会尽快完成调研。张经理：刘分析师，您继续监控客户反馈数据，为我们提供改进方向。同时，协助李主管优化售后服务流程。刘分析师：没问题，我会持续关注。张经理：好的，今天的会议就到这里。请大家按照分工，积极推进任务。谢谢大家！", '2024-12-18 07:15:41', 'zh',0,NULL);