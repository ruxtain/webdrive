"""
    和 django 本身关系比较近的函数
    需要依赖 django 环境才能运行
    辅助 view 的函数
    如果都定义在 utils，容易出现 utils 里面导入 models
    models 里面导入 utils 的情况，就会报错
"""

from django.conf import settings
from django.db.models import F
from .models import Directory, File, Link, get_media_abspath
import hashlib
import uuid
import os
import re

def handle_repetitive_file(file):
    """
        处理同名的或者重复的文件
        file: File object

        通过遍历看是否有重复路径，如果有重复，则返回带序号的 path
    """

    # 同一个用户的重名文件，与 digest 无关
    if File.objects.filter(owner=file.owner, path=file.path, name=file.name).count() > 1:
        base, ext = os.path.splitext(file.name)
        file.name = '{}_{}{}'.format(base, file.pk, ext)
        file.save()

    Link.add_one(file)


def handle_uploaded_files(files, owner, directory):
    """
        files: 接收到来自用户上传的一组文件
        owner: 用户的 user 对象
        directory: 用户上传文件时所在的目录

        先给一个随机名字，然后一边接收，一边 hash，
        最后用 hash 值来命名文件
    """
    # import pdb; pdb.set_trace()
    media_dir = get_media_abspath() # 所有文件的绝对路径

    for file in files:

        digest = hashlib.sha1()
        temp_filename = os.path.join(media_dir, str(uuid.uuid1())) #　临时文件
        with open(temp_filename, 'wb+') as destination:

            for chunk in file.chunks(chunk_size=1024):
                destination.write(chunk)
                destination.flush()
                digest.update(chunk)

        digest = digest.hexdigest() # hash 对象转字符串
        abspath = os.path.join(media_dir, digest) # 服务器路径，用于储存

        file = File.objects.create( # 返回 file 对象
            name = re.sub(r'[%/]', '_', file.name), # 给用户看的名字，去掉正斜杠和百分号，just in case
                                               # 亲测 mac 下，名字带正斜杠的文件无法被上传
            owner = owner,
            parent = directory, 
            digest = digest,    # 服务器上真正的名字
            path = directory.path, # 用户路径，用户给用户展示，不包含文件名
            size = file._size,
        )

        os.rename(temp_filename, abspath)
        handle_repetitive_file(file)

def set_captcha_to_session(request, captcha_text):
    """
        将 captcha_text 添加到当前用户的 session 中，
        仅在用户 cookies 中不带 sessionid 时创建 session
    """
    sessionid = settings.SESSION_COOKIE_NAME # 默认值就是 sessionid
    key = request.COOKIES.get(sessionid) # sessionid 的值
    if key is None: # 用户没有任何 sessionid
        request.session.create()
        key = request.session.session_key
        
    request.session[key] = {'captcha': ''.join(captcha_text).lower()}

def get_session_data(request, key):
    """
        根据 request 返回对应的 data dict，如果无法返回 data 则返回 {}
    """
    return request.session.get(key)

def set_session_data(request, key, value):
    """
        为 session 新增键值对
    """
    request.session.update({key: value})
    request.session.modified = True