import wx
import os


# 照片展示
class PhotoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # 获取整个显示屏的高度和宽度
        size = wx.DisplaySize()
        # 图片宽度和高度
        self.img_height = None
        self.img_width = None
        self.width = size[0]
        self.height = size[1]
        # 图片坐标地址
        self.img_path = os.path.join(os.getcwd(), "background")
        self.photos = None
        self.photo_index = 1
        self.bmp = None
        # 显示图片
        self.tool_photo()
        self.Bind(wx.EVT_PAINT, self.on_paint)
        # 点击退出pannel
        self.Bind(wx.EVT_LEFT_DOWN, self.close_window)

    # 绘画事件
    def on_paint(self, event=None):
        # 创建画布
        dc = wx.PaintDC(self)
        # 清除画布
        dc.Clear()
        # 绘制图片
        dc.DrawBitmap(self.bmp, 0, int((self.height - self.img_height) / 2), True)

    # 关闭窗口
    def close_window(self, event):
        self.Close()
        self.Destroy()

    # 照片展示器，展示我们所有的照片
    def tool_photo(self):
        # 首先我们获取文件夹下所有的图片
        self.photos = os.listdir(self.img_path)
        # 先显示第一个图片
        self.set_background(os.path.join(self.img_path, self.photos[0]))
        # 创建定时器
        self.timer = wx.Timer(self)
        # 绑定一个定时器事件
        self.Bind(wx.EVT_TIMER, self.timer_photo, self.timer)
        # 设定时间间隔为1000毫秒,并启动定时器
        self.timer.Start(3000)

    # 图片定时显示
    def timer_photo(self, evt):
        # 遍历完图片后重新开始遍历
        if self.photo_index >= len(self.photos):
            self.photo_index = 0
        # print(os.path.join(self.img_path, self.photos[self.photo_index]))
        # 显示背景图片
        self.set_background(os.path.join(self.img_path, self.photos[self.photo_index]))
        self.photo_index += 1

    # 设置背景图片
    def set_background(self, filename):
        # wx.Image是一个加载图像的函数wx.BITMAP_TYPE_ANY表示任意类型的图片
        img = wx.Image(filename, type=wx.BITMAP_TYPE_ANY)
        # 我们获取一下图片的高度和宽度(这个高度是根据我们屏幕的宽度算出来的，是为了让图片更好展示，避免拉伸)
        self.img_width = img.GetWidth()
        self.img_height = int(img.GetHeight() * (self.width / self.img_width))
        # 对图片进行缩放，方便我们全屏显示
        self.bmp = img.Scale(self.width, self.img_height).ConvertToBitmap()
        # 设置一下背景颜色，让多余部分显示为黑色
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        # 刷新图片
        self.Refresh()
