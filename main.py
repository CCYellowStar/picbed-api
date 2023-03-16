from flask import Flask, render_template, request, jsonify
import sqlite3
import requests
import random

app = Flask(__name__)

# Connect to the MySQL database
conn = sqlite3.connect("my_emojis")
cursor = conn.cursor()
cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='emojis' ''')
if cursor.fetchone()[0] == 0:
    cursor.execute('''CREATE TABLE emojis (tag text, url text)''')

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
  success = False
  conn = sqlite3.connect('my_emojis')
  cursor = conn.cursor()
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
      cursor.execute("INSERT INTO emojis (tag, url) VALUES (?, ?)", (tag, txt))
      success = True
    except:
      success = False
      pass
  conn.commit()
  conn.close()
  message = '上传成功！' if success else '上传失败，请重试！'
  print(message)
  return jsonify({'success': success, 'message': message})


@app.route('/<keyword>')
def emoji(keyword):
  conn = sqlite3.connect('my_emojis')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM emojis WHERE tag LIKE ?", ('%' + keyword + '%', ))
  result = cursor.fetchall()
  if len(result) > 0:
    res = result[random.randint(0, len(result) - 1)][1]
    conn.close()
    return res
  else:
    cursor.execute("SELECT * FROM emojis")
    data = cursor.fetchall()
    conn.close()
    return data[random.randint(0, len(data) - 1)][1]


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
