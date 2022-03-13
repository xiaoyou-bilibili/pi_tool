import wx
import tool.photo as photo


# 照片展示
class PhotoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # 获取整个显示屏的高度和宽度
        self.timer = None
        size = wx.DisplaySize()
        # self.width = size[0]
        # self.height = size[1]
        self.height = 340
        self.width = 480
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
        dc.DrawBitmap(self.bmp, 0, int((self.height - photo.get_img_height()) / 2), True)

    # 关闭窗口
    def close_window(self, event):
        self.Close()
        self.Destroy()

    # 照片展示器，展示我们所有的照片
    def tool_photo(self):
        # 先显示第一个图片
        self.set_background()
        # 绑定一个定时器事件
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_photo, self.timer)
        # 10s更换一次图片
        self.timer.Start(10000)

    # 图片定时显示
    def timer_photo(self, evt):
        # 显示背景图片
        self.set_background()

    # 设置背景图片
    def set_background(self):
        # 对图片进行缩放，方便我们全屏显示
        self.bmp = photo.get_img_bitmap(self.width)
        # 设置一下背景颜色，让多余部分显示为黑色
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        # 刷新图片
        self.Refresh()
