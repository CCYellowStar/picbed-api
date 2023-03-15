from flask import Flask, render_template, request, jsonify
from replit import db
import requests
import random

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
  success = False
  data = request.get_json()
  for da in data:
    pic = da['base64']
    tag = da['name']
    headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
      'X-API-Key':
      'chv_nAXZ_c576a6c529f9042626b47a487d978a727a76fd8299cb3f2fc7fea17498d99bb904ca7a30e82b60a5c675d0dc0787174bbdbdc1fa61ad65951b068b3adee985c6',
    }
    d = {"source": pic, "format": "txt"}
    try:
      res = requests.post("https://imgloc.com/api/1/upload",
                          headers=headers,
                          data=d)
      txt = res.text
      q = db.prefix(tag)
      if not q:
        db[tag] = txt
      else:
        db[tag + str(len(db.prefix(tag)))] = txt
      success = True
    except:
      success = False
      pass

  message = '上传成功！' if success else '上传失败，请重试！'
  print(message)
  return jsonify({'success': success, 'message': message})


@app.route('/<keyword>')
def emoji(keyword):
  q = db.prefix(keyword)
  if q:
    res = db[db.prefix(keyword)[random.randint(0,
                                               len(db.prefix(keyword)) - 1)]]
    return res
  else:
    # 如果没有找到对应的表情包，则从指定范围内返回一张随机表情包，并将该关键字单独存储记录下来以便人工添加。
    return db[random.sample(db.keys(), 1)[0]]


app.run(host='0.0.0.0', port=81)
