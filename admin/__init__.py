# -*- coding: utf-8 -*-            
# @Time : 2024/4/29 上午12:08
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from sql_operation import init_database
import os
from werkzeug.utils import secure_filename

admin_api = Blueprint('admin', __name__)


# 使用刷新token获取新的访问token
@admin_api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username is None or password is None:
        return jsonify({
            'result': 'fail',
            'msg': '参数错误'
        })
    conn, cursor = init_database()
    cursor.execute('select * from admin where username = "%s"' % username)
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    if admin is None:
        return jsonify({
            'result': 'fail',
            'msg': '用户不存在'
        })
    if password == admin[1]:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return jsonify({
            'result': 'success',
            'access_token': access_token,
            'refresh_token': refresh_token
        })
