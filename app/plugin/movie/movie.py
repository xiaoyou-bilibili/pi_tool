import wx
import wx.media


# 树莓派需要下载 sudo sudo apt-get install libgstreamer*
# windows系统需要使用szBackend为MEDIABACKEND_WMP10
# 后续有时间再试一下吧

class MoviePanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)
        self.m_mediaCtrl1 = wx.media.MediaCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(480, 320),
                                               style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_GSTREAMER)
        bSizer10.Add(self.m_mediaCtrl1, 0, wx.ALL, 5)
        self.SetSizer(bSizer10)
        self.Layout()

        print(self.m_mediaCtrl1.Load(u"movie/animation.mp4"))
        self.m_mediaCtrl1.Bind(wx.media.EVT_MEDIA_LOADED, self.play)
        # self.m_mediaCtrl1.SetPlaybackRate(1)
        # self.m_mediaCtrl1.SetVolume(1)
        # self.m_mediaCtrl1.Play()
        # # 绑定一个定时器事件
        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.paly, self.timer)
        # # 10s更换一次图片
        # self.timer.Start(1000)

    def play(self, evt):
        # 播放
        self.m_mediaCtrl1.Play()

    def __del__(self):
        pass
