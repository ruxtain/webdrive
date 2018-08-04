"""
    和 django 本身关系比较远的函数。
    不依赖 django 环境运行
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import os

def get_captcha_text():
    """
        产生不重复的随机四位验证码
    """
    chars = list(string.ascii_uppercase + string.digits)
    return random.sample(chars, 4)

def get_captcha_image(captcha_text):
    """
        captcha_text: 长度为 4 的字母或者数字字符串
        返回一个验证码图片对象
    """

    size = (120, 30)

    #定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片
    img1=Image.new(mode="RGB",size=size,color=(255,255,255))

     #实例化一支画笔
    draw1=ImageDraw.Draw(img1,mode="RGB")

    #定义要使用的字体，先获取字体文件的路径
    app_dir = os.path.dirname(__file__)
    font_path = os.path.join(app_dir, 'static/myapp/fonts/Andale_Mono')
    font1 = ImageFont.truetype(font_path, 25)

    for i in range(4):

        char1 = captcha_text[i]
        #每循环一次重新生成随机颜色
        color1=(random.randint(0,20),random.randint(0,20),random.randint(0,20))
        
        #把生成的字母或数字添加到图片上
        #图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
        draw1.text([i*24,0],char1,fill=color1,font=font1)

    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img1 = img1.transform(size, Image.PERSPECTIVE, params)
    img1 = img1.filter(ImageFilter.EDGE_ENHANCE_MORE)        
    return img1


if __name__ == '__main__':
    """ 测试代码 """
    captcha_text = get_captcha_text()
    img1 = get_captcha_image(captcha_text)
    with open("pic.png","wb") as f:
        img1.save(f,format="png")

    
