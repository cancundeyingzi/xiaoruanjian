import re
import threading
from os import system
from flask import Flask, render_template, request, make_response
import time
import requests
lock = threading.Lock()
app = Flask(__name__)

system("title 自动更新stun网址/header显示-v3.1")
print("自动更新stun网址/header显示-v3.1 by残存の影子")
# request都放这边吧
def 更新 (更新项目,更新内容):
    with lock:
        lineList = []
        with open('./index.html', 'r', encoding='utf-8') as r:
            while True:
                line=r.readline()
                if not line:
                    print("读取完毕或读取错误")
                    break
                elif 更新项目 in line:
                    print("更新前", line)
                    new=re.sub(r'[\w-]+(?:\.[\w-]+)+:\d{1,5}\/?',更新内容,line)#new=re.sub(r'(?:https?:\/\/)?[\w-]+(?:\.[\w-]+)+:\d{1,5}\/?',更新内容,line)
                    lineList.append(new)
                    print("更新后",new)
                elif 更新项目 not in line:
                    lineList.append(line)
        #print(lineList)
        with open('./index.html', 'w', encoding='utf-8') as w:
            for i in lineList:
                w.write(i)


@app.route('/post/', methods=['GET', 'POST'])
def post表单提交():
    if request.method == 'GET':
        return render_template("index6.html")
    elif request.method == 'POST':
        print(request.get_data().decode('utf8'))
        更新项目 = request.get_json()['更新项目']
        更新内容 = request.get_json()['更新内容']
        更新 (更新项目,更新内容)
    html = requests.get(
        'http://www.pushplus.plus/send?token=xxxxxx&title=net打洞变化&content=' + request.get_json()['时间']+更新项目+更新内容+ '&template=html')
    # print(html.text)
    return str(request.get_data())


@app.route('/')
def get_headers():
    name = str(request.headers)
    ip = request.remote_addr
    name = time.asctime() + ":</br>\n" + name.replace('\r', '</br>')
    name = name + ' request.remote_addr' + ip + "</br>\n"  # nginx反代后127001
    name = name + 'HTTP_X_REAL_IP' + request.environ.get('HTTP_X_REAL_IP',
                                                         request.remote_addr) + "</br>\n"  # nginx反代后正常,但是穿透不正常
    name = name + 'request.access_route[0]' + request.access_route[0] + "</br>\n"  # nginx反代后正常,但是穿透不正常
    name = name + "header显示,使用python-flask,by残存的影子"
    print(name)
    return name


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5555,  # 5999-6669
        debug=True,
        threaded=True
    )
