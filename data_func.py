import tortoise
from db_models import Emojis, Tags, EmojiTag,Submissions
from tortoise import Tortoise
from datetime import datetime
import random

upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def submit_emotic(
  url:str, tag_str:str, submitter:str,status:int=0
) -> bool:
  """ 提交表情包审核 返回是否成功 """
  try:
    await Submissions.create(url=url, tag=tag_str, submitter=submitter, submission_date=upload_time, status=status)
    return True
  except:
    return False


async def upload_emotic(
  url:str, tags:list, uploader:str
) -> str:
  """ 上传表情包图片 返回图片链接 """
  img,_= await Emojis.get_or_create(url=url, upload_time=upload_time, uploader=uploader)
  for t in tags:
    tag = await Tags.filter(name=t).first()  
    if tag:
      await tag.update_or_create(name=t,defaults={"emoji_count":tag.emoji_count + 1})
    else:
      tag,_= await Tags.get_or_create(name=t,emoji_count=1)
    await EmojiTag.create(emoji_id=img.id, tag_id=tag.id)
  return img.url

async def random_emotic(keyword:list, forbidden_tag:list = None) -> str:
  """ 随机表情包 返回结果图链 """
  tag = await Tags.filter(name=keyword).first()
  if tag:
    await tag.update_or_create(name=keyword,defaults={"search_count":tag.search_count + 1})
    if forbidden_tag:
      emoji_ids = await EmojiTag.filter(tag_id=tag.id).exclude(tag__name__in=forbidden_tag).all()
    else:
      emoji_ids = await EmojiTag.filter(tag_id=tag.id).all()
    if emoji_ids:          
      emoji_id = emoji_ids[random.randint(0, len(emoji_ids)-1)].emoji_id
      url=await Emojis.filter(id=emoji_id).first()
      return url.url
    else:
      return "failed"
  else:
    return "failed"


async def init_db():
    """ 初始化数据库 """
    TORTOISE_ORM_CONFIG = {
        "connections": {
          "default": {
              "engine": "tortoise.backends.sqlite",
              "credentials": {
                      "file_path": "my_emojis.db",
                      "journal_mode":"DELETE"
                  },
          },
          #"default": "sqlite://my_emojis.db?mode=memory&cache=shared"
        },
        "apps": {
            "models": {
                "models": ["db_models"],
                "default_connection": "default",
            },
        },
        "use_tz": True,
        "timezone": "UTC",
        "connections_params": {
            "default": {
                "journal_mode": "DELETE"
            }
        }
    }
  
    await Tortoise.init(
      TORTOISE_ORM_CONFIG
    )
    await Tortoise.generate_schemas() 
    print("Tables have been created!")