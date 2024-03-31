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
                "result": "success",
                "access":access_token,
                "refresh":refresh_token,
                "user":data
            })
    else:
        return jsonify({
            "result": "false",
            "msg": "用户名或密码错误"
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
            "result": "false",
            "msg": "用户已存在"
        })

    res = cursor.execute('INSERT INTO User(username, password, password_question, password_answer) VALUES ("%s", "%s", "%s", "%s")' % (username, password, password_question, password_answer))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            "result": "success",
        })
    else:
        return jsonify({
            "result": "false",
            'msg': '注册失败'
        })

@user_api.route('/get_info', methods=['GET'])
@jwt_required()
def get_info():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    cursor.execute('SELECT * FROM User WHERE username="%s"' % current_user)
    try:
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        if data:
            return jsonify({
                "result": "success",
                "data": {
                    'username': data[0][0],
                    'name': data[0][1],
                    'gender': data[0][3],
                    'age': data[0][4],
                    'major': data[0][5],
                    'interest_position': data[0][6],
                    'interest_city': data[0][9],
                    'education': data[0][10],
                    "avatar": data[0][11]
                }
            })
        return jsonify({
            "result": "false",
            "data": '用户不存在'
        })
    except:
        return jsonify({
            "result": "false",
            "msg": "未知错误"
        })

@user_api.route('/get_status', methods=['GET'])
@jwt_required()
def get_status():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    cursor.execute('SELECT * FROM User WHERE username="%s"' % current_user)
    try:
        data = cursor.fetchall()[0]
        conn.commit()
        cursor.close()
        conn.close()
        for d in data:
            if not d:
                return jsonify({
                    "result": "success",
                    "data": '未完善'
                })
    except:
        return jsonify({
            "result": "false",
            "msg": "未知错误"
        })

@user_api.route('/judge_user', methods=['POST'])
def judge_user():
    username = request.json.get("username", None)
    conn, cursor = init_database()
    user = cursor.execute('SELECT * FROM User WHERE username="%s"' % username)
    conn.commit()
    cursor.close()
    conn.close()
    if user:
        return jsonify({
            "result": "success",
            "msg": "用户存在"
        })
    else:
        return jsonify({
            "result": "false",
            "msg": "用户不存在"
        })