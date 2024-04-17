# -*- coding: utf-8 -*-            
# @Time : 2024/4/17 下午5:24
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from sql_operation import init_database

recommend_api = Blueprint('recommend', __name__)


# 筛选数据返回
@recommend_api.route('/recommend_data', methods=['GET'])
@jwt_required()
def recommend_data():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    # 查询用户资料
    cursor.execute('select * from User where username = "%s"' % current_user)
    user = cursor.fetchone()
    if not user:
        return jsonify({
            'result': 'fail',
            'msg': '用户不存在'
        })
    # 查询用户推荐数据
    major = user[5]
    position = user[6].split(' ')
    position.append(major)
    city = user[9].split(' ')
    education = user[10]
    if major is None or major == '' or education is None or education == '' or position is None or len(position) == 0 or city is None or len(city) == 0:
        return jsonify({
            'result': 'fail',
            'msg': '用户数据不全无法推荐'
        })
    educaitons = ['其他', '高中', '专科', '本科', '硕士研究生', '博士研究生']
    # 查找education下标
    education_index = educaitons.index(education)
    # 在数据库中查询符合任一项的条件的数据
    data = []
    for cit in city:
        for pos in position:
            for edu in range(education_index, 6):
                cursor.execute(f'select jobName, cityString, provideSalaryString, workYearString, degreeString, companyName, companyTypeString, jobHref, companyHref, industryType from job51 where jobName like "%{pos}%" or jobTitle like "%{pos}%" or cityString like "%{cit}%" or degreeString like "%{educaitons[edu]}%"')
                data += cursor.fetchall()

    # 去除重复的子列表
    data = [list(x) for x in set(tuple(x) for x in data)]

    # 排序
    educaitons = educaitons[education_index:]
    def sort_data(data):
        score = 0
        for cit in city:
            if cit in data[1]:
                score += 1
                break
        for pos in position:
            if pos in data[0]:
                score += 1
                break
        for edu in educaitons:
            if edu in data[4]:
                score += 1
                break
        return score
    data = sorted(data, key=lambda x: sort_data(x), reverse=True)
    return jsonify({
        'result': 'success',
        'data': data[:100]
    })