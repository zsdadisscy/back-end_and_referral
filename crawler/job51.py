import datetime
import json
import os
import random
import time
import sys
import requests

# 防止找不到包
sys.path.append('..')

import pandas as pd
from playwright.sync_api import sync_playwright  # 同步模式
from retrying import retry

from sql_operation import init_database

# 定义列名为全局变量
columns = ['岗位名称', '城市', "薪资", "发布时间", "工作经验", '学历要求', '公司名称', '公司类型', '公司人数',
           '岗位链接', '公司链接', '行业类型', '岗位描述']


# 用来获取省份
def get_province(city):
    # 这里采用高德地图的api，如果需要使用需要自己申请一个key，然后替换掉下面的key
    # 官网地址 https://developer.amap.com/api/webservice/guide/api/georegeo
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'key': '45f2d14634e443f0c298d94ed9babec8',
        'address': city
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == '1' and data['count'] == '1':
        return data['geocodes'][0]['province']
    return ''

# 初始化数据库


@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False, wait_fixed=3000)
# 这个装饰器的作用就是在滑块失败的时候可以重复滑动
def Sync_Playwright(url):
    """处理滑块"""
    with sync_playwright() as fp:
        bs = fp.firefox.launch(headless=False)  # 禁用无头模式(也就是启动不启动浏览器的区别)
        page = bs.new_page()  # 新建选项卡
        page.goto(url)  # 加载页面
        dropbutton = page.locator('#nc_1_n1z')
        box = dropbutton.bounding_box()  # 获取其边界框
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        page.mouse.down()
        # 模拟人类的鼠标移动轨迹
        steps = 30  # 可以根据需要调整步数
        for step in range(1, steps + 1):
            progress = step / steps
            mov_x = box['x'] + box['width'] / 2 + 300 * progress + random.uniform(-5, 5)
            mov_y = box['y'] + box['height'] / 2 + random.uniform(-5, 5)
            page.mouse.move(mov_x, mov_y)
            time.sleep(random.uniform(0.02, 0.1))  # 模拟人的自然反应时间
        page.mouse.up()
        ttt = random.uniform(5, 8)
        time.sleep(ttt)
        html = page.locator('xpath=/html/body/pre')
        qwer = html.inner_text()

        if 'resultbody' in qwer:
            a = json.loads(qwer)
            return a
        else:
            current_datetime = datetime.datetime.now()
            # 分别获取当前年、月、日、时、分、秒
            current_year = current_datetime.year
            current_month = current_datetime.month
            current_day = current_datetime.day
            current_hour = current_datetime.hour
            current_minute = current_datetime.minute
            current_second = current_datetime.second
            # 存日志
            with open(
                    f'./log/remove/error_{current_year}_{current_month}_{current_day}_{current_hour}.txt',
                    'a', encoding='utf-8') as f:
                f.write(
                    f'滑块失败，时间：{current_year}_{current_month}_{current_day}_{current_hour}_{current_minute}_{current_second}\n{json.loads(qwer)}\n')
            return False


def convert_characters(string: str) -> str:
    return string.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')


def save_csv(data, keyword):
    """保存数据"""
    # 如果文件不存在，则写入列名
    if not os.path.isfile(f'51jobs_{keyword}信息.csv'):
        df = pd.DataFrame(columns=columns)
        df.to_csv(f'51jobs_{keyword}信息.csv', index=False)

    # 使用pandas包将列表和列名整合到数据框架中
    df = pd.DataFrame(data, columns=columns)
    # 将数据框架保存为CSV文件
    df.to_csv(f'51jobs_{keyword}信息.csv', index=False, mode='a', header=False)


def save_mysql(data, keyword):
    """保存数据"""
    cursor, conn = None, None
    try:
        # 连接数据库
        conn, cursor = init_database()
        # 插入数据
        for job in data:
            # 获取省份
            province = get_province(job[2])
            cursor.execute(f'''INSERT INTO job51 (jobTitle, jobName, cityString, provideSalaryString, issueDateString, workYearString, degreeString,companyName, companyTypeString,
                 companySizeString,  jobHref, companyHref, industryType, jobDescribe, province) VALUES ( '{keyword}',
                    '{job[0]}', '{job[1]}', '{job[2]}', '{job[3]}', '{job[4]}', '{job[5]}', '{job[6]}', '{job[7]}', '{job[8]}', '{job[9]}', '{job[10]}', '{job[11]}', '{job[12][:1999].replace("'", '"')}', '{province}'
                );''')
        conn.commit()

    except Exception as e:
        current_datetime = datetime.datetime.now()
        # 分别获取当前年、月、日、时、分、秒
        current_year = current_datetime.year
        current_month = current_datetime.month
        current_day = current_datetime.day
        current_hour = current_datetime.hour
        current_minute = current_datetime.minute
        current_second = current_datetime.second
        with open(
                f'./log/db/error_{current_year}_{current_month}_{current_day}_{current_hour}_{current_minute}_{current_second}.txt',
                'w', encoding='utf-8') as f:
            f.write(str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 支持添加到数据库中
def save_data(data, keyword, type='csv'):
    if type == 'csv':
        save_csv(data, keyword)
    elif type == 'mysql':
        save_mysql(data, keyword)


def parseDataFields(job):
    """解析数据"""
    jobName = job['jobName']  # 岗位名称
    cityString = job['jobAreaString']  # 城市
    provideSalaryString = job['provideSalaryString']  # 薪资
    issueDateString = job['issueDateString']  # 发布时间
    workYearString = job['workYearString']  # 需要工作经验
    degreeString = job['degreeString']  # 学历
    companyName = job['companyName']  # 公司名称
    companyTypeString = job['companyTypeString']  # 企业类型
    companySizeString = job['companySizeString']  # 公司人数
    industryType = ''  # 行业类型
    for i in range(1, 10):
        if f'industryType{i}Str' in job:
            industryType += job[f'industryType{i}Str'] + '/'
        else:
            break
    jobHref = job['jobHref']  # 岗位链接
    companyHref = job['companyHref']  # 公司链接
    jobDescribe = job['jobDescribe']  # 岗位描述
    jobDescribe = convert_characters(jobDescribe)  # 去除换行符
    s = [jobName, cityString, provideSalaryString, issueDateString, workYearString, degreeString, companyName,
         companyTypeString,
         companySizeString, jobHref, companyHref, industryType, jobDescribe]
    return s


def get_data(keyword):
    keyword = convert_characters(keyword)

    # 判断job51_record中是否存在，如果存在则不再爬取，或者时间距今大于3个月也重新爬取
    conn, cursor = init_database()
    cursor.execute('select * from job51_record where jobTitle = "%s"' % keyword)
    res = cursor.fetchall()

    if len(res) >= 1:
        if (datetime.datetime.now() - res[0][2]).days < 90:
            cursor.close()
            conn.close()
            return  # 90天内不再爬取
        else: # 大于90天则删除原有数据
            cursor.execute('delete from job51 where jobTitle = "%s"' % keyword)

    folder_path1 = "./log/main"  # 将此处替换为要判断或创建的文件夹路径
    folder_path2 = "./log/remove"
    folder_path3 = "./log/db"
    if not os.path.exists(folder_path1):
        os.makedirs(folder_path1)
    if not os.path.exists(folder_path2):
        os.makedirs(folder_path2)
    if not os.path.exists(folder_path3):
        os.makedirs(folder_path3)
    # 获取当前时间的时间戳（秒）
    timestamp = int(time.time())
    # 将时间戳转换为指定格式的字符串
    formatted_timestamp = "{:06d}".format(timestamp)
    # 大小可以改
    for page in range(1, 11):
        url = (f'https://we.51job.com/api/job/search-pc?api_key=51job&timestamp={formatted_timestamp}&keyword={keyword}'
               f'&searchType=2&function=&industry=&jobArea&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&'
               f'companyType=&companySize=&jobType=&issueDate=&sortType=3&pageNum={page}&requestId='
               f'&pageSize=100&source=1&accountId=&pageCode=sou%7Csou%7Csoulb')
        try:
            html = Sync_Playwright(url)
            job_list = []
            # 获取数据
            jobs = html['resultbody']['job']['items']
            for job in jobs:
                s = parseDataFields(job)
                job_list.append(s)
            save_data(job_list, keyword, 'mysql')
            job_list.clear()
            # 记录爬取时间
            conn, cursor = init_database()
            cursor.execute('select * from job51_record where jobTitle = "%s"' % keyword)
            res = cursor.fetchall()
            # 如果存在这个记录就更新时间
            if len(res) >= 1:
                cursor.execute(
                    f'''UPDATE job51_record SET insertTime = '{datetime.datetime.now()}' WHERE jobTitle = '{keyword}' ''')
            else:
                cursor.execute(
                    f'''INSERT INTO job51_record (jobTitle, insertTime) VALUES ('{keyword}', '{datetime.datetime.now()}')''')
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            # 日志
            # 获取当前日期和时间
            current_datetime = datetime.datetime.now()

            # 分别获取当前年、月、日、时、分、秒
            current_year = current_datetime.year
            current_month = current_datetime.month
            current_day = current_datetime.day
            current_hour = current_datetime.hour
            current_minute = current_datetime.minute
            current_second = current_datetime.second
            with open(
                    f'./log/main/error_{current_year}_{current_month}_{current_day}_{current_hour}_{current_minute}_{current_second}.txt',
                    'w', encoding='utf-8') as f:
                f.write(str(e))


if __name__ == '__main__':
    keyword = input("请输入岗位:")
    get_data(keyword)
