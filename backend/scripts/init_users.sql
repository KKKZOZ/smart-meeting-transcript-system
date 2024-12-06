
-- 清空并重新创建用户表
TRUNCATE TABLE users;

-- 插入用户 (密码: admin123)
INSERT INTO users (username, hashed_password, phone) VALUES 
('admin', '$2b$12$Aw0Sc2BiPHgKuzZ6tdkbjuR7WFLkWmcQ1YG0Ve5iGct.prcrPaCU6', '13800000000');

-- 插入用户 (密码: test123)
INSERT INTO users (username, hashed_password, phone) VALUES 
('test', '$2b$12$v2DjpsUTtSEvPciRIJttUesgjQNyfP2yDaFXqBzF0TQDTTHHI5BFq', '13800000001');

-- 插入用户 (密码: test123)
INSERT INTO users (username, hashed_password, phone) VALUES 
('user1', '$2b$12$ac/3nQQPrdTseUiBUdnCE.upCJ17e4fVdJjPnyUWYHjEn2UzdSJp6', '13800000002');

-- 插入用户 (密码: test123)
INSERT INTO users (username, hashed_password, phone) VALUES 
('user2', '$2b$12$KW3I8..RkXwAE6xZ00L0XeQV4XzZWWl0WvE9flQvvEIc/igAJT0Gu', '13800000003');
