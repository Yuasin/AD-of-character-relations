from flask import Flask, render_template
from flask import send_file  # 跳转至静态html
from analysis.buildNet import buildNet


# 配置Flask路由，使得前端可以访问服务器中的静态资源
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            )


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


if __name__ == '__main__':
    # 全局变量
    all_name = {}
    adjacency_list = {}
    all_name, adjacency_list = buildNet()
    app.run(debug='true')

