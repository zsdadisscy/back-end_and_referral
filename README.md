# back-end_and_referral


## 大学生就业数据可视化和推荐后端部分

--------------------------------------------------
# 基于Flask和Echarts的大学生就业可视化和推荐系统
本系统为我毕业设计系统的后端部分，前端部分在[front-end_and_referral](https://github.com/zsdadisscy/visualization)

本人水平有限，代码写的不好，有问题请多多指教。

# 项目结构
```
admin 管理员部分代码（由于时间关系，管理员部分实现数据库和登录，jwt实现了身份验证的的不同函数，可以验证用户和管理员，管理员部分将不再更新，实现版本为（cd567b6）））
app 项目主要代码
user 用户部分代码
crawler 爬虫部分代码
    __init__.py 爬取初始化数据
    job51.py 爬取数据主要函数
data_analysis 数据分析部分代码
jwt_judge jwt验证部分代码
recommend 推荐部分代码
sql_operation 数据库操作部分代码
    __init__.py 数据库配置
    job51.sql 职位表（包含数据）
    job51_crawl.sql 待爬取数据表
    job51_record.sql 已经爬取记录表
    jobs51.sql 创建库及表
static 静态文件(前端部分打包）
templates 模板文件(前端部分打包）
```
该系统可以部署在服务器运行，已经试验过了，如果需要部署在服务器，提供[docker.tar](https://pan.baidu.com/s/1GfqdciTLnRd958VA25e7FQ?pwd=8sqs 
)

由于服务器已到期，请不要访问项目中的服务器，如需部署请改为自己服务器ip，目前项目中所有ip都已经改为本地ip：127.0.0.1

# 项目运行
项目基于python3.10，具体版本要求请看requirements.txt
1. 安装依赖
```pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple```
2. 修改数据库配置，在sql_operation文件夹中更改自己的数据库配置
    运行数据库文件，先运行jobs51.sql，最后运行job51.sql
3. 运行项目
```python run.py```


数据库部分由于爬虫每天都在更新，不能保证一直可用，所以提供sql文件

# 未实现
1. 原意是实现数据可是实时爬取
但是服务器ip被封，后期需要可以通过thrift实现本地抓取，或者做ip代理
2. 由于时间关系，管理员部分实现数据库和登录，jwt实现了身份验证的的不同函数，可以验证用户和管理员
，管理员部分将不再更新，实现版本为（cd567b6）

# 少年何惧岁月长，我有代码，你有梦想


--------------------------------
**声明：本项目仅供学习交流使用，不得用于商业用途，如有侵权请联系删除**