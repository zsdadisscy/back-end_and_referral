# -*- coding: utf-8 -*-            
# @Time : 2024/3/26 20:33
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm

import pymysql


def init_database(host='localhost', user='root', passwd='Scy123456', charset='utf8mb4', db='jobs51'):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, charset=charset, db=db)
    cursor = conn.cursor()
    return conn, cursor


if __name__ == '__main__':
    print('运行init_database成功')
