# picbed-api
Minimalist Python web framework.
https://flask.ccyellowstar.repl.co/

# 接口文档

## 上传接口
### path: /upload
(需求：上传表情包图片，每次接收多张图片的base64(最多9张)，同时接收tags(词条，str list), uploader(上传者，str)字段，返回是否成功)

#### 参数说明：
- 图片文件：base64 (list<str>)
- 词条列表：tags (list<str>)
- 上传者：uploader (str)

#### 返回值说明：
- 成功：status_code=200, 返回值为"success"
- 失败：status_code=400, 返回值为"failed"

## 随机表情包接口
### path: /random_emotic
(需求：随机表情包，接收两个参数：关键词keyword(str)、屏蔽词forbidden_tag(str list)，返回符合条件的图链)

#### 参数说明：
- 关键词：keyword (str)
- 屏蔽词列表：forbidden_tag (list<str>)

#### 返回值说明：
- 成功：status_code=200, 返回值为符合条件的图链(list<str>)
- 失败：status_code=400, 返回值为"failed"

## 管理接口

### 登录接口
#### path: /admin/login
需求：登录接口，接收username和password(md5加密后)，返回是否登录成功，使用session保存状态

#### 参数说明：
- 用户名：username (str)
- 密码(md5加密后)：password (str)

#### 返回值说明:
- 成功: status_code=200, session中保存登录状态(is_login=True)
- 失败: status_code=401, session中保存登录状态(is_login=False)


### 更新记录
#### path: /admin/update
需求: 留空

### 检索记录
#### path: /admin/query
需求: 留空



# 接口文档生成prompt

## 上传接口
### path: /upload
(需求：上传表情包图片，每次接收一张图片(png、gif、jpg等)，同时接收tags(词条，str list), uploader(上传者，str)字段，返回是否成功)

## 随机表情包接口
### path: /random_emotic
(需求：随机表情包，接收两个参数：关键词keyword(str)、屏蔽词forbidden_tag(str list)，返回符合条件的图链)

## 管理接口

### 登录接口
#### path: /admin/login
需求：登录接口，接收username和password(md5加密后)，返回是否登录成功，使用session保存状态

### 更新记录
#### path: /admin/update
需求：

### 检索记录
#### path: /admin/query
需求：
请根据以上信息，帮我编写一份符合需求的接口文档，要求有详细的参数说明，可以重写原格式，结果需要符合标准的接口文档格式
图片每次一张，关键词和屏蔽词均是['word1', 'word2']的形式，session不需要设定过期时间，更新和检索记录先留空