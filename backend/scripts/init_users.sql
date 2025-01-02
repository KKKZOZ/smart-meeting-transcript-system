-- 清空并重新创建用户表
TRUNCATE TABLE users;

-- 插入用户 (密码: admin123)
INSERT INTO users (user_id,username, hashed_password, email,nickname,notification_type,enabled) VALUES 
('1','admin', '$2b$12$j5qnQ4no2I0UpdYRsYZIyOn/CNgO5s4xyw2K7LUrXFmBqj9zEtKc6', 'admin@example.com', '张经理',1,1);

-- 插入用户 (密码: test123)
INSERT INTO users (user_id,username, hashed_password, email,nickname,notification_type,enabled) VALUES 
('2','test', '$2b$12$H6SAqBgeKL7JrnKRsY6Ho.vr/Bb4f15A9WA9Cktfw0z2kHC1Zqvve', 'test@example.com', '李主管',1,1);

-- 插入用户 (密码: test123)
INSERT INTO users (user_id,username, hashed_password, email,nickname,notification_type,enabled) VALUES 
('3','user1', '$2b$12$9T0h8DKZt5mmmcG3tKymhet/JOC4T3GAOihZ58S2ZjR3/D.iCZ.y.', 'user1@example.com', '王专员',1,1);

-- 插入用户 (密码: test123)
INSERT INTO users (user_id,username, hashed_password, email,nickname,notification_type,enabled) VALUES 
('4','user2', '$2b$12$a3RF8U1wIjhninNOHv0FpeO2Kx84Xr9lcZvcHXVRz3DVuAyzjbfl6', 'user2@example.com', '赵助理',1,1);

-- 插入用户 (密码: liujinyi)
INSERT INTO users (user_id,username, hashed_password, email,nickname,notification_type,enabled) VALUES 
('5','liujinyi', '$2b$12$vtZayOlmcvvABgQZ5Ns..OUgByr2ZkV8uyYMuimUejymyvYQwcNaq', 'kkkzoz@qq.com', '刘分析师',1,1);
