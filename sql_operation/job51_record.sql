/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80030 (8.0.30)
 Source Host           : localhost:3306
 Source Schema         : jobs51

 Target Server Type    : MySQL
 Target Server Version : 80030 (8.0.30)
 File Encoding         : 65001

 Date: 01/05/2024 22:43:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for job51_record
-- ----------------------------
DROP TABLE IF EXISTS `job51_record`;
CREATE TABLE `job51_record`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `jobTitle` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `insertTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `jobTitle`(`jobTitle` ASC) USING BTREE,
  INDEX `index_job_title_record`(`jobTitle` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 46 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of job51_record
-- ----------------------------
INSERT INTO `job51_record` VALUES (1, '计算机', '2024-05-01 14:51:09');
INSERT INTO `job51_record` VALUES (2, '临床医学', '2024-05-01 14:54:11');
INSERT INTO `job51_record` VALUES (3, '会计', '2024-05-01 14:56:56');
INSERT INTO `job51_record` VALUES (4, '电气工程及其自动化', '2024-05-01 14:59:37');
INSERT INTO `job51_record` VALUES (5, '金融', '2024-05-01 15:02:20');
INSERT INTO `job51_record` VALUES (6, '软件工程', '2024-05-01 15:05:07');
INSERT INTO `job51_record` VALUES (7, '建筑', '2024-05-01 15:07:49');
INSERT INTO `job51_record` VALUES (8, '法律', '2024-05-01 15:10:38');
INSERT INTO `job51_record` VALUES (9, '机械', '2024-05-01 15:13:23');
INSERT INTO `job51_record` VALUES (10, '电子信息', '2024-05-01 15:16:13');
INSERT INTO `job51_record` VALUES (11, '英语', '2024-05-01 15:18:59');
INSERT INTO `job51_record` VALUES (12, '人工智能', '2024-05-01 15:21:46');
INSERT INTO `job51_record` VALUES (13, '经济', '2024-05-01 15:24:30');
INSERT INTO `job51_record` VALUES (14, '工商管理', '2024-05-01 15:27:18');
INSERT INTO `job51_record` VALUES (15, '电子商务', '2024-05-01 15:30:04');
INSERT INTO `job51_record` VALUES (16, '土木工程', '2024-05-01 15:32:46');
INSERT INTO `job51_record` VALUES (17, '通信工程', '2024-05-01 15:35:29');
INSERT INTO `job51_record` VALUES (18, '汉语言文学', '2024-05-01 15:38:22');
INSERT INTO `job51_record` VALUES (19, '水利', '2024-05-01 15:41:09');
INSERT INTO `job51_record` VALUES (20, '力学', '2024-05-01 15:43:54');
INSERT INTO `job51_record` VALUES (21, '学前教育', '2024-05-01 15:47:29');
INSERT INTO `job51_record` VALUES (22, '物理', '2024-05-01 15:50:13');
INSERT INTO `job51_record` VALUES (23, '生物', '2024-05-01 15:52:15');
INSERT INTO `job51_record` VALUES (24, '化学', '2024-05-01 16:08:29');
INSERT INTO `job51_record` VALUES (25, '地理', '2024-05-01 16:26:29');
INSERT INTO `job51_record` VALUES (26, '历史', '2024-05-01 16:29:15');
INSERT INTO `job51_record` VALUES (27, '销售客服', '2024-05-01 16:31:59');
INSERT INTO `job51_record` VALUES (28, '行政助理', '2024-05-01 16:34:53');
INSERT INTO `job51_record` VALUES (29, '物流采购', '2024-05-01 16:37:40');
INSERT INTO `job51_record` VALUES (30, '外贸业务', '2024-05-01 16:40:33');
INSERT INTO `job51_record` VALUES (31, 'IT技术', '2024-05-01 16:43:15');
INSERT INTO `job51_record` VALUES (32, '财务金融', '2024-05-01 16:46:09');
INSERT INTO `job51_record` VALUES (33, '工程技术', '2024-05-01 16:49:26');
INSERT INTO `job51_record` VALUES (34, '房地产', '2024-05-01 16:52:10');
INSERT INTO `job51_record` VALUES (35, '生物医药', '2024-05-01 16:54:57');
INSERT INTO `job51_record` VALUES (36, '服务行业', '2024-05-01 16:58:02');
INSERT INTO `job51_record` VALUES (37, '电子商务经理', '2024-05-01 17:00:50');
INSERT INTO `job51_record` VALUES (38, '健康与福祉顾问', '2024-05-01 17:01:20');
INSERT INTO `job51_record` VALUES (39, '网络安全工程师', '2024-05-01 17:06:33');
INSERT INTO `job51_record` VALUES (40, '区块链开发者', '2024-05-01 17:09:23');
INSERT INTO `job51_record` VALUES (41, '虚拟现实设计师', '2024-05-01 17:12:42');
INSERT INTO `job51_record` VALUES (42, '碳管理师', '2024-05-01 17:15:39');
INSERT INTO `job51_record` VALUES (43, '能源管理师', '2024-05-01 17:18:30');
INSERT INTO `job51_record` VALUES (44, '人工智能工程师', '2024-05-01 17:21:11');
INSERT INTO `job51_record` VALUES (45, 'ESG商业分析师', '2024-05-01 17:23:09');

SET FOREIGN_KEY_CHECKS = 1;
