from flask import Flask, request, render_template, session, jsonify
import asyncio
import hashlib
import os
import httpx
from db_models import Emojis, Tags, EmojiTag,Submissions
from tortoise import Tortoise
import random
from datetime import datetime
from flask_cors import CORS
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
  print("up")
  
  pic = data['base64']
  tags = data['tags']
  uploader=data['uploader']
  tag_str = ",".join(tags)
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'X-API-Key':    'chv_nAXZ_c576a6c529f9042626b47a487d978a727a76fd8299cb3f2fc7fea17498d99bb904ca7a30e82b60a5c675d0dc0787174bbdbdc1fa61ad65951b068b3adee985c6',
  }
  for p in pic:
    d = {"source": p, "format": "txt"}
    print("开始请求")
    async with httpx.AsyncClient() as client:
      res = await client.post("https://imgloc.com/api/1/upload", headers=headers, data=d)
      url = res.text

    print("请求完成")
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:   
      if url !="重复上传": 
          await Submissions.create(url=url, tag=tag_str, submitter=uploader, submission_date=upload_time, status=0)
    
          success = True
      else:
          success = False
    except Exception as e:
      print(e)
      success = False
      pass
  message = 'success' if success else 'failed'
  print(message)
  return message

@app.route('/test/upload', methods=['POST'])
async def tupload():
  success = False
  data = request.get_json()
  print("up")
  
  pic = data['base64']
  tags = data['tags']
  uploader=data['uploader']
  #tag_str = ",".join(tags)
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'X-API-Key':    'chv_nAXZ_c576a6c529f9042626b47a487d978a727a76fd8299cb3f2fc7fea17498d99bb904ca7a30e82b60a5c675d0dc0787174bbdbdc1fa61ad65951b068b3adee985c6',
  }
  for p in pic:
    d = {"source": p, "format": "txt"}
    print("开始请求")
    async with httpx.AsyncClient() as client:
      res = await client.post("https://imgloc.com/api/1/upload", headers=headers, data=d)
      url = res.text

    print("请求完成")
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:   
      if url !="重复上传": 
          img,_= await Emojis.get_or_create(url=url, upload_time=upload_time, uploader=uploader)
          for t in tags:
            tag, _ = await Tags.get_or_create(name=t)
            tag.emoji_count += 1
            await tag.save()
            await EmojiTag.create(emoji_id=img.id, tag_id=tag.id)
          success = True
      else:
          success = False
    except Exception as e:
      print(e)
      success = False
      pass
  message = 'success' if success else 'failed'
  print(message)
  return message

@app.route('/random_emotic', methods=['POST'])
@app.route('/random_emotic/<keyword>', methods=['GET'])
async def emoji(keyword):
  if request.method == 'GET':
    tag = await Tags.filter(name=keyword).first()
    if tag:
      emoji_ids = await EmojiTag.filter(tag_id=tag.id).all()
      if emoji_ids:
        emoji_id = emoji_ids[random.randint(0, len(emoji_ids) - 1)].emoji
        url=await Emojis.filter(id=emoji_id).first().url
        return url
      else:
        return "failed"
    else:
      return "failed"

  if request.method == 'POST': #再解决屏蔽词
    pass
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

async def init_db():
    await Tortoise.init(
        db_url='sqlite://my_emojis.db',
        modules={'models': ['db_models']}
    )
    await Tortoise.generate_schemas()   
    print("Tables have been created!")
if __name__ == '__main__':
    asyncio.run(init_db())
    app.run(host='0.0.0.0', port=81)


