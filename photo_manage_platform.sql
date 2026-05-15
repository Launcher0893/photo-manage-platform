/*
 Navicat MySQL Dump SQL

 Source Server         : PhotoManagePlatfrom
 Source Server Type    : MySQL
 Source Server Version : 80043 (8.0.43)
 Source Host           : localhost:3306
 Source Schema         : photo_manage_platform

 Target Server Type    : MySQL
 Target Server Version : 80043 (8.0.43)
 File Encoding         : 65001

 Date: 15/05/2026 13:21:36
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `admin_id` int NOT NULL AUTO_INCREMENT COMMENT '管理员ID',
  `admin_account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录账号',
  `admin_password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码，MD5加密',
  `admin_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '管理员姓名',
  `role_id` int NULL DEFAULT NULL COMMENT '角色ID',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1正常，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`admin_id`) USING BTREE,
  UNIQUE INDEX `uk_admin_account`(`admin_account` ASC) USING BTREE,
  INDEX `fk_admin_role`(`role_id` ASC) USING BTREE,
  CONSTRAINT `fk_admin_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '管理员表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', '系统管理员', 1, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');

-- ----------------------------
-- Table structure for announcement
-- ----------------------------
DROP TABLE IF EXISTS `announcement`;
CREATE TABLE `announcement`  (
  `announcement_id` int NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告内容',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公告图片OSS地址',
  `admin_id` int NOT NULL COMMENT '发布管理员ID',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1发布，0下架',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`announcement_id`) USING BTREE,
  INDEX `fk_announcement_admin`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `fk_announcement_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '公告表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of announcement
-- ----------------------------
INSERT INTO `announcement` VALUES (2, '作品征集说明', '欢迎上传街拍、人像、风光等类型作品，优秀作品将推荐到首页精选区域。', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/announcements/bb75be4057894356953e794b2d67b18b.png', 1, 1, '2026-05-14 12:08:02', '2026-05-14 12:08:02');

-- ----------------------------
-- Table structure for carousel
-- ----------------------------
DROP TABLE IF EXISTS `carousel`;
CREATE TABLE `carousel`  (
  `carousel_id` int NOT NULL AUTO_INCREMENT COMMENT '轮播图ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '轮播标题',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片OSS地址',
  `link_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '跳转类型：work、photographer、announcement、url',
  `link_id` int NULL DEFAULT NULL COMMENT '跳转目标ID',
  `link_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '外部跳转地址',
  `sort` int NULL DEFAULT 0 COMMENT '排序值',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1启用，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`carousel_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '首页轮播图表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of carousel
-- ----------------------------
INSERT INTO `carousel` VALUES (1, 'test', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/carousels/7bf8c492aacc49d69b69977470355caa.png', NULL, NULL, NULL, 0, 1, '2026-05-13 21:42:52');
INSERT INTO `carousel` VALUES (2, 'test2', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/carousels/e4218023d4774604b7ffcd2f8b386e26.png', NULL, NULL, NULL, 1, 1, '2026-05-13 15:30:31');
INSERT INTO `carousel` VALUES (4, 'test4', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/carousels/84528d161d0f48eb8eb06e4b46939492.png', NULL, NULL, NULL, 4, 1, '2026-05-14 09:06:17');

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `category_id` int NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类名称',
  `sort` int NULL DEFAULT 0 COMMENT '排序值',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1启用，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`category_id`) USING BTREE,
  UNIQUE INDEX `uk_category_name`(`category_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品分类/风格标签表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES (1, '人像', 1, 1, '2026-05-13 21:41:15', '2026-05-13 21:41:16');
INSERT INTO `category` VALUES (2, '街拍', 2, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');
INSERT INTO `category` VALUES (3, '风光', 3, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');
INSERT INTO `category` VALUES (4, '黑白光影', 4, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');

-- ----------------------------
-- Table structure for forum_board
-- ----------------------------
DROP TABLE IF EXISTS `forum_board`;
CREATE TABLE `forum_board`  (
  `board_id` int NOT NULL AUTO_INCREMENT COMMENT '板块ID',
  `board_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '板块名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '板块描述',
  `sort` int NULL DEFAULT 0 COMMENT '排序值',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1启用，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`board_id`) USING BTREE,
  UNIQUE INDEX `uk_board_name`(`board_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '论坛板块表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum_board
-- ----------------------------
INSERT INTO `forum_board` VALUES (1, '作品交流', '发布作品并交流构图、色彩和后期思路', 1, 1, '2026-05-13 10:00:00');
INSERT INTO `forum_board` VALUES (2, '技巧分享', '讨论器材、布光、修图和拍摄经验', 2, 1, '2026-05-13 10:00:00');

-- ----------------------------
-- Table structure for forum_comment
-- ----------------------------
DROP TABLE IF EXISTS `forum_comment`;
CREATE TABLE `forum_comment`  (
  `comment_id` int NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `post_id` int NOT NULL COMMENT '帖子ID',
  `user_id` int NOT NULL COMMENT '评论用户ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论内容',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1正常，0删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `fk_forum_comment_post`(`post_id` ASC) USING BTREE,
  INDEX `fk_forum_comment_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_forum_comment_post` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`post_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_forum_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '帖子评论表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum_comment
-- ----------------------------
INSERT INTO `forum_comment` VALUES (1, 1, 2, '参数说明很清楚，学习了。', 0, '2026-05-15 10:23:44');
INSERT INTO `forum_comment` VALUES (2, 1, 4, '下次可以试试更低的机位。', 0, '2026-05-15 10:23:44');
INSERT INTO `forum_comment` VALUES (3, 2, 1, '这个布光方案很适合练习。', 0, '2026-05-15 10:23:39');
INSERT INTO `forum_comment` VALUES (4, 4, 1, '牢祥好帅啊，爱了爱了', 0, '2026-05-15 10:23:35');
INSERT INTO `forum_comment` VALUES (5, 5, 9, '666', 1, '2026-05-14 10:10:33');
INSERT INTO `forum_comment` VALUES (6, 4, 10, '牢祥好帅啊，爱了爱了', 1, '2026-05-15 10:23:22');

-- ----------------------------
-- Table structure for forum_post
-- ----------------------------
DROP TABLE IF EXISTS `forum_post`;
CREATE TABLE `forum_post`  (
  `post_id` int NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
  `board_id` int NOT NULL COMMENT '所属板块ID',
  `user_id` int NOT NULL COMMENT '发帖用户ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '帖子标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '帖子内容',
  `view_count` int NULL DEFAULT 0 COMMENT '浏览量',
  `like_count` int NULL DEFAULT 0 COMMENT '点赞数',
  `comment_count` int NULL DEFAULT 0 COMMENT '评论数',
  `is_top` smallint NULL DEFAULT 0 COMMENT '是否置顶：1是，0否',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1正常，0删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`post_id`) USING BTREE,
  INDEX `fk_forum_post_board`(`board_id` ASC) USING BTREE,
  INDEX `fk_forum_post_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_forum_post_board` FOREIGN KEY (`board_id`) REFERENCES `forum_board` (`board_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_forum_post_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '论坛帖子表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum_post
-- ----------------------------
INSERT INTO `forum_post` VALUES (1, 1, 1, '第一次夜景人像拍摄心得', '分享一次夜景人像拍摄的参数设置和现场沟通经验。', 62, 1, 0, 0, 0, '2026-05-15 10:23:44', '2026-05-15 10:23:45');
INSERT INTO `forum_post` VALUES (2, 2, 2, '人像布光笔记', '整理几种常见人像布光方式，适合室内小空间练习。', 42, 1, 0, 0, 0, '2026-05-15 10:23:39', '2026-05-15 10:23:40');
INSERT INTO `forum_post` VALUES (3, 1, 1, 'test_work1', 'test example for work', 7, 0, 0, 0, 0, '2026-05-15 13:13:06', '2026-05-15 13:13:07');
INSERT INTO `forum_post` VALUES (4, 1, 5, '李的遗憾', '困住我青春的人始终没有回头看我', 43, 1, 1, 0, 1, '2026-05-15 13:21:08', '2026-05-15 13:21:08');
INSERT INTO `forum_post` VALUES (5, 1, 9, '清纯男大', '男大daisiki', 18, 2, 1, 0, 1, '2026-05-15 10:23:54', '2026-05-15 10:23:54');
INSERT INTO `forum_post` VALUES (6, 1, 12, '春夏秋冬', 'AI创作', 13, 1, 0, 0, 1, '2026-05-15 12:16:18', '2026-05-15 12:16:19');
INSERT INTO `forum_post` VALUES (7, 2, 10, '黄金时段法则', '日出后一小时和日落前一小时，光线柔和、色温温暖、阴影拉长，几乎任何题材在这个时段拍摄都会有更好的表现。这个时段被称为“黄金时刻”，是户外人像、风光摄影的绝佳时机。\r\n顺光：主体明亮、色彩鲜艳，但缺乏立体感，适合旅行记录和抓拍\r\n侧光：产生强烈明暗对比，突出纹理和轮廓，是人像和静物的经典用光\r\n逆光：营造剪影效果或漂亮的光晕，需要控制曝光补偿，适合氛围感照片\r\n散射光：阴天或多云时的柔和光线，反差小、细节丰富，特别适合人像和花卉特写', 2, 0, 0, 0, 1, '2026-05-15 13:12:31', '2026-05-15 13:12:32');

-- ----------------------------
-- Table structure for forum_post_image
-- ----------------------------
DROP TABLE IF EXISTS `forum_post_image`;
CREATE TABLE `forum_post_image`  (
  `image_id` int NOT NULL AUTO_INCREMENT COMMENT '图片ID',
  `post_id` int NOT NULL COMMENT '帖子ID',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片OSS地址',
  `oss_object_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'OSS文件对象名',
  `sort` int NULL DEFAULT 0 COMMENT '排序值',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `fk_post_image_post`(`post_id` ASC) USING BTREE,
  CONSTRAINT `fk_post_image_post` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`post_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '帖子图片表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum_post_image
-- ----------------------------
INSERT INTO `forum_post_image` VALUES (1, 1, 'https://via.placeholder.com/900x600?text=Forum+Post+1', NULL, 1, '2026-05-11 19:00:00');
INSERT INTO `forum_post_image` VALUES (2, 2, 'https://via.placeholder.com/900x600?text=Forum+Post+2', NULL, 1, '2026-05-12 20:00:00');
INSERT INTO `forum_post_image` VALUES (3, 3, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/587a4297eac247a1941a17c6e3e682dd.png', 'photo-manage-platform/forum/587a4297eac247a1941a17c6e3e682dd.png', 1, '2026-05-14 09:07:50');
INSERT INTO `forum_post_image` VALUES (4, 4, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/da9b12ce7b6c469cb57c415aff12dd26.jpg', 'photo-manage-platform/forum/da9b12ce7b6c469cb57c415aff12dd26.jpg', 1, '2026-05-14 09:26:02');
INSERT INTO `forum_post_image` VALUES (5, 5, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/370793af4bcd428fb1ebed65879ea26a.jpg', 'photo-manage-platform/forum/370793af4bcd428fb1ebed65879ea26a.jpg', 1, '2026-05-14 10:10:05');
INSERT INTO `forum_post_image` VALUES (6, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/5137c09e76e84071a1340080987ee4c6.jpg', 'photo-manage-platform/forum/5137c09e76e84071a1340080987ee4c6.jpg', 1, '2026-05-15 12:16:10');
INSERT INTO `forum_post_image` VALUES (7, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/6de477fa7e474dfeb46f02fa1ec2642e.jpg', 'photo-manage-platform/forum/6de477fa7e474dfeb46f02fa1ec2642e.jpg', 2, '2026-05-15 12:16:10');
INSERT INTO `forum_post_image` VALUES (8, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/144dcc054b104387bc10ec3eff30247a.jpg', 'photo-manage-platform/forum/144dcc054b104387bc10ec3eff30247a.jpg', 3, '2026-05-15 12:16:10');
INSERT INTO `forum_post_image` VALUES (9, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/aadfc5209b6b4b2c95c76289a8aacbb2.jpg', 'photo-manage-platform/forum/aadfc5209b6b4b2c95c76289a8aacbb2.jpg', 4, '2026-05-15 12:16:10');
INSERT INTO `forum_post_image` VALUES (10, 7, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/forum/e5f53fc9e19a41408cf63571bf29f7b0.png', 'photo-manage-platform/forum/e5f53fc9e19a41408cf63571bf29f7b0.png', 1, '2026-05-15 13:12:32');

-- ----------------------------
-- Table structure for forum_post_like
-- ----------------------------
DROP TABLE IF EXISTS `forum_post_like`;
CREATE TABLE `forum_post_like`  (
  `like_id` int NOT NULL AUTO_INCREMENT COMMENT '??ID',
  `post_id` int NOT NULL COMMENT '??ID',
  `user_id` int NOT NULL COMMENT '??ID',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  PRIMARY KEY (`like_id`) USING BTREE,
  UNIQUE INDEX `uk_forum_post_user`(`post_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `fk_forum_post_like_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_forum_post_like_post` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`post_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_forum_post_like_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '?????' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum_post_like
-- ----------------------------
INSERT INTO `forum_post_like` VALUES (1, 1, 2, '2026-05-12 21:10:00');
INSERT INTO `forum_post_like` VALUES (2, 2, 1, '2026-05-12 21:20:00');
INSERT INTO `forum_post_like` VALUES (5, 4, 1, '2026-05-14 09:26:29');
INSERT INTO `forum_post_like` VALUES (7, 5, 9, '2026-05-15 02:09:23');
INSERT INTO `forum_post_like` VALUES (8, 5, 10, '2026-05-15 10:23:54');
INSERT INTO `forum_post_like` VALUES (9, 6, 12, '2026-05-15 12:16:15');

-- ----------------------------
-- Table structure for photo_work
-- ----------------------------
DROP TABLE IF EXISTS `photo_work`;
CREATE TABLE `photo_work`  (
  `work_id` int NOT NULL AUTO_INCREMENT COMMENT '作品ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作品标题',
  `photographer_id` int NOT NULL COMMENT '摄影师ID',
  `category_id` int NOT NULL COMMENT '分类ID',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '封面图OSS地址',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '拍摄城市',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '作品描述',
  `view_count` int NULL DEFAULT 0 COMMENT '浏览量',
  `like_count` int NULL DEFAULT 0 COMMENT '点赞数',
  `comment_count` int NULL DEFAULT 0 COMMENT '评论数',
  `hot_score` int NULL DEFAULT 0 COMMENT '热度分',
  `audit_status` smallint NULL DEFAULT 0 COMMENT '审核状态：0待审核，1通过，2拒绝',
  `is_featured` smallint NULL DEFAULT 0 COMMENT '是否精选：1是，0否',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1上架，0下架',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`work_id`) USING BTREE,
  INDEX `fk_work_photographer`(`photographer_id` ASC) USING BTREE,
  INDEX `fk_work_category`(`category_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_work_photographer` FOREIGN KEY (`photographer_id`) REFERENCES `photographer` (`photographer_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '摄影作品表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of photo_work
-- ----------------------------
INSERT INTO `photo_work` VALUES (1, '夜色人像', 1, 1, 'https://via.placeholder.com/900x600?text=Night+Portrait', '上海', '夜景环境下的人像摄影作品，强调城市霓虹与人物情绪。', 134, 2, 2, 144, 1, 1, 0, '2026-05-10 14:00:00', '2026-05-14 10:35:39');
INSERT INTO `photo_work` VALUES (2, '街头光影', 1, 2, 'https://via.placeholder.com/900x600?text=Street+Light', '广州', '街头抓拍中的光影层次，记录日常场景里的瞬间。', 98, 1, 1, 103, 1, 0, 0, '2026-05-11 15:00:00', '2026-05-14 10:35:39');
INSERT INTO `photo_work` VALUES (3, '海边清晨', 2, 3, 'https://via.placeholder.com/900x600?text=Morning+Sea', '深圳', '日出时分的海边风光，色彩柔和，层次清晰。', 88, 0, 0, 88, 1, 0, 0, '2026-05-12 08:00:00', '2026-05-14 10:35:37');
INSERT INTO `photo_work` VALUES (4, '霸王', 3, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/953b0bfcaefa4f6cb719374da201b4ab.jpg', '武汉', '今日我虽死，但我仍是霸王。', 8, 3, 2, 21, 1, 0, 1, '2026-05-14 09:33:30', '2026-05-15 13:21:08');
INSERT INTO `photo_work` VALUES (5, '奇幻牢祥', 4, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/95131e118733464eb870b23759ac1bdd.jpg', '武汉', '牢祥daisiki', 8, 3, 0, 17, 1, 0, 1, '2026-05-14 10:00:56', '2026-05-15 11:17:58');
INSERT INTO `photo_work` VALUES (6, '点开的是gay', 4, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/95fd762693514fe18e6df030e7114e15.jpg', '武汉', '点开的是gay', 4, 0, 0, 4, 1, 0, 1, '2026-05-14 10:12:41', '2026-05-15 10:19:02');
INSERT INTO `photo_work` VALUES (7, '巨人的城堡', 4, 1, NULL, '武汉', '巨人的城堡', 5, 1, 0, 8, 1, 0, 0, '2026-05-14 20:52:56', '2026-05-14 23:01:32');
INSERT INTO `photo_work` VALUES (8, '巨人的城堡', 4, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/b43180fc03a249eab488e1a380a909b3.jpg', '武汉', '巨人的城堡', 0, 0, 0, 0, 1, 0, 0, '2026-05-14 23:06:36', '2026-05-14 23:07:13');
INSERT INTO `photo_work` VALUES (9, '巨人的城堡', 4, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/b88f88742cec41218e3de450b72c7dea.jpg', '武汉', '巨人的城堡', 1, 0, 0, 1, 1, 0, 1, '2026-05-14 23:06:47', '2026-05-15 11:21:58');
INSERT INTO `photo_work` VALUES (10, '武汉', 4, 2, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/6d78410979a143d0a5b1225bade3f2b9.jpg', '武汉', '武汉', 1, 0, 0, 1, 1, 0, 1, '2026-05-14 23:07:59', '2026-05-15 11:21:49');
INSERT INTO `photo_work` VALUES (11, '闲人小屁孩', 4, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/d63de91fc29c4a858dc96693b6a555ae.jpg', '湖南', '闲人小屁孩', 5, 0, 0, 5, 1, 0, 1, '2026-05-14 23:08:55', '2026-05-15 11:21:54');
INSERT INTO `photo_work` VALUES (12, '街角咖啡店', 5, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/082f717f73db4077806853906c361e9d.png', '武汉', '我从山中来，带着兰花草。家中无富贵，口袋无财宝。', 24, 2, 1, 32, 1, 0, 1, '2026-05-15 10:45:52', '2026-05-15 11:33:51');
INSERT INTO `photo_work` VALUES (13, '四時之花', 6, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/5f682c6185074cfbaa0411a21d41956d.jpg', '武汉', '风起时刻，四时花开', 33, 2, 0, 39, 1, 0, 1, '2026-05-15 11:07:16', '2026-05-15 11:33:44');
INSERT INTO `photo_work` VALUES (14, '再见，再见', 6, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/1b67043ad8684c5d917254cba054ce96.jpg', '武汉', '我很欣赏你有独当一面的勇气，但是世界有太多定律我们无法改变，你吃饭了吗，我带你去吃饭吧', 38, 3, 0, 47, 1, 0, 1, '2026-05-15 11:15:20', '2026-05-15 11:34:11');
INSERT INTO `photo_work` VALUES (15, '琳琅', 6, 2, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/7aac6f63806a48648279dd0fd69e9156.jpg', '荆州', '我想，人生是可以慢半拍', 2, 1, 0, 5, 1, 0, 1, '2026-05-15 11:21:31', '2026-05-15 11:30:41');
INSERT INTO `photo_work` VALUES (16, 'L.O.V.E.', 6, 1, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/1076503f67fe47c4aa2b940fd9b4cbba.jpg', '武汉', '幸福，易如反掌', 19, 2, 0, 25, 1, 0, 1, '2026-05-15 11:29:13', '2026-05-15 11:33:49');
INSERT INTO `photo_work` VALUES (17, '❀', 5, 3, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/5e181def2fb64526b4590cdb3ec8cd13.png', '武汉', NULL, 0, 0, 0, 0, 1, 0, 1, '2026-05-15 13:08:53', '2026-05-15 13:08:53');
INSERT INTO `photo_work` VALUES (18, '☁', 5, 3, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/948dd54c84fa42b49ebf76c275c92e52.png', '武汉', NULL, 0, 0, 0, 0, 1, 0, 1, '2026-05-15 13:09:16', '2026-05-15 13:09:16');

-- ----------------------------
-- Table structure for photo_work_image
-- ----------------------------
DROP TABLE IF EXISTS `photo_work_image`;
CREATE TABLE `photo_work_image`  (
  `image_id` int NOT NULL AUTO_INCREMENT COMMENT '图片ID',
  `work_id` int NOT NULL COMMENT '作品ID',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片OSS地址',
  `oss_object_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'OSS文件对象名，用于删除',
  `sort` int NULL DEFAULT 0 COMMENT '排序值',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `fk_work_image_work`(`work_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_image_work` FOREIGN KEY (`work_id`) REFERENCES `photo_work` (`work_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品组图表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of photo_work_image
-- ----------------------------
INSERT INTO `photo_work_image` VALUES (1, 1, 'https://via.placeholder.com/900x600?text=Night+Portrait+1', NULL, 1, '2026-05-10 14:00:00');
INSERT INTO `photo_work_image` VALUES (2, 1, 'https://via.placeholder.com/900x600?text=Night+Portrait+2', NULL, 2, '2026-05-10 14:00:00');
INSERT INTO `photo_work_image` VALUES (3, 2, 'https://via.placeholder.com/900x600?text=Street+Light+1', NULL, 1, '2026-05-11 15:00:00');
INSERT INTO `photo_work_image` VALUES (4, 3, 'https://via.placeholder.com/900x600?text=Morning+Sea+1', NULL, 1, '2026-05-12 08:00:00');
INSERT INTO `photo_work_image` VALUES (5, 4, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/0295b9c6d7f745c99b075660de5e843e.jpg', 'photo-manage-platform/works/0295b9c6d7f745c99b075660de5e843e.jpg', 1, '2026-05-14 09:33:31');
INSERT INTO `photo_work_image` VALUES (6, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/087e86a067654989bda6b73025963c83.jpg', 'photo-manage-platform/works/087e86a067654989bda6b73025963c83.jpg', 1, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (7, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/ebf741c476824caf8383a4319064ed20.jpg', 'photo-manage-platform/works/ebf741c476824caf8383a4319064ed20.jpg', 2, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (8, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/a17df3ac1bfd42f6b9f5f7479c8602ad.jpg', 'photo-manage-platform/works/a17df3ac1bfd42f6b9f5f7479c8602ad.jpg', 3, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (9, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/3ad6ab138a404417ad82052e8bf8e182.jpg', 'photo-manage-platform/works/3ad6ab138a404417ad82052e8bf8e182.jpg', 4, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (10, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/520a7796716342d4b71ea563fef9f941.jpg', 'photo-manage-platform/works/520a7796716342d4b71ea563fef9f941.jpg', 5, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (11, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/68a6867e44764efa994f7d062e7c764c.jpg', 'photo-manage-platform/works/68a6867e44764efa994f7d062e7c764c.jpg', 6, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (12, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/f2bf251a67d84eacbd1d746c6dc26f73.jpg', 'photo-manage-platform/works/f2bf251a67d84eacbd1d746c6dc26f73.jpg', 7, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (13, 6, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/79d7ea4ae7a1409885122f47874d3253.jpg', 'photo-manage-platform/works/79d7ea4ae7a1409885122f47874d3253.jpg', 8, '2026-05-14 10:16:53');
INSERT INTO `photo_work_image` VALUES (14, 12, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/f375a5b48b9847ad8d8a5fe4130ca81a.png', 'photo-manage-platform/works/f375a5b48b9847ad8d8a5fe4130ca81a.png', 1, '2026-05-15 10:48:26');
INSERT INTO `photo_work_image` VALUES (16, 13, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/2322ffaf4af24fffa69c5c8421af3be4.jpg', 'photo-manage-platform/works/2322ffaf4af24fffa69c5c8421af3be4.jpg', 1, '2026-05-15 11:07:34');
INSERT INTO `photo_work_image` VALUES (17, 13, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/c0217121f8a04a3fa6d792d2e4d425af.jpg', 'photo-manage-platform/works/c0217121f8a04a3fa6d792d2e4d425af.jpg', 2, '2026-05-15 11:07:34');
INSERT INTO `photo_work_image` VALUES (18, 14, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/f0964e4f5914472cab693c390d0204d6.jpg', 'photo-manage-platform/works/f0964e4f5914472cab693c390d0204d6.jpg', 1, '2026-05-15 11:15:21');
INSERT INTO `photo_work_image` VALUES (19, 15, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/ae1395cca588486183b777afa7bcd85f.jpg', 'photo-manage-platform/works/ae1395cca588486183b777afa7bcd85f.jpg', 1, '2026-05-15 11:21:32');
INSERT INTO `photo_work_image` VALUES (20, 15, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/61614a754a984aa8bf74b937712ae860.jpg', 'photo-manage-platform/works/61614a754a984aa8bf74b937712ae860.jpg', 2, '2026-05-15 11:21:32');
INSERT INTO `photo_work_image` VALUES (21, 16, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/8e00bf3dc40a4f45a3603374aa25a536.jpg', 'photo-manage-platform/works/8e00bf3dc40a4f45a3603374aa25a536.jpg', 1, '2026-05-15 11:29:14');
INSERT INTO `photo_work_image` VALUES (22, 16, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/9fbfeb9d018d4b27b62aca1405dae98a.jpg', 'photo-manage-platform/works/9fbfeb9d018d4b27b62aca1405dae98a.jpg', 2, '2026-05-15 11:29:14');
INSERT INTO `photo_work_image` VALUES (23, 17, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/4a13f8a16c1e4455810a0447beaf4fff.png', 'photo-manage-platform/works/4a13f8a16c1e4455810a0447beaf4fff.png', 1, '2026-05-15 13:08:54');
INSERT INTO `photo_work_image` VALUES (24, 18, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/works/5aae75a478ca459db6ba01730131bb05.png', 'photo-manage-platform/works/5aae75a478ca459db6ba01730131bb05.png', 1, '2026-05-15 13:09:17');

-- ----------------------------
-- Table structure for photographer
-- ----------------------------
DROP TABLE IF EXISTS `photographer`;
CREATE TABLE `photographer`  (
  `photographer_id` int NOT NULL AUTO_INCREMENT COMMENT '摄影师ID',
  `user_id` int NOT NULL COMMENT '关联user.user_id',
  `real_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '所在城市',
  `cert_status` smallint NULL DEFAULT 0 COMMENT '认证状态：0待审核，1通过，2拒绝',
  `cert_remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '审核备注',
  `audit_admin_id` int NULL DEFAULT NULL COMMENT '审核管理员ID',
  `audit_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '审核时间',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`photographer_id`) USING BTREE,
  UNIQUE INDEX `uk_user_id`(`user_id` ASC) USING BTREE,
  INDEX `fk_photographer_audit_admin`(`audit_admin_id` ASC) USING BTREE,
  CONSTRAINT `fk_photographer_audit_admin` FOREIGN KEY (`audit_admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `fk_photographer_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '摄影师认证资料表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of photographer
-- ----------------------------
INSERT INTO `photographer` VALUES (1, 2, '李明', '上海', 1, '资料完整，审核通过', 1, '2026-05-10 10:00:00', '2026-05-08 09:30:00', '2026-05-10 10:00:00');
INSERT INTO `photographer` VALUES (2, 3, '周然', '广州', 1, '作品风格清晰', 1, '2026-05-11 10:00:00', '2026-05-09 09:30:00', '2026-05-11 10:00:00');
INSERT INTO `photographer` VALUES (3, 7, NULL, NULL, 1, NULL, 1, '2026-05-14 09:30:43', '2026-05-14 09:30:42', '2026-05-14 09:30:43');
INSERT INTO `photographer` VALUES (4, 9, NULL, NULL, 1, '关系户', 1, '2026-05-14 09:37:38', '2026-05-14 09:37:37', '2026-05-14 09:37:38');
INSERT INTO `photographer` VALUES (5, 10, '肖卓', '武汉', 1, '666', 1, '2026-05-15 10:51:25', '2026-05-15 10:51:25', '2026-05-15 10:51:25');
INSERT INTO `photographer` VALUES (6, 12, NULL, '荆州', 1, NULL, 1, '2026-05-15 11:03:11', '2026-05-15 11:03:11', '2026-05-15 11:03:11');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `role_id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `permissions` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '管理员角色表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, '超级管理员', 'all', '系统默认管理员角色', '2026-05-13 10:00:00', '2026-05-13 10:00:00');

-- ----------------------------
-- Table structure for system_log
-- ----------------------------
DROP TABLE IF EXISTS `system_log`;
CREATE TABLE `system_log`  (
  `log_id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `admin_id` int NOT NULL COMMENT '操作管理员ID',
  `operate_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作类型',
  `operate_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作内容',
  `ip_address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作IP',
  `operate_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `fk_system_log_admin`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `fk_system_log_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 51 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统操作日志表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_log
-- ----------------------------
INSERT INTO `system_log` VALUES (1, 1, '初始化数据', '导入课程项目演示数据', '127.0.0.1', '2026-05-13 10:00:00');
INSERT INTO `system_log` VALUES (2, 1, '作品保存', '保存作品：海边清晨', '127.0.0.1', '2026-05-13 20:55:40');
INSERT INTO `system_log` VALUES (3, 1, '公告删除', '删除公告：????????', '127.0.0.1', '2026-05-13 21:00:49');
INSERT INTO `system_log` VALUES (4, 1, '公告保存', '保存公告：test', '127.0.0.1', '2026-05-13 21:02:37');
INSERT INTO `system_log` VALUES (5, 1, '公告删除', '删除公告：test', '127.0.0.1', '2026-05-13 21:02:45');
INSERT INTO `system_log` VALUES (6, 1, '公告删除', '删除公告：平台试运行公告', '127.0.0.1', '2026-05-13 21:03:07');
INSERT INTO `system_log` VALUES (7, 1, '分类状态', '更新分类状态：人像', '127.0.0.1', '2026-05-13 21:41:14');
INSERT INTO `system_log` VALUES (8, 1, '分类状态', '更新分类状态：人像', '127.0.0.1', '2026-05-13 21:41:16');
INSERT INTO `system_log` VALUES (9, 1, '作品状态', '下架作品：海边清晨', '127.0.0.1', '2026-05-13 21:41:36');
INSERT INTO `system_log` VALUES (10, 1, '作品状态', '恢复作品：海边清晨', '127.0.0.1', '2026-05-13 21:41:37');
INSERT INTO `system_log` VALUES (11, 1, '作品状态', '下架作品：海边清晨', '127.0.0.1', '2026-05-13 21:41:50');
INSERT INTO `system_log` VALUES (12, 1, '作品状态', '恢复作品：海边清晨', '127.0.0.1', '2026-05-13 21:41:51');
INSERT INTO `system_log` VALUES (13, 1, '作品评论状态', '更新作品评论：3', '127.0.0.1', '2026-05-13 21:42:00');
INSERT INTO `system_log` VALUES (14, 1, '作品评论状态', '更新作品评论：3', '127.0.0.1', '2026-05-13 21:42:01');
INSERT INTO `system_log` VALUES (15, 1, '帖子置顶', '更新帖子置顶：第一次夜景人像拍摄心得', '127.0.0.1', '2026-05-13 21:42:27');
INSERT INTO `system_log` VALUES (16, 1, '帖子置顶', '更新帖子置顶：第一次夜景人像拍摄心得', '127.0.0.1', '2026-05-13 21:42:28');
INSERT INTO `system_log` VALUES (17, 1, '论坛评论状态', '更新论坛评论：3', '127.0.0.1', '2026-05-13 21:42:36');
INSERT INTO `system_log` VALUES (18, 1, '论坛评论状态', '更新论坛评论：3', '127.0.0.1', '2026-05-13 21:42:37');
INSERT INTO `system_log` VALUES (19, 1, '轮播图状态', '更新轮播图状态：test', '127.0.0.1', '2026-05-13 21:42:52');
INSERT INTO `system_log` VALUES (20, 1, '轮播图状态', '更新轮播图状态：test', '127.0.0.1', '2026-05-13 21:42:53');
INSERT INTO `system_log` VALUES (21, 1, '用户状态', '更新用户状态：user1', '127.0.0.1', '2026-05-13 21:44:09');
INSERT INTO `system_log` VALUES (22, 1, '用户状态', '更新用户状态：user1', '127.0.0.1', '2026-05-13 21:44:20');
INSERT INTO `system_log` VALUES (23, 1, '轮播图保存', '保存轮播图：test4', '127.0.0.1', '2026-05-14 09:06:17');
INSERT INTO `system_log` VALUES (24, 1, '轮播图删除', '删除轮播图：test3', '127.0.0.1', '2026-05-14 09:13:53');
INSERT INTO `system_log` VALUES (25, 1, '摄影师审核', '审核摄影师：Leeeee', '127.0.0.1', '2026-05-14 09:30:43');
INSERT INTO `system_log` VALUES (26, 1, '摄影师审核', '审核摄影师：lazale2', '127.0.0.1', '2026-05-14 09:37:38');
INSERT INTO `system_log` VALUES (27, 1, '帖子置顶', '更新帖子置顶：第一次夜景人像拍摄心得', '127.0.0.1', '2026-05-14 10:35:00');
INSERT INTO `system_log` VALUES (28, 1, '帖子状态', '更新帖子状态：人像布光笔记', '127.0.0.1', '2026-05-14 10:35:02');
INSERT INTO `system_log` VALUES (29, 1, '帖子状态', '更新帖子状态：第一次夜景人像拍摄心得', '127.0.0.1', '2026-05-14 10:35:04');
INSERT INTO `system_log` VALUES (30, 1, '作品状态', '下架作品：海边清晨', '127.0.0.1', '2026-05-14 10:35:37');
INSERT INTO `system_log` VALUES (31, 1, '作品状态', '下架作品：街头光影', '127.0.0.1', '2026-05-14 10:35:39');
INSERT INTO `system_log` VALUES (32, 1, '作品状态', '下架作品：夜色人像', '127.0.0.1', '2026-05-14 10:35:39');
INSERT INTO `system_log` VALUES (33, 1, '用户状态', '更新用户状态：user1', '127.0.0.1', '2026-05-14 10:37:55');
INSERT INTO `system_log` VALUES (34, 1, '用户状态', '更新用户状态：user_test', '127.0.0.1', '2026-05-14 10:37:57');
INSERT INTO `system_log` VALUES (35, 1, '用户状态', '更新用户状态：user3', '127.0.0.1', '2026-05-14 10:37:58');
INSERT INTO `system_log` VALUES (36, 1, '用户状态', '更新用户状态：user2', '127.0.0.1', '2026-05-14 10:37:59');
INSERT INTO `system_log` VALUES (37, 1, '用户删除', '删除用户：user3', '127.0.0.1', '2026-05-14 11:03:24');
INSERT INTO `system_log` VALUES (38, 1, '用户删除', '删除用户：user2', '127.0.0.1', '2026-05-14 11:03:30');
INSERT INTO `system_log` VALUES (39, 1, '用户删除', '删除用户：user_test', '127.0.0.1', '2026-05-14 11:03:32');
INSERT INTO `system_log` VALUES (40, 1, '用户删除', '删除用户：user1', '127.0.0.1', '2026-05-14 11:03:35');
INSERT INTO `system_log` VALUES (41, 1, '公告保存', '保存公告：作品征集说明', '127.0.0.1', '2026-05-14 12:08:02');
INSERT INTO `system_log` VALUES (42, 1, '作品评论状态', '更新作品评论：5', '127.0.0.1', '2026-05-15 09:15:02');
INSERT INTO `system_log` VALUES (43, 1, '作品评论状态', '更新作品评论：5', '127.0.0.1', '2026-05-15 09:15:03');
INSERT INTO `system_log` VALUES (44, 1, '摄影师审核', '审核摄影师：Launcher0893', '127.0.0.1', '2026-05-15 10:22:27');
INSERT INTO `system_log` VALUES (45, 1, '论坛评论状态', '更新论坛评论：4', '127.0.0.1', '2026-05-15 10:23:35');
INSERT INTO `system_log` VALUES (46, 1, '论坛评论状态', '更新论坛评论：3', '127.0.0.1', '2026-05-15 10:23:40');
INSERT INTO `system_log` VALUES (47, 1, '论坛评论状态', '更新论坛评论：2', '127.0.0.1', '2026-05-15 10:23:44');
INSERT INTO `system_log` VALUES (48, 1, '论坛评论状态', '更新论坛评论：1', '127.0.0.1', '2026-05-15 10:23:45');
INSERT INTO `system_log` VALUES (49, 1, '摄影师审核', '审核摄影师：Jasmine99_D', '127.0.0.1', '2026-05-15 10:57:27');
INSERT INTO `system_log` VALUES (50, 1, '帖子状态', '更新帖子状态：test_work1', '127.0.0.1', '2026-05-15 13:13:07');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码，MD5加密',
  `nickname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '昵称',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像OSS地址',
  `user_role` smallint NULL DEFAULT 1 COMMENT '角色：1普通用户，2摄影师',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1正常，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'user1', 'e10adc3949ba59abbe56e057f20f883e', '晨光旅人', 'user1@example.com', '13800000001', 'https://via.placeholder.com/300x200?text=User1', 1, -1, '2026-05-14 11:03:34', '2026-05-14 11:03:35');
INSERT INTO `user` VALUES (2, 'user2', 'e10adc3949ba59abbe56e057f20f883e', '城市取景器', 'user2@example.com', '13800000002', 'https://via.placeholder.com/300x200?text=User2', 2, -1, '2026-05-14 11:03:29', '2026-05-14 11:03:30');
INSERT INTO `user` VALUES (3, 'user3', 'e10adc3949ba59abbe56e057f20f883e', '胶片观察员', 'user3@example.com', '13800000003', 'https://via.placeholder.com/300x200?text=User3', 2, -1, '2026-05-14 11:03:23', '2026-05-14 11:03:24');
INSERT INTO `user` VALUES (4, 'user_test', 'e10adc3949ba59abbe56e057f20f883e', '测试用户', 'test@example.com', '13800000004', 'https://via.placeholder.com/300x200?text=Test', 1, -1, '2026-05-14 11:03:32', '2026-05-14 11:03:32');
INSERT INTO `user` VALUES (5, 'Gemini', 'e10adc3949ba59abbe56e057f20f883e', 'Gemini', NULL, NULL, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/avatars/8876d5702a314fb99e63e88df0cbe40d.jpg', 1, 1, '2026-05-14 11:10:11', '2026-05-14 11:10:12');
INSERT INTO `user` VALUES (6, 'Lee', 'e10adc3949ba59abbe56e057f20f883e', '归零.', NULL, NULL, NULL, 1, 1, '2026-05-14 09:29:21', '2026-05-14 09:29:21');
INSERT INTO `user` VALUES (7, 'Leeeee', 'e10adc3949ba59abbe56e057f20f883e', '归零', NULL, NULL, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/avatars/4464bd95c04a4c28a5356e701c5a5926.jpg', 2, 1, '2026-05-14 11:05:21', '2026-05-14 11:05:22');
INSERT INTO `user` VALUES (8, 'lazale', '62c8ad0a15d9d1ca38d5dee762a16e01', 'lazale', NULL, NULL, NULL, 1, 1, '2026-05-14 09:35:40', '2026-05-14 09:35:40');
INSERT INTO `user` VALUES (9, 'lazale2', '62c8ad0a15d9d1ca38d5dee762a16e01', 'lazale2', NULL, NULL, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/avatars/0906ca48783e484eac94baebb8ee9df6.jpg', 2, 1, '2026-05-14 11:09:56', '2026-05-14 11:09:56');
INSERT INTO `user` VALUES (10, 'Launcher0893', 'e10adc3949ba59abbe56e057f20f883e', '黎若雨', 'xiaozhuo0893@outlook.com', '13117206686', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/avatars/928c0a2bf53848da99947a09e25127dc.jpg', 2, 1, '2026-05-15 10:51:03', '2026-05-15 10:51:04');
INSERT INTO `user` VALUES (11, 'Jasmine99_DYC', 'e10adc3949ba59abbe56e057f20f883e', '沫梨咏', NULL, NULL, NULL, 1, 1, '2026-05-15 10:54:00', '2026-05-15 10:54:00');
INSERT INTO `user` VALUES (12, 'Jasmine99_D', 'e10adc3949ba59abbe56e057f20f883e', '沫梨梨咏', NULL, NULL, 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/avatars/5b9c9d2bcbca443f8801664746443a21.jpg', 2, 1, '2026-05-15 11:02:58', '2026-05-15 11:02:58');

-- ----------------------------
-- Table structure for work_comment
-- ----------------------------
DROP TABLE IF EXISTS `work_comment`;
CREATE TABLE `work_comment`  (
  `comment_id` int NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `work_id` int NOT NULL COMMENT '作品ID',
  `user_id` int NOT NULL COMMENT '评论用户ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论内容',
  `audit_status` smallint NULL DEFAULT 1 COMMENT '审核状态：0待审核，1通过，2拒绝',
  `status` smallint NULL DEFAULT 1 COMMENT '状态：1正常，0删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `fk_work_comment_work`(`work_id` ASC) USING BTREE,
  INDEX `fk_work_comment_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_work_comment_work` FOREIGN KEY (`work_id`) REFERENCES `photo_work` (`work_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品评论表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of work_comment
-- ----------------------------
INSERT INTO `work_comment` VALUES (1, 1, 1, '构图很稳，夜景颜色也很干净。', 1, 1, '2026-05-12 13:00:00', '2026-05-12 13:00:00');
INSERT INTO `work_comment` VALUES (2, 1, 4, '人物和背景的层次很好。', 1, 1, '2026-05-12 13:10:00', '2026-05-12 13:10:00');
INSERT INTO `work_comment` VALUES (3, 2, 4, '街头氛围很自然。', 1, 1, '2026-05-13 21:42:01', '2026-05-13 21:42:01');
INSERT INTO `work_comment` VALUES (4, 4, 7, '111', 1, 1, '2026-05-14 09:33:47', '2026-05-14 09:33:47');
INSERT INTO `work_comment` VALUES (5, 4, 5, '董哥daisiki', 1, 1, '2026-05-15 09:15:02', '2026-05-15 09:15:03');
INSERT INTO `work_comment` VALUES (6, 12, 12, '好评', 1, 1, '2026-05-15 11:16:40', '2026-05-15 11:16:40');

-- ----------------------------
-- Table structure for work_like
-- ----------------------------
DROP TABLE IF EXISTS `work_like`;
CREATE TABLE `work_like`  (
  `like_id` int NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `work_id` int NOT NULL COMMENT '作品ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '点赞时间',
  PRIMARY KEY (`like_id`) USING BTREE,
  UNIQUE INDEX `uk_work_user`(`work_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `fk_work_like_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_like_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_work_like_work` FOREIGN KEY (`work_id`) REFERENCES `photo_work` (`work_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品点赞表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of work_like
-- ----------------------------
INSERT INTO `work_like` VALUES (2, 1, 4, '2026-05-12 12:05:00');
INSERT INTO `work_like` VALUES (3, 2, 1, '2026-05-12 12:10:00');
INSERT INTO `work_like` VALUES (6, 1, 1, '2026-05-13 20:15:01');
INSERT INTO `work_like` VALUES (7, 4, 7, '2026-05-14 09:33:44');
INSERT INTO `work_like` VALUES (8, 5, 9, '2026-05-14 10:06:10');
INSERT INTO `work_like` VALUES (9, 5, 5, '2026-05-14 10:06:23');
INSERT INTO `work_like` VALUES (10, 4, 5, '2026-05-14 10:06:30');
INSERT INTO `work_like` VALUES (11, 7, 9, '2026-05-14 22:44:44');
INSERT INTO `work_like` VALUES (12, 12, 10, '2026-05-15 10:49:32');
INSERT INTO `work_like` VALUES (13, 4, 12, '2026-05-15 11:16:25');
INSERT INTO `work_like` VALUES (14, 12, 12, '2026-05-15 11:16:31');
INSERT INTO `work_like` VALUES (15, 5, 12, '2026-05-15 11:17:58');
INSERT INTO `work_like` VALUES (16, 14, 12, '2026-05-15 11:18:05');
INSERT INTO `work_like` VALUES (17, 13, 12, '2026-05-15 11:18:11');
INSERT INTO `work_like` VALUES (18, 16, 12, '2026-05-15 11:29:37');
INSERT INTO `work_like` VALUES (19, 15, 12, '2026-05-15 11:30:41');
INSERT INTO `work_like` VALUES (20, 14, 10, '2026-05-15 11:33:39');
INSERT INTO `work_like` VALUES (21, 13, 10, '2026-05-15 11:33:44');
INSERT INTO `work_like` VALUES (22, 16, 10, '2026-05-15 11:33:49');
INSERT INTO `work_like` VALUES (23, 14, 7, '2026-05-15 11:34:11');

SET FOREIGN_KEY_CHECKS = 1;
