# -*- coding: utf-8 -*-
import wx
import wx.xrc
from tool.photo import get_net_bitmap
from tool.bilibili import get_video_list


class VideoPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(480, 320), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        box_main = wx.BoxSizer(wx.VERTICAL)

        self.grid_video = wx.GridSizer(3, 2, 0, 0)

        box_main.Add(self.grid_video, 1, wx.EXPAND, 5)

        box_menu = wx.BoxSizer(wx.HORIZONTAL)
        self.text_page = wx.StaticText(self, wx.ID_ANY, u"0/0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_page.Wrap(-1)
        box_menu.Add(self.text_page, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btn_pre = wx.Button(self, wx.ID_ANY, u"上一页", wx.DefaultPosition, wx.DefaultSize, 0)
        box_menu.Add(self.btn_pre, 0, wx.ALL, 5)
        self.btn_pre.Disable()

        self.btn_next = wx.Button(self, wx.ID_ANY, u"下一页", wx.DefaultPosition, wx.DefaultSize, 0)
        box_menu.Add(self.btn_next, 0, wx.ALL, 5)
        self.btn_next.Disable()

        self.btn_quit = wx.Button(self, wx.ID_ANY, u"退出", wx.DefaultPosition, wx.DefaultSize, 0)
        box_menu.Add(self.btn_quit, 0, wx.ALL, 5)

        box_main.Add(box_menu, 1, wx.EXPAND, 5)

        self.SetSizer(box_main)
        # 先使用一个空的来进行占位，避免显示错乱
        self.add_video("")
        self.Layout()
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.total = 0
        self.now = 1
        # 绑定按钮事件
        self.btn_quit.Bind(wx.EVT_BUTTON, self.exit)
        self.btn_pre.Bind(wx.EVT_BUTTON, self.pre_page)
        self.btn_next.Bind(wx.EVT_BUTTON, self.next_page)
        # 为了避免阻塞主要的线程，我们设置定时器来触发
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_video_data, self.timer)
        self.timer.StartOnce(100)

    # 上一页
    def pre_page(self, e):
        if self.now <= 1:
            return
        self.now -= 1
        self.get_video_data(None)

    # 下一页
    def next_page(self, e):
        if self.now >= self.total:
            return
        self.now += 1
        self.get_video_data(None)

    # 获取视频数据
    def get_video_data(self, evt):
        # 清空数据
        self.grid_video.Clear(True)
        # 获取视频列表
        data = get_video_list(self.now)
        self.now = data["now"]
        self.total = data["total"]
        self.text_page.SetLabelText("%d/%d" % (self.now, self.total))
        # 控制按钮
        if self.now > 1:
            self.btn_pre.Enable()
        else:
            self.btn_pre.Disable()
        if self.now < self.total:
            self.btn_next.Enable()
        else:
            self.btn_next.Disable()
        # 依次显示视频信息
        for video in data["data"]:
            # 替换图片地址避免无法加载
            url = video["pic"].replace("i0.", "i2.")
            url = url.replace("i1.", "i2.")
            self.add_video(url,
                           video["view"], video["comment"], video["title"])

    # 退出
    def exit(self, event):
        self.Close()
        self.Destroy()

    # 添加视频信息
    def add_video(self, url, play=0, comment=0, title="加载中..."):
        # 文本自动截断
        if len(title) > 16:
            title = title[:16]

        box_video = wx.BoxSizer(wx.VERTICAL)

        box_pic = wx.BoxSizer(wx.HORIZONTAL)

        img_cover = wx.StaticBitmap(self, wx.ID_ANY,
                                    get_net_bitmap(url, 100),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        img_cover.SetMaxSize(wx.Size(120, 50))
        box_pic.Add(img_cover, 0, wx.ALL, 5)

        box_data = wx.BoxSizer(wx.VERTICAL)

        text_play = wx.StaticText(self, wx.ID_ANY, u"播放 %d" % play, wx.DefaultPosition, wx.DefaultSize, 0)
        text_play.Wrap(-1)

        box_data.Add(text_play, 0, wx.BOTTOM | wx.LEFT, 5)

        text_good = wx.StaticText(self, wx.ID_ANY, u"评论 %d" % comment, wx.DefaultPosition, wx.DefaultSize, 0)
        text_good.Wrap(-1)

        box_data.Add(text_good, 0, wx.EXPAND | wx.BOTTOM | wx.LEFT, 5)

        box_pic.Add(box_data, 1, wx.EXPAND, 5)

        box_video.Add(box_pic, 1, wx.EXPAND, 5)

        text_title = wx.StaticText(self, wx.ID_ANY, title, wx.DefaultPosition, wx.DefaultSize, 0)
        text_title.Wrap(-1)

        text_title.SetFont(
            wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        box_video.Add(text_title, 0, wx.ALL, 5)
        self.grid_video.Add(box_video, 1, wx.EXPAND, 5)
        self.Layout()

    def __del__(self):
        pass
