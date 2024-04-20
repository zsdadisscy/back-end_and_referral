DROP DATABASE IF EXISTS jobs51;
CREATE DATABASE jobs51;
# ALTER DATABASE jobs51 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

use jobs51;
DROP TABLE IF EXISTS job51;

CREATE TABLE job51 (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    jobTitle VARCHAR(30),
                    jobName VARCHAR(50),
                    cityString VARCHAR(30),
                    provideSalaryString VARCHAR(20),
                    issueDateString DATETIME,
                    workYearString VARCHAR(10),
                    degreeString VARCHAR(10),
                    companyName VARCHAR(100),
                    companyTypeString VARCHAR(10),
                    companySizeString VARCHAR(20),
                    jobHref VARCHAR(250),
                    companyHref VARCHAR(250),
                    industryType VARCHAR(50),
                    jobDescribe VARCHAR(2000),
                    city VARCHAR(30)
                );

# 加入索引
CREATE INDEX index_job_title ON job51 (jobTitle);

DROP TABLE IF EXISTS User;
CREATE TABLE User (
    username VARCHAR(30) PRIMARY KEY,
    name VARCHAR(30),
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(2)  default '男',
    age INT,
    major VARCHAR(50),
    interest_position VARCHAR(255),
    password_question VARCHAR(255),
    password_answer VARCHAR(255),
    interest_city VARCHAR(255),
    education VARCHAR(7) default '本科',
    avatar VARCHAR(255)
);

# 时间戳
CREATE TABLE job51_record (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    jobTitle VARCHAR(30) UNIQUE,
                    # 添加插入时间
                    insertTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                );

# 加入索引
CREATE INDEX index_job_title_record ON job51_record (jobTitle);

# 数据抓取表
DROP TABLE IF EXISTS job51_crawl;
CREATE TABLE job51_crawl (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    jobTitle VARCHAR(30) UNIQUE
                );

# 加入索引
CREATE INDEX index_job_title_crawl ON job51_record (jobTitle);