# -*- coding: utf-8 -*-            
# @Time : 2024/4/16 下午5:15
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from sql_operation import init_database
import pandas as pd
from crawler.job51 import convert_characters

data_api = Blueprint('data', __name__)


# 从数据库中得到数据
def get_data(keyword):
    # 创建数据库连接
    conn, cursor = init_database()

    # 执行SQL查询
    cursor.execute("SELECT * FROM job51 where jobTitle='%s'" % keyword)

    # 获取所有记录列表
    results = cursor.fetchall()

    # 将结果转换为DataFrame
    df = pd.DataFrame(results, columns=[i[0] for i in cursor.description])

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return df


# 判断数据是否存在
@data_api.route('/judge_data', methods=['POST'])
@jwt_required()
def judge_data():
    job = request.json.get('job', None)
    if job is None:
        return jsonify({
            'result': 'fail',
            'msg': '参数错误'
        })
    job = convert_characters(job)
    conn, cursor = init_database()
    cursor.execute('select * from job51_record where jobTitle = %s', job)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if data:
        return jsonify({
            'result': 'success',
        })
    else:
        return jsonify({
            'result': 'fail',
            'msg': '数据不存在'
        })


# 分析数据
@data_api.route('/analysis_data', methods=['POST'])
@jwt_required()
def analysis_data():
    job = request.json.get('job', None)
    if job is None:
        return jsonify({
            'result': 'fail',
            'msg': '参数错误'
        })
    job = convert_characters(job)
    data = get_data(job)
    if data.empty:
        return jsonify({
            'result': 'fail',
            'msg': '数据不存在'
        })

    # 处理cityString
    data['cityString'] = data['cityString'].str.split('·').str[0]
    city_counts = data['cityString'].dropna().value_counts().sort_values(ascending=False)

    # 处理degreeString
    degree_counts = data['degreeString'].dropna().value_counts().sort_values(ascending=False)

    # 处理companyTypeString
    companytype_counts = data['companyTypeString'].dropna().value_counts().sort_values(ascending=False)

    # 将 'issueString' 列转换为 datetime 类型
    data['issueDateString'] = pd.to_datetime(data['issueDateString'])

    # 创建一个新的 DataFrame，其中包含 'issueString' 列的年份和月份
    df_date = data['issueDateString'].dt.to_period('M')

    # 对年份和月份进行分组，并计算每个组的大小
    date_counts = df_date.value_counts()

    # 按降序排序
    date_counts = date_counts.sort_values(ascending=True)
    date_counts.index = date_counts.index.strftime('%Y-%m')

    city_counts = city_counts.to_dict()
    degree_counts = degree_counts.to_dict()
    companytype_counts = companytype_counts.to_dict()
    date_counts = date_counts.to_dict()
    city_counts = {k: v for k, v in city_counts.items() if k != ''}
    city_counts_keys = list(city_counts.keys())
    city_counts_values = list(city_counts.values())
    date_counts = {k: v for k, v in date_counts.items() if k != ''}
    date_counts_keys = list(date_counts.keys())
    date_counts_values = list(date_counts.values())
    return jsonify({
        'result': 'success',
        'city_counts_key': city_counts_keys,
        'city_counts_values': city_counts_values,
        'degree_counts': {k: v for k, v in degree_counts.items() if k != ''},
        'companytype_counts': {k: v for k, v in companytype_counts.items() if k != ''},
        'date_counts_key': date_counts_keys,
        'date_counts_values': date_counts_values
    })


# 登记数据
@data_api.route('/register_data', methods=['POST'])
@jwt_required()
def register_data():
    job = request.json.get('job', None)
    if job is None:
        return jsonify({
            'result': 'success',
        })
    job = convert_characters(job)

    # 创建数据库连接
    conn, cursor = init_database()
    # 先查询
    cursor.execute('select * from job51_crawl where jobTitle = "%s"' % job)
    res = cursor.fetchall()
    if res:
        cursor.close()
        conn.close()
        return jsonify({
            'result': 'success',
            'msg': '数据已存在'
        })
    res = cursor.execute('INSERT INTO job51_crawl(jobTitle) VALUES ("%s")' % job)

    # 关闭数据库连接
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            'result': 'success',
        })
    else:
        return jsonify({
            'result': 'fail',
        })
