from flask import Flask, request, render_template, session, jsonify
import asyncio
import hashlib
import os
import httpx

import random
from datetime import datetime
from flask_cors import CORS

import data_func


headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'X-API-Key':    'chv_nAXZ_c576a6c529f9042626b47a487d978a727a76fd8299cb3f2fc7fea17498d99bb904ca7a30e82b60a5c675d0dc0787174bbdbdc1fa61ad65951b068b3adee985c6',
  }
app = Flask(__name__)
CORS(app, resources=r'/*')
# Connect to the MySQL database
app.secret_key = os.urandom(24) # 设置密钥
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 设置Session过期时间


@app.route('/')
async def index():
  print("200")
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
async def upload():
  success = False
  data = request.get_json()
  
  pic = data['base64']
  tags = data['tags']
  uploader=data['uploader']
  tag_str = ",".join(tags)

  for p in pic:
    d = {"source": p, "format": "txt"}
    async with httpx.AsyncClient() as client:
      res = await client.post("https://imgloc.com/api/1/upload", headers=headers, data=d)
      url = res.text
    if url !="重复上传": 
      success= await data_func.submit_emotic(url,tag_str,uploader)
    else:
        success = False
  message = 'success' if success else 'failed'
  print(message)
  return message

@app.route('/test/upload', methods=['POST'])
async def tupload():
  success = False
  data = request.get_json()
  pic = data['base64']
  tags = data['tags']
  uploader=data['uploader']
  #tag_str = ",".join(tags)
  for p in pic:
    d = {"source": p, "format": "txt"}
    async with httpx.AsyncClient() as client:
      res = await client.post("https://imgloc.com/api/1/upload", headers=headers, data=d)
      url = res.text     
    if url !="重复上传": 
        await data_func.upload_emotic(url,tags,uploader)
        success = True
    else:
        success = False
  message = 'success' if success else 'failed'
  print(message)
  return message

@app.route('/random_emotic', methods=['POST'])
@app.route('/random_emotic/<keyword>', methods=['GET'])
async def emoji(keyword):
  if request.method == 'GET':
    return await data_func.random_emotic(keyword)

  if request.method == 'POST':
    data = request.get_json()   
    keyword = data['keyword']
    forbidden_tag = data['forbidden_tag']
    return await data_func.random_emotic(keyword,forbidden_tag)
      
@app.route('/admin/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # 对密码进行md5加密

    # 判断用户名和密码是否正确
    if username == 'admin' and password == 'e10adc3949ba59abbe56e057f20f883e':
        session.permanent = True # 设置Session永久有效
        session['username'] = username # 保存登录状态
        session['is_login'] = True
        return jsonify({'code': 200, 'msg': '登录成功'})
    else:
        return jsonify({'code': 401, 'msg': '用户名或密码错误'})


if __name__ == '__main__':
    asyncio.run(data_func.init_db())
    app.run(host='0.0.0.0', port=81)


