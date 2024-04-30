# -*- coding: utf-8 -*-            
# @Time : 2024/3/26 20:27
# @name: scy
# @FileName: __init__.py.py
# @Software: PyCharm
from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from sql_operation import init_database
import os
from werkzeug.utils import secure_filename
from jwt_judge import user_jwt_required

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
    user = cursor.execute('SELECT * FROM User WHERE username="%s" AND password="%s"' % (username, password))
    # cursor.execute('INSERT INTO User(username, password, gender, education) VALUES ("admin1", "admin1", "男", "本科");')
    conn.commit()
    conn.close()
    cursor.close()
    if user:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return jsonify(
            {
                "result": "success",
                "access": access_token,
                "refresh": refresh_token,
            })
    else:
        return jsonify({
            "result": "false",
            "msg": "用户名或密码错误"
        })


# 注册
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

    res = cursor.execute(
        'INSERT INTO User(username, password, password_question, password_answer) VALUES ("%s", "%s", "%s", "%s")' % (
        username, password, password_question, password_answer))
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


# 获取用户信息
@user_api.route('/get_info', methods=['GET'])
@user_jwt_required
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


# 判断是否需要完善用户信息
@user_api.route('/get_status', methods=['GET'])
@user_jwt_required
def get_status():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    cursor.execute('SELECT * FROM User WHERE username="%s"' % current_user)
    try:
        data = cursor.fetchall()[0]
        for d in data:
            if not d:
                return jsonify({
                    "result": "success",
                    "data": '未完善'
                })
        return jsonify({
            "result": "success",
            "data": '已完善'
        })
    except:
        return jsonify({
            "result": "false",
            "msg": "未知错误"
        })
    finally:
        conn.commit()
        cursor.close()
        conn.close()


# 判断用户是否存在
@user_api.route('/judge_user', methods=['POST'])
def judge_user():
    username = request.json.get("username", None)
    conn, cursor = init_database()
    user = cursor.execute('SELECT * FROM User WHERE username="%s"' % username)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if user:
        return jsonify({
            "result": "success",
            "password_question": data[0][7],
            "msg": "用户存在"
        })
    else:
        return jsonify({
            "result": "false",
            "msg": "用户不存在"
        })


# 判断jwt是否有效
@user_api.route('/judge_online', methods=['GET'])
@user_jwt_required
def judge_online():
    print(request)
    return jsonify({
        'result': 'success'
    })


# 验证密保问题
@user_api.route('/validation_secure', methods=['POST'])
def validation_secure():
    username = request.json.get("username", None)
    password_answer = request.json.get('password_answer', None)
    conn, cursor = init_database()
    user = cursor.execute(
        'SELECT * FROM User WHERE username="%s" AND password_answer="%s"' % (username, password_answer))
    conn.commit()
    cursor.close()
    conn.close()
    if user:
        return jsonify({
            "result": "success",
        })
    else:
        return jsonify({
            "result": "false",
        })


# 利用密保修改密码
@user_api.route('/secure_passwd', methods=['POST'])
def secure_passwd():
    username = request.json.get("username", None)
    password_answer = request.json.get('password_answer', None)
    password = request.json.get('password', None)
    confirm_password = request.json.get('confirm_password', None)
    if not password:
        return jsonify(
            {
                'result': "false",
                'msg': '密码不能为空'
            }
        )
    if password != confirm_password:
        return jsonify(
            {
                'result': 'false',
                'msg': '两次密码不一致'
            }
        )
    conn, cursor = init_database()
    user = cursor.execute(
        'SELECT * FROM User WHERE username="%s" AND password_answer="%s"' % (username, password_answer))
    if not user:
        return jsonify({
            'result': 'false',
            'msg': "用户不存在或者密保答案错误"
        })
    res = cursor.execute('UPDATE User SET password = "%s" WHERE username = "%s"' % (password, username))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            'result': 'success'
        })
    return jsonify({
        'result': 'false',
        'msg': '修改密码失败，请稍后再试'
    })


# 用户修改密码
@user_api.route('/mod_passwd', methods=['POST'])
@user_jwt_required
def mod_passwd():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    old_password = request.json.get('old_password', None)
    new_password = request.json.get('new_password', None)
    confirm_new_password = request.json.get('confirm_new_password', None)
    if not new_password:
        return jsonify({
            'result': 'false',
            'msg': '新密码不能为空'
        })
    if new_password != confirm_new_password:
        return jsonify({
            'result': 'success',
            'msg': '两次密码不一致'
        })
    res = cursor.execute('SELECT * FROM User WHERE username = "%s" AND password = "%s"' % (current_user, old_password))
    if not res:
        return jsonify({
            'result': 'false',
            'msg': '原密码不正确'
        })
    res = cursor.execute('UPDATE User SET password = "%s" WHERE username = "%s"' % (new_password, current_user))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            'result': 'success'
        })
    return jsonify({
        'result': 'false',
        'msg': '修改失败请稍后再试'
    })


# 修改用户资料
@user_api.route('/mod_info', methods=['POST'])
@user_jwt_required
def mod_info():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    cursor.execute('SELECT * FROM User WHERE username="%s"' % current_user)
    user = cursor.fetchone()
    name = request.json.get('name', user[1])
    gender = request.json.get('gender', user[3])
    age = int(request.json.get('age', user[4]))
    major = request.json.get('major', user[5])
    interest_position = request.json.get('interest_position', user[6])
    interest_city = request.json.get('interest_city', user[9])
    education = request.json.get('education', user[10])
    if name == user[1] and gender == user[3] and age == user[4] and major == user[5] and interest_position == user[
        6] and interest_city == user[9] and education == user[10]:
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            'result': 'success',
            'msg': '未修改任何信息'
        })
    res = cursor.execute(
        "UPDATE User SET name = '%s', gender = '%s', age = '%d', major = '%s', interest_position = '%s',interest_city = '%s',education = '%s' WHERE username = '%s';" %
        (name, gender, age, major, interest_position, interest_city, education, current_user))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            'result': 'success'
        })
    return jsonify({
        'result': 'false',
        'msg': '修改失败，请稍后再试'
    })


# 更新头像
@user_api.route('/upload_avatar', methods=['POST'])
@user_jwt_required
def upload_avatar():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    cursor.execute('SELECT * FROM User WHERE username="%s"' % current_user)
    user = cursor.fetchone()

    avatar = None
    if 'avatar' not in request.files:
        avatar = user[11]
    else:
        avatar = request.files['avatar']

        filename = secure_filename(avatar.filename)
        # 以防文件不存在
        if not os.path.exists('static/avatar'):
            os.makedirs('static/avatar')
        if avatar.filename.find('.png') != -1:
            avatar.save(os.path.join('static/avatar', filename + current_user + '.png'))
            avatar = "http://47.105.178.110:8000/" + os.path.join('user/avatar', filename + current_user + '.png')
        else:
            avatar.save(os.path.join('static/avatar', filename + current_user + '.jpeg'))
            avatar = "http://47.105.178.110:8000/" + os.path.join('user/avatar',
                                                                  filename + current_user + '.jpeg')
    res = cursor.execute(
        "UPDATE User SET  avatar = '%s' WHERE username = '%s';" % (avatar, current_user))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            'result': 'success',
        })
    return jsonify({
        'result': 'false',
        'msg': '修改失败，请稍后再试'
    })


# 获取图片
@user_api.route('/avatar/<path:filename>', methods=['GET'])
def send_image(filename):
    path = os.path.join('static/avatar', filename)
    # 以防文件不存在
    if not os.path.exists(path):
        return jsonify({
            'result': 'false',
            'msg': '文件不存在'
        })
    return send_from_directory('static/avatar', filename)


# 获取用户密保
@user_api.route('/get_secure', methods=['GET'])
@user_jwt_required
def get_secure():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    cursor.execute('SELECT * FROM User WHERE username="%s"' % current_user)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if data:
        return jsonify({
            "result": "success",
            "data": {
                'password_question': data[0][7],
                'password_answer': data[0][8]
            }
        })
    return jsonify({
        "result": "false",
        "msg": "未知错误"
    })


# 修改密保
@user_api.route('/mod_secure', methods=['POST'])
@user_jwt_required
def mod_secure():
    current_user = get_jwt_identity()
    conn, cursor = init_database()
    password_question = request.json.get('password_question', None)
    password_answer = request.json.get('password_answer', None)
    if not password_question or not password_answer:
        return jsonify({
            'result': 'false',
            'msg': '密保问题或者答案不能为空'
        })
    # 判重
    cursor.execute(
        'SELECT * FROM User WHERE username = "%s" AND password_question = "%s" AND password_answer = "%s"' % (
        current_user, password_question, password_answer))
    if len(cursor.fetchall()) >= 1:
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            'result': 'success',
        })
    res = cursor.execute('UPDATE User SET password_question = "%s", password_answer = "%s" WHERE username = "%s"' % (
    password_question, password_answer, current_user))
    conn.commit()
    cursor.close()
    conn.close()
    if res:
        return jsonify({
            'result': 'success'
        })
    return jsonify({
        'result': 'false',
        'msg': '修改失败请稍后再试'
    })
