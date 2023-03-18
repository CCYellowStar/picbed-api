from flask import Flask, request, jsonify
import sqlite3
import requests
import random
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__, static_folder='static',template_folder='static',static_url_path='/static')
CORS(app, resources=r'/*')
# Connect to the MySQL database
conn = sqlite3.connect("my_emojis")
cursor = conn.cursor()
cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='emojis' ''')
if cursor.fetchone()[0] == 0:
  cursor.execute('''
      CREATE TABLE emojis (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          url TEXT NOT NULL,
          upload_time TEXT NOT NULL,
          uploader TEXT NOT NULL
      )
  ''')
  cursor.execute('''
      CREATE TABLE tags (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          emoji_count INTEGER NOT NULL DEFAULT 0,
          search_count INTEGER NOT NULL DEFAULT 0
      )
  ''')
  cursor.execute('''
      CREATE TABLE emoji_tag (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          emoji_id INTEGER NOT NULL,
          tag_id INTEGER NOT NULL,
          FOREIGN KEY (emoji_id) REFERENCES emojis (id),
          FOREIGN KEY (tag_id) REFERENCES tags (id)
      );
  ''')
  cursor.execute('''
    CREATE TABLE submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        tag TEXT NOT NULL,
        submitter TEXT NOT NULL,
        submission_date TEXT NOT NULL,
        status INTEGER NOT NULL DEFAULT 0
    )
''')



@app.route('/')
def index():
  return


@app.route('/upload', methods=['POST'])
def upload():
  success = False
  conn = sqlite3.connect('my_emojis')
  cursor = conn.cursor()
  data = request.get_json()
  for da in data:
    pic = da['base64']
    tags = da['name']
    uploader=da['uploadername']
    tag_str = ",".join(tags)
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
      url = res.text
      upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      cursor.execute("INSERT INTO submissions (url,tag, submitter, submission_date,status) VALUES (?, ?, ?, ?, ?)", (url, tag_str,uploader,upload_time,0))
      """
      for tag in tags:
        cursor.execute("SELECT * FROM tags WHERE tags = ?", (tag, ))
        result = cursor.fetchall()
        if result is not None:
          tag_id = result[0]
          emoji_count = result[2]
          cursor.execute("UPDATE tags SET emoji_count = ? WHERE id = ?", (emoji_count + 1, tag_id))"""
      conn.commit()
      success = True
    except:
      success = False
      pass
  conn.commit()
  conn.close()
  message = '上传成功！' if success else '上传失败，请重试！'
  print(message)
  return jsonify({'success': success, 'message': message})


@app.route('/random_emotic', methods=['POST'])
@app.route('/random_emotic/<keyword>', methods=['GET'])
def emoji(keyword):
  conn = sqlite3.connect('my_emojis')
  cursor = conn.cursor()
  if request.method == 'GET':
    cursor.execute("SELECT * FROM tags WHERE name = ?", (keyword , ))
    result = cursor.fetchall()
    if len(result) > 0:
      tag_id = result[0]
      cursor.execute("SELECT * FROM emoji_tag WHERE tag_id = ?", (tag_id , ))
      result1 = cursor.fetchall()
      if len(result1) > 0:
        emoji_id = result1[random.randint(0, len(result1) - 1)][1]
        url=cursor.execute("SELECT * FROM emojis WHERE id = ?", (emoji_id , )).fetchall()[0][1]
        conn.close()
        return url
      else:
        cursor.execute("SELECT * FROM emojis")
        data = cursor.fetchall()
        conn.close()
        return data[random.randint(0, len(data) - 1)][1]
    else:
      cursor.execute("SELECT * FROM emojis")
      data = cursor.fetchall()
      conn.close()
      return data[random.randint(0, len(data) - 1)][1]

  if request.method == 'POST': #再解决屏蔽词
    data = request.get_json()
    keyword=data['keyword']
    blocked_tags=data['forbidden_tag']
    cursor.execute("SELECT * FROM tags WHERE name = ?", (keyword , ))
    result = cursor.fetchall()
    if len(result) > 0:
      tag_id = result[0]
      cursor.execute("SELECT * FROM emoji_tag WHERE tag_id = ?", (tag_id , ))
      result1 = cursor.fetchall()
      if len(result1) > 0:
        emoji_id = result1[random.randint(0, len(result1) - 1)][1]
        url=cursor.execute("SELECT * FROM emojis WHERE id = ?", (emoji_id , )).fetchall()[0][1]
        conn.close()
        return url
      else:
        cursor.execute("SELECT * FROM emojis")
        data = cursor.fetchall()
        conn.close()
        return data[random.randint(0, len(data) - 1)][1]
    else:
      cursor.execute("SELECT * FROM emojis")
      data = cursor.fetchall()
      conn.close()
      return data[random.randint(0, len(data) - 1)][1]
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
