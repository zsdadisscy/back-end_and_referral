# -*- coding: utf-8 -*-            
# @Time : 2024/3/26 20:27
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sql import init_database

user_api = Blueprint('user', __name__)

from werkzeug.security import generate_password_hash, check_password_hash

# 加密密码
def set_password(password):
    '''
    :param password: 带加密的密码，如123456
    :return: 加密的密码：pbkdf2:sha256:150000$0koyI6Eb$cff6e1b193381f5891fc1cf7b87b1b4dab33869aa5490a7f935579e47c7666cf
    '''
    password = generate_password_hash(password)
    return password


def check_password(password, pwhash):
    '''
    :param password: 字符串密码，如123456
    :param pwhash: 加密后的密码，存在用户表中的hash值
    :return: Ture or False
    '''
    return check_password_hash(password=password, pwhash=pwhash)


# 用户登录函数
@user_api.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    password = set_password(password)[:244]
    # cursor, conn = None, None
    conn, cursor = init_database()
    user = cursor.execute('SELECT * FROM User WHERE username="%s" AND password="%s"'% (username, password))
    # cursor.execute('INSERT INTO User(username, password, gender, education) VALUES ("admin1", "admin1", "男", "本科");')
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(
            {
                "success": True,
                "access_token":access_token,
                "user":data
            })
    else:
        return jsonify({
            "success": False,
        })


@user_api.route('/register', methods=['POST'])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not (username or password):
        return jsonify(msg="用户名或密码不能为空")
    confirm_password = request.json.get("confirm_password", None)
    if password != confirm_password:
        return jsonify(msg="两次密码不一致")
    conn, cursor = init_database()
    password = set_password(password)[:244]
    res = cursor.execute('INSERT INTO User(username, password) VALUES ("%s", "%s")' % (username, password))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        access_token = create_access_token(identity=username)
        return jsonify({
            "success": True,
            "access_token": access_token,
        })
    else:
        return jsonify({
            "success": False,
        })