# Webdrive 使用说明
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.png?v=103)](https://opensource.org/licenses/mit-license.php)

仿效 UNIX 文件管理系统，为文件设置一个 original file，一旦有 sha1 摘要的文件上传，则只增加 original file 的计数器，而不占用两份空间。

已有功能：
+ 上传文件，重命名文件
+ 新建目录
+ 下载文件
+ 删除文件
+ 预览文件

TODO：
+ 共享文件，通过短密码下载
+ 限制用户的磁盘空间

Further TODO:
+ 命令行客户端

# 安装

```
pip install -r requirements.txt
# Mac OS 下需要多一步：
brew install libmagic
```
