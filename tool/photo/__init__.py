import os
from io import BytesIO

import wx
from core.net import get_row_data

# 图片坐标地址
img_path = os.path.join(os.getcwd(), "background")
photos = os.listdir(img_path)
photo_index = 1
img_height = 0


# 获取图片,这里执行一下宽度信息，用于图片缩放
def get_img_bitmap(width):
    global photo_index, photos
    # 遍历完图片后重新开始遍历
    if photo_index >= len(photos):
        photo_index = 0
    # 获取文件名称
    filename = os.path.join(img_path, photos[photo_index])
    # 图片顺序
    photo_index += 1
    # wx.Image是一个加载图像的函数wx.BITMAP_TYPE_ANY表示任意类型的图片
    img = wx.Image(filename, type=wx.BITMAP_TYPE_ANY)
    return scale_img(img, width)


# 获取当前图片的高度信息
def get_img_height():
    return img_height


# 缩放图片
def scale_img(img, width):
    global img_height
    # 我们获取一下图片的高度和宽度(这个高度是根据我们屏幕的宽度算出来的，是为了让图片更好展示，避免拉伸)
    img_width = img.GetWidth()
    img_height = int(img.GetHeight() * (width / img_width))
    # 返回一个bitmap对象
    return img.Scale(width, img_height).ConvertToBitmap()


# 显示网络图片
def get_net_bitmap(url, width):
    if url == "":
        return wx.NullBitmap
    # 获取图片的二进制数据
    data = get_row_data(url)
    # 获取IO数据
    stream = BytesIO(data)
    img = wx.Image(stream)
    if img.IsOk():
        return scale_img(img, width)
    else:
        return wx.NullBitmap
