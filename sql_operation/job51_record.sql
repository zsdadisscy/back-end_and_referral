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

 Date: 16/04/2024 21:01:51
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
  INDEX `index_job_title_record`(`jobTitle` ASC) USING BTREE,
  INDEX `index_job_title_crawl`(`jobTitle` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 47 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of job51_record
-- ----------------------------
INSERT INTO `job51_record` VALUES (1, '计算机', '2024-04-12 11:35:31');
INSERT INTO `job51_record` VALUES (2, '临床医学', '2024-04-12 11:40:52');
INSERT INTO `job51_record` VALUES (3, '会计', '2024-04-12 11:48:39');
INSERT INTO `job51_record` VALUES (4, '电气工程及其自动化', '2024-04-12 11:53:52');
INSERT INTO `job51_record` VALUES (5, '金融', '2024-04-12 12:00:01');
INSERT INTO `job51_record` VALUES (6, '软件工程', '2024-04-12 12:05:47');
INSERT INTO `job51_record` VALUES (7, '建筑', '2024-04-12 12:11:05');
INSERT INTO `job51_record` VALUES (8, '法律', '2024-04-12 12:14:33');
INSERT INTO `job51_record` VALUES (9, '机械', '2024-04-12 18:42:31');
INSERT INTO `job51_record` VALUES (10, '电子信息', '2024-04-12 18:46:50');
INSERT INTO `job51_record` VALUES (11, '英语', '2024-04-12 18:51:31');
INSERT INTO `job51_record` VALUES (12, '人工智能', '2024-04-12 18:56:05');
INSERT INTO `job51_record` VALUES (13, '经济', '2024-04-12 19:01:00');
INSERT INTO `job51_record` VALUES (14, '工商管理', '2024-04-12 19:05:40');
INSERT INTO `job51_record` VALUES (15, '电子商务', '2024-04-12 19:10:12');
INSERT INTO `job51_record` VALUES (16, '土木工程', '2024-04-12 19:14:52');
INSERT INTO `job51_record` VALUES (17, '通信工程', '2024-04-12 19:19:42');
INSERT INTO `job51_record` VALUES (18, '汉语言文学', '2024-04-12 19:24:30');
INSERT INTO `job51_record` VALUES (19, '水利', '2024-04-12 19:28:58');
INSERT INTO `job51_record` VALUES (20, '力学', '2024-04-12 19:33:49');
INSERT INTO `job51_record` VALUES (21, '学前教育', '2024-04-12 19:38:34');
INSERT INTO `job51_record` VALUES (22, '物理', '2024-04-12 19:43:18');
INSERT INTO `job51_record` VALUES (23, '生物', '2024-04-12 19:48:08');
INSERT INTO `job51_record` VALUES (24, '化学', '2024-04-12 19:53:03');
INSERT INTO `job51_record` VALUES (25, '地理', '2024-04-12 19:57:47');
INSERT INTO `job51_record` VALUES (26, '历史', '2024-04-12 20:02:27');
INSERT INTO `job51_record` VALUES (27, '销售客服', '2024-04-12 20:07:08');
INSERT INTO `job51_record` VALUES (28, '行政助理', '2024-04-12 20:12:00');
INSERT INTO `job51_record` VALUES (29, '物流采购', '2024-04-12 20:16:52');
INSERT INTO `job51_record` VALUES (30, '外贸业务', '2024-04-12 20:21:40');
INSERT INTO `job51_record` VALUES (31, 'IT技术', '2024-04-12 20:26:34');
INSERT INTO `job51_record` VALUES (32, '财务金融', '2024-04-12 20:31:24');
INSERT INTO `job51_record` VALUES (33, '工程技术', '2024-04-12 20:35:56');
INSERT INTO `job51_record` VALUES (34, '房地产', '2024-04-12 20:40:40');
INSERT INTO `job51_record` VALUES (35, '生物医药', '2024-04-12 20:45:34');
INSERT INTO `job51_record` VALUES (36, '服务行业', '2024-04-12 20:50:10');
INSERT INTO `job51_record` VALUES (37, '电子商务经理', '2024-04-12 20:54:50');
INSERT INTO `job51_record` VALUES (38, '健康与福祉顾问', '2024-04-12 20:59:36');
INSERT INTO `job51_record` VALUES (39, '网络安全工程师', '2024-04-12 21:04:08');
INSERT INTO `job51_record` VALUES (40, '区块链开发者', '2024-04-12 21:08:40');
INSERT INTO `job51_record` VALUES (41, '虚拟现实设计师', '2024-04-12 21:13:26');
INSERT INTO `job51_record` VALUES (42, '碳管理师', '2024-04-12 21:18:08');
INSERT INTO `job51_record` VALUES (43, '数据科学家', '2024-04-12 21:21:53');
INSERT INTO `job51_record` VALUES (44, '能源管理师', '2024-04-13 08:37:10');
INSERT INTO `job51_record` VALUES (45, '人工智能工程师', '2024-04-13 08:39:42');
INSERT INTO `job51_record` VALUES (46, 'ESG商业分析师', '2024-04-13 08:42:07');

SET FOREIGN_KEY_CHECKS = 1;
