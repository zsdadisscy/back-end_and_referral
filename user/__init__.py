# -*- coding: utf-8 -*-            
# @Time : 2024/3/26 20:27
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from sql import init_database

user_api = Blueprint('user', __name__)


# 使用刷新token获取新的访问token
@user_api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # 使用刷新token进行验证
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)

# 用户登录函数
@user_api.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

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
        refresh_token = create_refresh_token(identity=username)
        return jsonify(
            {
                "success": True,
                "access":access_token,
                "refresh":refresh_token,
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
    password_question = request.json.get("password_question", None)
    password_answer = request.json.get("password_answer", None)

    if not (username or password):
        return jsonify(msg="用户名或密码不能为空")
    confirm_password = request.json.get("confirm_password", None)
    if password != confirm_password:
        return jsonify(msg="两次密码不一致")
    conn, cursor = init_database()

    # 判断用户名是否存在
    user = cursor.execute('SELECT * FROM User WHERE username="%s"' % username)
    if user:
        return jsonify({
            "success": False,
            "msg": "用户名已存在"
        })

    res = cursor.execute('INSERT INTO User(username, password, password_question, password_answer) VALUES ("%s", "%s", "%s", "%s")' % (username, password, password_question, password_answer))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            "success": True,
        })
    else:
        return jsonify({
            "success": False,
            'msg': '注册失败'
        })