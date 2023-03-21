from tortoise import fields
from tortoise.models import Model


class Emojis(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    upload_time = fields.CharField(max_length=255)
    uploader = fields.CharField(max_length=255)
  
    class Meta:
        table =  "emojis"

class Tags(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    emoji_count = fields.IntField(default=0)
    search_count = fields.IntField(default=0)
  
    class Meta:
        table =  "tags"

class EmojiTag(Model):
    id = fields.IntField(pk=True)
    emoji = fields.ForeignKeyField('models.Emojis', related_name='emoji_tag')
    tag = fields.ForeignKeyField('models.Tags', related_name='emoji_tag')
  
    class Meta:
        table =  "emoji_tag"

class Submissions(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    tag = fields.CharField(max_length=255)
    submitter = fields.CharField(max_length=255)
    submission_date = fields.CharField(max_length=255)
    status = fields.IntField(default=0)
  
    class Meta:
        table =  "submissions"

