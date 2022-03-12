import wx
from app.menu import MainPanel


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="树莓派", size=(480, 340))
        self.panel = MainPanel(self)
        # 开启全屏
        self.ShowFullScreen(True)
        # 隐藏鼠标
        self.SetCursor(wx.Cursor(wx.CURSOR_BLANK))


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
