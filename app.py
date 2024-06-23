from datetime import timedelta
from flask import Flask, render_template
import user
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import data_analysis
import recommend
import admin

app = Flask(__name__, )
CORS(app)
app.register_blueprint(user.user_api, url_prefix='/user')
app.register_blueprint(data_analysis.data_api, url_prefix='/data')
app.register_blueprint(recommend.recommend_api, url_prefix='/recommend')
app.register_blueprint(admin.admin_api, url_prefix='/admin')

# 设置普通JWT过期时间

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# 设置刷新JWT过期时间

app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['JWT_SECRET_KEY'] = 'hgdfcvuisdhgavoasghu7GJUFu67'
jwt = JWTManager(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
