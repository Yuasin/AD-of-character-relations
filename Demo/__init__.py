import os
from flask import Flask, render_template
from flask import send_file  # 跳转至静态html
from flask import flash, request, redirect, url_for, send_from_directory
from analysis.buildNet import buildNet


UPLOAD_FOLDER = './static/book'
# 配置Flask路由，使得前端可以访问服务器中的静态资源
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    global all_name
    print(all_name)
    return send_file('templates/main.html')


@app.route('/CondorHeroes')
def show_example(name=None):
    global all_name
    print("修改后全局变量" + str(all_name))
    return render_template('example.html', name=name)


@app.route('/more', methods=['GET'])
def look_more():

    return render_template('morebook.html')


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

if __name__ == '__main__':
    # 全局变量
    all_name = {}
    adjacency_list = {}
    all_name, adjacency_list = buildNet()
    app.run(debug='true')
