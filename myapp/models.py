from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone

import os


def get_media_abspath():
    """
        所有文件都直接放到 media 目录下，不再做不必要的划分，增加麻烦！
    """
    return settings.MEDIA_ROOT


class Directory(models.Model):
    """
        name: 用户能看到的文件目录名. todo: 同级目录下不允许重复
        parent: 上级目录，如果本身是根目录则 parent 为空字符
        path: 用户能看到的相对路径，需要用 get_full_path 才能转换成绝对路径
    """
    name = models.CharField(max_length=256) # 如 / home
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('Directory', null=True, on_delete=models.CASCADE) # 只有根目录没有 parent
    path = models.CharField(max_length=4096, default='')

    def __str__(self):
        return self.name or '/'

    @classmethod
    def create_root_dir(cls, user):
        """
            用户注册时，会同时创建一个根目录对象
        """
        directory = cls.objects.create(
                    name= '/', 
                    owner=user,
                    parent=None,
                    path=''     # 根目录为空字符，方便后续 URL 拼接不出现 // 影响美观
                )
        return directory

    def get_url(self):
        return '/{}/{}'.format(self.owner.username, self.path)


class File(models.Model):
    """
        name:   用户能看到的文件目录名.
                考虑到文件名只是存在于数据库的字段，所以不需要限制命名规则
        digest: 文件的 sha1 摘要，也是文件真正的名字
        owner:  文件所有者
        size:   文件大小
        parent: 上级目录
        path:   相对路径，包含了 digest 作为文件名，和用户自定义的树形结构对应
                但是服务器的储存不按照这个结构存放
                如果对应的话，那么多个File对象映射同一个文件时，下载路径按照 path 来会出错
                此外，path 需要包含用户的根目录，如 user_12，否则用户无法引用到其他用户的文件
                文件的 path 不应该包括文件名，否则会造成改 name 时 path 不能一起改

        links:  被引用的次数，无人使用时才删除
        origin: 是否为第一份文件。计数器都只作用于第一份文件，其他的同 digest 的文件都是硬链接
                如果删除，只将 origin 的 links 减一。
                不过有个问题，那就是硬链接文件的 links 这一栏用不上。
    """

    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField(default=0) 
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE)
    digest = models.CharField(max_length=40) 
    path = models.CharField(max_length=4096, default='')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_full_path(self):
        """ 文件的服务器路径 """
        return os.path.join(get_media_abspath(), self.digest)

    def remove_from_disk(self):
        """ 
            删除磁盘上的文件，而不是只减少计数器+删除 File 对象 
            用于发现重复文件后，清除新添加的文件，保留用户的 File 对象，改写其 path 值
        """
        os.remove(self.get_full_path())

    def get_url(self):
        """
            没有这步判断，根目录下的文件链接会多一条杠。
        """
        if self.path:
            return '/{}/{}/{}'.format(self.owner.username, self.path, self.name)
        else:
            return '/{}/{}'.format(self.owner.username, self.name)

    def get_size(self): # Byte
        """
            make the file size more human-readable
        """
        size = self.size
        if size > 1024**3: # GB
            size = '{:.2f} GB'.format(size/(1024**3))
        elif size > 1024**2: # MG
            size = '{:.2f} MB'.format(size/(1024**2))
        elif size > 1024:
            size = '{:.2f} KB'.format(size/(1024))
        else:
            size = '{:.2f} Bytes'.format(size)
        return size


class Link(models.Model):
    """
        记录文件的摘要和links数
        当用户删除文件时，删掉文件对象，但是不从磁盘删除，
        除非对应的 link 数为0，表示该 hash 值对应的所有文件已经删光，
        此时，从磁盘删除文件

        每次上传文件必然产生两种情况：
            1. 产生一个新的 link 对象
            2. links 值 + 1

        之前把 links 属性放在 File，有一个问题，当记录 links 的文件被删除时，
        这个值就丢失了
    """
    digest = models.CharField(max_length=40, primary_key=True) # 和 digest 绑定，而不是和文件绑定
    links = models.IntegerField() # links 数

    def __str__(self):
        return str(self.links)

    @classmethod
    def add_one(cls, file):
        """
            新增文件后调用。使得计数器加一
            如果对应的 digest 没有计数器，则创建计数器，并 links = 1
        """
        nums = File.objects.filter(digest=file.digest).count()
        link_objects = cls.objects.filter(digest=file.digest)
        if link_objects:
            link = link_objects[0]
            link.links = nums
            link.save()
        else:
            link = cls.objects.create(digest=file.digest, links=nums) # nums 为1

    @classmethod
    def minus_one(cls, file):
        """ 
            删除文件后调用。使得计数器减一
            如果对应的 digest 的计数器为 0，那么从磁盘删除掉这个文件
        """
        link = cls.objects.get(digest=file.digest)
        link.links -= 1
        
        if link.links < 1:
            file.remove_from_disk()
            link.delete()
        else:
            link.save()

        file.delete()
















