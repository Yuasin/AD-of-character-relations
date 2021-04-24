from flask import Flask, render_template
from flask import send_file #跳转至静态html

# 配置Flask路由，使得前端可以访问服务器中的静态资源
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            )

@app.route('/')
def hello():
   return send_file('templates/main.html')


@app.route('/CondorHeroes')
def show_example(name=None):
    return render_template('example.html', name=name)


if __name__ == '__main__':
   app.run(debug='true')