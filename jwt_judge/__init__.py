# -*- coding: utf-8 -*-            
# @Time : 2024/4/29 上午12:11
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm
# 用于判断身份

from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from sql_operation import init_database
from flask import jsonify


def user_jwt_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        # 执行一些额外的检查
        current_user = get_jwt_identity()
        conn, cursor = init_database()
        cursor.execute('select * from User where username = "%s"' % current_user)
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if current_user == user[0]:
            return fn(*args, **kwargs)

        return jsonify({"msg": "Missing user identity"}), 401

    return wrapper


def admin_jwt_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):

        # 执行一些额外的检查
        current_user = get_jwt_identity()
        conn, cursor = init_database()
        cursor.execute('select * from admin where username = "%s"' % current_user)
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if current_user == admin[0]:
            return fn(*args, **kwargs)

        return jsonify({"msg": "Missing user identity"}), 401

    return wrapper
