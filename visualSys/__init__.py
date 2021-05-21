import os
from flask import Flask, render_template
from flask import send_file  # 跳转至静态html
from flask import flash, request, redirect, url_for, send_from_directory, jsonify
from analysis.buildNet import buildNet
from analysis.hierarchyCluster import cluster_hierarchy
from analysis.buildJson import buildJson
from urllib.parse import urlparse, urljoin

from datetime import timedelta


# 文件上传保存路径
UPLOAD_FOLDER = './static/book'


# 配置Flask路由，使得前端可以访问服务器中的静态资源
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# 主页
@app.route('/')
def hello():
    global all_name
    # print(all_name)
    return send_file('templates/main.html')


# 展示射雕英雄传
@app.route('/CondorHeroes')
def show_example(name=None):
    global all_name, adjacency_list
    all_name, adjacency_list = buildNet('CondorHeroes')
    # print("修改后全局变量" + str(all_name))
    return render_template('example.html', name=name)

# 指定展示特定的书籍
# 获取该书籍的人物列表以及邻接表
@app.route('/book<name>')
def look_book(name=None):
    global all_name,adjacency_list
    all_name,adjacency_list = buildNet(name)
    print("该书籍人物列表"+name)
    return render_template('example.html', name=name)

# 层次聚类
@app.route('/cluster')
def hierarchycluster():
    clusterNum = request.args.get('num', 5, type=int)
    print("层次聚类测试" + str(clusterNum))
    global all_name, adjacency_list
    combos_tree, labels = cluster_hierarchy(all_name, adjacency_list, clusterNum)
    data_list = buildJson(all_name, adjacency_list, combos_tree, labels)
    return jsonify(content=data_list)

# 查看更多页面
@app.route('/more', methods=['GET'])
def look_more():
    # 获取当前已经存在后端的所有书籍
    all_book = os.listdir(app.config['UPLOAD_FOLDER'])
    print(all_book)
    # 将书籍列表附带名字传递回前端
    return render_template('morebook.html', test = all_book)

# 文件、人物列表上传相关
@app.route('/more', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'corpus' not in request.files:
            flash('未上传文本')
            return redirect(request.url)
        if 'namelist' not in request.files:
            flash('未上传人物列表')
            return redirect(request.url)
        bookname = request.form['bookname']
        print(bookname)
        file = request.files['corpus']
        namelist = request.files['namelist']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file 文本')
            return redirect(request.url)
        if namelist.filename == '':
            flash('No selected file 人物列表')
            return redirect(request.url)

        # 创建书籍目录
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], bookname))
        # 储存语料与人物列表
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], bookname, 'corpus.txt'))
        if namelist:
            namelist.save(os.path.join(app.config['UPLOAD_FOLDER'], bookname, 'namelist.txt'))
    return redirect(request.url)


# 函数功能，传入当前url 跳转回当前url的前一个url
def redirect_back(backurl, **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(backurl, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


if __name__ == '__main__':
    # 全局变量
    all_name = {}
    adjacency_list = {}
    all_name, adjacency_list = buildNet('CondorHeroes')
    app.run(debug='true')
