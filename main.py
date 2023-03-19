from flask import Flask, request, jsonify
import asyncio
from db_models import Emojis, Tags, EmojiTag,Submissions
from tortoise import Tortoise
import requests
import random
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/*')
# Connect to the MySQL database



@app.route('/')
def index():
  return


@app.route('/upload', methods=['POST'])
async def upload():
  success = False
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
      if url !="重复上传":
      
        await Submissions.create(url=url, tag=tag_str, submitter=uploader, submission_date=upload_time, status=0)
  
        success = True
      else:
        success = False
    except:
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

async def init_db():
    await Tortoise.init(
        db_url='sqlite://my_emojis.db',
        modules={'models': [__name__]}
    )
    await Tortoise.generate_schemas()   
if __name__ == '__main__':
    asyncio.run(init_db())
    app.run(host='0.0.0.0', port=81)


