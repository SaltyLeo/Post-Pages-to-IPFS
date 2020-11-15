# -*- coding: utf-8 -*-
import time,os,sys,random,requests
from flask import Flask
from flask import stream_with_context
from flask import render_template
from flask import request
from flask import Response
from flask import abort
from flask import url_for
from flask import redirect
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app=Flask(__name__,static_url_path='/static/',static_folder = 'static')
app.secret_key = *your_secret_key* #                                                     【随机密钥】
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

#————————————————————————函数————————————————————————

def get_rip():#获取ip
    headers_list = request.headers.getlist("X-Forwarded-For")
    rip = headers_list[0] if headers_list else request.remote_addr
    return rip

def ipfs_upload(file_path):#上传到IPFS                  #待优化为原生命令
    curl_cmd = '/usr/local/bin/ipfs add /root/ipfs-md-post/%s '%file_path#           【根据你的实际地址修改】
    del_cmd = 'rm /root/ipfs-md-post/%s '%file_path#                                 【根据你的实际地址修改】
    result = os.popen(curl_cmd)
    qmhash_list = list(result)
    qmhash = qmhash_list[0].replace('added ','').replace('%s'%file_path,'').replace('\n','').replace(' ','')
    os.popen(del_cmd)
    return qmhash

def get_rs(num):#获取指定长度(num)随机字符
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789'
    li = random.sample(s,num)
    return ''.join(li)

def save2file(name,html):#保存到文件                   #待优化为 内存文件
    fileObject = open('%s'%name, 'a')#将获取到的json保存
    fileObject.write(html)
    fileObject.close()

def now_time():#时间戳
    nt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    nt = str(nt)
    return nt

def pc(post):#生成HTML   #时间戳无法直接加入str #       待优化
    times = now_time()
    head='<!DOCTYPE html><html lang="zh-CN"><head><title>Post-Pages-to-IPFS</title><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1" /><link rel="apple-touch-icon" sizes="76x76" href="https://post.ipfs.uno/static/img/logo.png"><link rel="icon" type="image/png" href="https://post.ipfs.uno/static/img/logo.png"><link rel="stylesheet" href="https://post.ipfs.uno/static/css/bootstrap.min.css"  add_header Access-Control-Allow-Origin *;><link rel="stylesheet" href="https://post.ipfs.uno/static/css/easy-markdown.min.css"  add_header Access-Control-Allow-Origin *;><style>.easy-markdown ul,.easy-markdown ol{margin:0}.easy-markdown ul,.easy-markdown ol{padding-inline-start:30px;}body::-webkit-scrollbar{width:6px;height:6px;background-color:#f5f5f5}body::-webkit-scrollbar-track{-webkit-box-shadow:inset 0 0 6px #D3D3D3;border-radius:10px;background-color:#f5f5f5}body::-webkit-scrollbar-thumb{height:20px;border-radius:10px;-webkit-box-shadow:inset 0 0 6px rgba(0,0,0,0.3);background-color:#555}</style></head><body><div class="container" ><div class="row"><div class="col" style="margin-left: 10px; margin-right: 10px;">'
    footer1='</div></div></div><div style="text-align:center;color: #777;font-size: 70%;border-top: 1px solid #e5e5e5;padding-top: 5px;">生成时间:'
    footer2='</br>此文档由用户自行编写，经<a href="https://github.com/SaltyLeo/Post-Pages-to-IPFS/">『Post-Pages-to-IPFS』</a>生成，托管于IPFS网络。</div></body></html>'
    allhtml = """%s%s%s%s%s"""%(head,post,footer1,times,footer2)
    return allhtml

def replace_blankk(rt):#删除所有【连续5个空格】和【换行符】
    rt = rt.replace('     ','').replace('\n','')
    return rt

def post_2_ipfs(html):#IPFS 上传流程
    html_name = get_rs(5)
    html_source = replace_blankk(html)
    html_save2file = save2file(html_name,html_source)
    html_Qmhash = ipfs_upload(html_name)
    return html_Qmhash

def check_hash(qmhash):#检查 Qmhash 是否合法
    qmhash_len = 46
    if len(qmhash) != 46:
        return False
    else:
        if qmhash.isalnum() == True:
            return True
        else:
            return False

#————————————————————————路由————————————————————————

@app.route('/')#首页
@limiter.limit("1/second",get_rip,error_message='请求太快了哦~')
def index():
    return render_template("index.html")

@app.route('/post',methods=['GET', 'POST'])# 发布页
@limiter.limit("2/minute",get_rip,error_message='每分钟只可以 Post 2次哦~')
def post():
    if request.method == 'POST':
        post = request.form["post"]
        try:
            checkbox1 = request.form["checkbox1"]
            if checkbox1 == 'on':
                allhtmls = pc(post)
                post_down = post_2_ipfs(allhtmls)
                return redirect("https://post.ipfs.uno/check/%s"%str(post_down)) # 【根据你的实际地址修改】
            else:
                return redirect("/")
        except:
            return redirect("/")

    else:
        return redirect("/")

@app.route('/check/<Qmhash>')# 查询页
@limiter.limit("1/second",get_rip,error_message='请求太快了哦~')
def check(Qmhash):
    if check_hash(Qmhash) == True:
        return replace_blankk(render_template("check.html",Qmhash=Qmhash))
    else:
        return redirect("/")

@app.errorhandler(404)
def error(xx):
    return redirect("/")

if __name__=="__main__":
    app.run(host="127.0.0.1",port=9902,debug=True)  
