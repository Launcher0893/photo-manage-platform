/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80018 (8.0.18)
 Source Host           : localhost:3306
 Source Schema         : photo_manage_platform

 Target Server Type    : MySQL
 Target Server Version : 80018 (8.0.18)
 File Encoding         : 65001

 Date: 13/05/2026 10:15:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '管理员ID',
  `admin_account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录账号',
  `admin_password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码，MD5加密',
  `admin_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '管理员姓名',
  `role_id` int(11) NULL DEFAULT NULL COMMENT '角色ID',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1正常，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`admin_id`) USING BTREE,
  UNIQUE INDEX `uk_admin_account`(`admin_account` ASC) USING BTREE,
  INDEX `fk_admin_role`(`role_id` ASC) USING BTREE,
  CONSTRAINT `fk_admin_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '管理员表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------

-- ----------------------------
-- Table structure for announcement
-- ----------------------------
DROP TABLE IF EXISTS `announcement`;
CREATE TABLE `announcement`  (
  `announcement_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告内容',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公告图片OSS地址',
  `admin_id` int(11) NOT NULL COMMENT '发布管理员ID',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1发布，0下架',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`announcement_id`) USING BTREE,
  INDEX `fk_announcement_admin`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `fk_announcement_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '公告表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of announcement
-- ----------------------------

-- ----------------------------
-- Table structure for carousel
-- ----------------------------
DROP TABLE IF EXISTS `carousel`;
CREATE TABLE `carousel`  (
  `carousel_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '轮播图ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '轮播标题',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片OSS地址',
  `link_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '跳转类型：work、photographer、announcement、url',
  `link_id` int(11) NULL DEFAULT NULL COMMENT '跳转目标ID',
  `link_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '外部跳转地址',
  `sort` int(11) NULL DEFAULT 0 COMMENT '排序值',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1启用，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`carousel_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '首页轮播图表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of carousel
-- ----------------------------
INSERT INTO `carousel` VALUES (1, 'test', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/carousels/7bf8c492aacc49d69b69977470355caa.png', NULL, NULL, NULL, 0, 1, '2026-05-13 15:25:00');
INSERT INTO `carousel` VALUES (2, 'test2', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/carousels/e4218023d4774604b7ffcd2f8b386e26.png', NULL, NULL, NULL, 1, 1, '2026-05-13 15:30:31');
INSERT INTO `carousel` VALUES (3, 'test3', 'https://photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com/photo-manage-platform/carousels/940aa602cb854cfe99d4a4bee322011b.png', NULL, NULL, NULL, 3, 1, '2026-05-13 15:31:08');

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `category_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类名称',
  `sort` int(11) NULL DEFAULT 0 COMMENT '排序值',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1启用，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`category_id`) USING BTREE,
  UNIQUE INDEX `uk_category_name`(`category_name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品分类/风格标签表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of category
-- ----------------------------

-- ----------------------------
-- Table structure for forum_board
-- ----------------------------
DROP TABLE IF EXISTS `forum_board`;
CREATE TABLE `forum_board`  (
  `board_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '板块ID',
  `board_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '板块名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '板块描述',
  `sort` int(11) NULL DEFAULT 0 COMMENT '排序值',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1启用，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`board_id`) USING BTREE,
  UNIQUE INDEX `uk_board_name`(`board_name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '论坛板块表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of forum_board
-- ----------------------------

-- ----------------------------
-- Table structure for forum_comment
-- ----------------------------
DROP TABLE IF EXISTS `forum_comment`;
CREATE TABLE `forum_comment`  (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `post_id` int(11) NOT NULL COMMENT '帖子ID',
  `user_id` int(11) NOT NULL COMMENT '评论用户ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论内容',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1正常，0删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `fk_forum_comment_post`(`post_id` ASC) USING BTREE,
  INDEX `fk_forum_comment_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_forum_comment_post` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`post_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_forum_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '帖子评论表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of forum_comment
-- ----------------------------

-- ----------------------------
-- Table structure for forum_post
-- ----------------------------
DROP TABLE IF EXISTS `forum_post`;
CREATE TABLE `forum_post`  (
  `post_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
  `board_id` int(11) NOT NULL COMMENT '所属板块ID',
  `user_id` int(11) NOT NULL COMMENT '发帖用户ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '帖子标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '帖子内容',
  `view_count` int(11) NULL DEFAULT 0 COMMENT '浏览量',
  `like_count` int(11) NULL DEFAULT 0 COMMENT '点赞数',
  `comment_count` int(11) NULL DEFAULT 0 COMMENT '评论数',
  `is_top` smallint(6) NULL DEFAULT 0 COMMENT '是否置顶：1是，0否',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1正常，0删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`post_id`) USING BTREE,
  INDEX `fk_forum_post_board`(`board_id` ASC) USING BTREE,
  INDEX `fk_forum_post_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_forum_post_board` FOREIGN KEY (`board_id`) REFERENCES `forum_board` (`board_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_forum_post_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '论坛帖子表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of forum_post
-- ----------------------------

-- ----------------------------
-- Table structure for forum_post_like
-- ----------------------------
DROP TABLE IF EXISTS `forum_post_like`;
CREATE TABLE `forum_post_like`  (
  `like_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `post_id` int(11) NOT NULL COMMENT '帖子ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '点赞时间',
  PRIMARY KEY (`like_id`) USING BTREE,
  UNIQUE INDEX `uk_forum_post_user`(`post_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `fk_forum_post_like_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_forum_post_like_post` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`post_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_forum_post_like_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '帖子点赞表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of forum_post_like
-- ----------------------------

-- ----------------------------
-- Table structure for forum_post_image
-- ----------------------------
DROP TABLE IF EXISTS `forum_post_image`;
CREATE TABLE `forum_post_image`  (
  `image_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '图片ID',
  `post_id` int(11) NOT NULL COMMENT '帖子ID',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片OSS地址',
  `oss_object_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'OSS文件对象名',
  `sort` int(11) NULL DEFAULT 0 COMMENT '排序值',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `fk_post_image_post`(`post_id` ASC) USING BTREE,
  CONSTRAINT `fk_post_image_post` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`post_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '帖子图片表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of forum_post_image
-- ----------------------------

-- ----------------------------
-- Table structure for photo_work
-- ----------------------------
DROP TABLE IF EXISTS `photo_work`;
CREATE TABLE `photo_work`  (
  `work_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '作品ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作品标题',
  `photographer_id` int(11) NOT NULL COMMENT '摄影师ID',
  `category_id` int(11) NOT NULL COMMENT '分类ID',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '封面图OSS地址',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '拍摄城市',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '作品描述',
  `view_count` int(11) NULL DEFAULT 0 COMMENT '浏览量',
  `like_count` int(11) NULL DEFAULT 0 COMMENT '点赞数',
  `comment_count` int(11) NULL DEFAULT 0 COMMENT '评论数',
  `hot_score` int(11) NULL DEFAULT 0 COMMENT '热度分',
  `audit_status` smallint(6) NULL DEFAULT 0 COMMENT '审核状态：0待审核，1通过，2拒绝',
  `is_featured` smallint(6) NULL DEFAULT 0 COMMENT '是否精选：1是，0否',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1上架，0下架',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`work_id`) USING BTREE,
  INDEX `fk_work_photographer`(`photographer_id` ASC) USING BTREE,
  INDEX `fk_work_category`(`category_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_work_photographer` FOREIGN KEY (`photographer_id`) REFERENCES `photographer` (`photographer_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '摄影作品表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of photo_work
-- ----------------------------

-- ----------------------------
-- Table structure for photo_work_image
-- ----------------------------
DROP TABLE IF EXISTS `photo_work_image`;
CREATE TABLE `photo_work_image`  (
  `image_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '图片ID',
  `work_id` int(11) NOT NULL COMMENT '作品ID',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片OSS地址',
  `oss_object_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'OSS文件对象名，用于删除',
  `sort` int(11) NULL DEFAULT 0 COMMENT '排序值',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `fk_work_image_work`(`work_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_image_work` FOREIGN KEY (`work_id`) REFERENCES `photo_work` (`work_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品组图表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of photo_work_image
-- ----------------------------

-- ----------------------------
-- Table structure for photographer
-- ----------------------------
DROP TABLE IF EXISTS `photographer`;
CREATE TABLE `photographer`  (
  `photographer_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '摄影师ID',
  `user_id` int(11) NOT NULL COMMENT '关联user.user_id',
  `real_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '所在城市',
  `cert_status` smallint(6) NULL DEFAULT 0 COMMENT '认证状态：0待审核，1通过，2拒绝',
  `cert_remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '审核备注',
  `audit_admin_id` int(11) NULL DEFAULT NULL COMMENT '审核管理员ID',
  `audit_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '审核时间',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`photographer_id`) USING BTREE,
  UNIQUE INDEX `uk_user_id`(`user_id` ASC) USING BTREE,
  INDEX `fk_photographer_audit_admin`(`audit_admin_id` ASC) USING BTREE,
  CONSTRAINT `fk_photographer_audit_admin` FOREIGN KEY (`audit_admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `fk_photographer_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '摄影师认证资料表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of photographer
-- ----------------------------

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `role_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `permissions` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '管理员角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------

-- ----------------------------
-- Table structure for system_log
-- ----------------------------
DROP TABLE IF EXISTS `system_log`;
CREATE TABLE `system_log`  (
  `log_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `admin_id` int(11) NOT NULL COMMENT '操作管理员ID',
  `operate_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作类型',
  `operate_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作内容',
  `ip_address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作IP',
  `operate_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `fk_system_log_admin`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `fk_system_log_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统操作日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_log
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码，MD5加密',
  `nickname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '昵称',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像OSS地址',
  `user_role` smallint(6) NULL DEFAULT 1 COMMENT '角色：1普通用户，2摄影师',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1正常，0禁用',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '注册时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for work_comment
-- ----------------------------
DROP TABLE IF EXISTS `work_comment`;
CREATE TABLE `work_comment`  (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `work_id` int(11) NOT NULL COMMENT '作品ID',
  `user_id` int(11) NOT NULL COMMENT '评论用户ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论内容',
  `audit_status` smallint(6) NULL DEFAULT 1 COMMENT '审核状态：0待审核，1通过，2拒绝',
  `status` smallint(6) NULL DEFAULT 1 COMMENT '状态：1正常，0删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `fk_work_comment_work`(`work_id` ASC) USING BTREE,
  INDEX `fk_work_comment_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_work_comment_work` FOREIGN KEY (`work_id`) REFERENCES `photo_work` (`work_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品评论表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of work_comment
-- ----------------------------

-- ----------------------------
-- Table structure for work_like
-- ----------------------------
DROP TABLE IF EXISTS `work_like`;
CREATE TABLE `work_like`  (
  `like_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `work_id` int(11) NOT NULL COMMENT '作品ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '点赞时间',
  PRIMARY KEY (`like_id`) USING BTREE,
  UNIQUE INDEX `uk_work_user`(`work_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `fk_work_like_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_work_like_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_work_like_work` FOREIGN KEY (`work_id`) REFERENCES `photo_work` (`work_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '作品点赞表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of work_like
-- ----------------------------

-- ----------------------------
-- Demo records
-- ----------------------------
INSERT INTO `role` (`role_id`, `role_name`, `permissions`, `remark`, `create_time`, `update_time`) VALUES
(1, '超级管理员', 'all', '系统默认管理员角色', '2026-05-13 10:00:00', '2026-05-13 10:00:00');

INSERT INTO `admin` (`admin_id`, `admin_account`, `admin_password`, `admin_name`, `role_id`, `status`, `create_time`, `update_time`) VALUES
(1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', '系统管理员', 1, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');

INSERT INTO `user` (`user_id`, `username`, `password`, `nickname`, `email`, `phone`, `avatar_url`, `user_role`, `status`, `create_time`, `update_time`) VALUES
(1, 'user1', 'e10adc3949ba59abbe56e057f20f883e', '晨光旅人', 'user1@example.com', '13800000001', 'https://via.placeholder.com/300x200?text=User1', 1, 1, '2026-05-07 09:00:00', '2026-05-07 09:00:00'),
(2, 'user2', 'e10adc3949ba59abbe56e057f20f883e', '城市取景器', 'user2@example.com', '13800000002', 'https://via.placeholder.com/300x200?text=User2', 2, 1, '2026-05-08 09:00:00', '2026-05-08 09:00:00'),
(3, 'user3', 'e10adc3949ba59abbe56e057f20f883e', '胶片观察员', 'user3@example.com', '13800000003', 'https://via.placeholder.com/300x200?text=User3', 2, 1, '2026-05-09 09:00:00', '2026-05-09 09:00:00'),
(4, 'user_test', 'e10adc3949ba59abbe56e057f20f883e', '测试用户', 'test@example.com', '13800000004', 'https://via.placeholder.com/300x200?text=Test', 1, 1, '2026-05-10 09:00:00', '2026-05-10 09:00:00');

INSERT INTO `category` (`category_id`, `category_name`, `sort`, `status`, `create_time`, `update_time`) VALUES
(1, '人像', 1, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00'),
(2, '街拍', 2, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00'),
(3, '风光', 3, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00'),
(4, '黑白光影', 4, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');

INSERT INTO `photographer` (`photographer_id`, `user_id`, `real_name`, `city`, `cert_status`, `cert_remark`, `audit_admin_id`, `audit_time`, `create_time`, `update_time`) VALUES
(1, 2, '李明', '上海', 1, '资料完整，审核通过', 1, '2026-05-10 10:00:00', '2026-05-08 09:30:00', '2026-05-10 10:00:00'),
(2, 3, '周然', '广州', 1, '作品风格清晰', 1, '2026-05-11 10:00:00', '2026-05-09 09:30:00', '2026-05-11 10:00:00');

INSERT INTO `forum_board` (`board_id`, `board_name`, `description`, `sort`, `status`, `create_time`) VALUES
(1, '作品交流', '发布作品并交流构图、色彩和后期思路', 1, 1, '2026-05-13 10:00:00'),
(2, '技巧分享', '讨论器材、布光、修图和拍摄经验', 2, 1, '2026-05-13 10:00:00');

INSERT INTO `photo_work` (`work_id`, `title`, `photographer_id`, `category_id`, `cover_url`, `city`, `description`, `view_count`, `like_count`, `comment_count`, `hot_score`, `audit_status`, `is_featured`, `status`, `create_time`, `update_time`) VALUES
(1, '夜色人像', 1, 1, 'https://via.placeholder.com/900x600?text=Night+Portrait', '上海', '夜景环境下的人像摄影作品，强调城市霓虹与人物情绪。', 128, 2, 2, 138, 1, 1, 1, '2026-05-10 14:00:00', '2026-05-10 14:00:00'),
(2, '街头光影', 1, 2, 'https://via.placeholder.com/900x600?text=Street+Light', '广州', '街头抓拍中的光影层次，记录日常场景里的瞬间。', 96, 1, 1, 101, 1, 0, 1, '2026-05-11 15:00:00', '2026-05-11 15:00:00'),
(3, '海边清晨', 2, 3, 'https://via.placeholder.com/900x600?text=Morning+Sea', '深圳', '日出时分的海边风光，色彩柔和，层次清晰。', 88, 0, 0, 88, 1, 1, 1, '2026-05-12 08:00:00', '2026-05-12 08:00:00');

INSERT INTO `photo_work_image` (`image_id`, `work_id`, `image_url`, `oss_object_name`, `sort`, `create_time`) VALUES
(1, 1, 'https://via.placeholder.com/900x600?text=Night+Portrait+1', NULL, 1, '2026-05-10 14:00:00'),
(2, 1, 'https://via.placeholder.com/900x600?text=Night+Portrait+2', NULL, 2, '2026-05-10 14:00:00'),
(3, 2, 'https://via.placeholder.com/900x600?text=Street+Light+1', NULL, 1, '2026-05-11 15:00:00'),
(4, 3, 'https://via.placeholder.com/900x600?text=Morning+Sea+1', NULL, 1, '2026-05-12 08:00:00');

INSERT INTO `work_like` (`like_id`, `work_id`, `user_id`, `create_time`) VALUES
(1, 1, 1, '2026-05-12 12:00:00'),
(2, 1, 4, '2026-05-12 12:05:00'),
(3, 2, 1, '2026-05-12 12:10:00');

INSERT INTO `work_comment` (`comment_id`, `work_id`, `user_id`, `content`, `audit_status`, `status`, `create_time`, `update_time`) VALUES
(1, 1, 1, '构图很稳，夜景颜色也很干净。', 1, 1, '2026-05-12 13:00:00', '2026-05-12 13:00:00'),
(2, 1, 4, '人物和背景的层次很好。', 1, 1, '2026-05-12 13:10:00', '2026-05-12 13:10:00'),
(3, 2, 4, '街头氛围很自然。', 1, 1, '2026-05-12 13:20:00', '2026-05-12 13:20:00');

INSERT INTO `forum_post` (`post_id`, `board_id`, `user_id`, `title`, `content`, `view_count`, `like_count`, `comment_count`, `is_top`, `status`, `create_time`, `update_time`) VALUES
(1, 1, 1, '第一次夜景人像拍摄心得', '分享一次夜景人像拍摄的参数设置和现场沟通经验。', 56, 1, 2, 1, 1, '2026-05-11 19:00:00', '2026-05-11 19:00:00'),
(2, 2, 2, '人像布光笔记', '整理几种常见人像布光方式，适合室内小空间练习。', 42, 1, 1, 0, 1, '2026-05-12 20:00:00', '2026-05-12 20:00:00');

INSERT INTO `forum_post_like` (`like_id`, `post_id`, `user_id`, `create_time`) VALUES
(1, 1, 2, '2026-05-12 21:10:00'),
(2, 2, 1, '2026-05-12 21:20:00');

INSERT INTO `forum_post_image` (`image_id`, `post_id`, `image_url`, `oss_object_name`, `sort`, `create_time`) VALUES
(1, 1, 'https://via.placeholder.com/900x600?text=Forum+Post+1', NULL, 1, '2026-05-11 19:00:00'),
(2, 2, 'https://via.placeholder.com/900x600?text=Forum+Post+2', NULL, 1, '2026-05-12 20:00:00');

INSERT INTO `forum_comment` (`comment_id`, `post_id`, `user_id`, `content`, `status`, `create_time`) VALUES
(1, 1, 2, '参数说明很清楚，学习了。', 1, '2026-05-11 20:00:00'),
(2, 1, 4, '下次可以试试更低的机位。', 1, '2026-05-11 20:10:00'),
(3, 2, 1, '这个布光方案很适合练习。', 1, '2026-05-12 21:00:00');

INSERT INTO `announcement` (`announcement_id`, `title`, `content`, `cover_url`, `admin_id`, `status`, `create_time`, `update_time`) VALUES
(1, '平台试运行公告', '摄影作品分享平台当前已完成基础功能接入，欢迎发布作品和参与论坛交流。', 'https://via.placeholder.com/900x360?text=Announcement', 1, 1, '2026-05-13 09:00:00', '2026-05-13 09:00:00'),
(2, '作品征集说明', '欢迎上传街拍、人像、风光等类型作品，优秀作品将推荐到首页精选区域。', 'https://via.placeholder.com/900x360?text=Works+Wanted', 1, 1, '2026-05-12 09:00:00', '2026-05-12 09:00:00');

INSERT INTO `system_log` (`log_id`, `admin_id`, `operate_type`, `operate_content`, `ip_address`, `operate_time`) VALUES
(1, 1, '初始化数据', '导入课程项目演示数据', '127.0.0.1', '2026-05-13 10:00:00');

SET FOREIGN_KEY_CHECKS = 1;
