# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
import tool.bilibili as bilibili
import tool.youtube as youtube
import tool.xiaomi as xiaomi
import tool.electricity as electricity
import wx
import wx.xrc
from app.photo import PhotoPanel

week_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def switch_update(btn, on_png, off_png):
    if btn.Label == "off":
        btn.SetBitmap(wx.Bitmap(on_png, wx.BITMAP_TYPE_ANY))
        btn.SetLabelText("on")
        return True
    else:
        btn.SetBitmap(wx.Bitmap(off_png, wx.BITMAP_TYPE_ANY))
        btn.SetLabelText("off")
        return False


class MainPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(480, 320), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.ui_init()

        # 全局变量信息
        self.img_path = os.path.join(os.getcwd(), "background")
        self.photos = os.listdir(self.img_path)
        self.photo_index = 1

        # 数据更新
        self.update_electricity()
        self.update_fans_and_play(None)
        self.show_photo(os.path.join(self.img_path, self.photos[0]))

        # 底部按钮点击事件
        self.btn_right.Bind(wx.EVT_LEFT_DOWN, self.light_switch)
        self.btn_switch.Bind(wx.EVT_LEFT_DOWN, self.switch_switch)
        self.img_photo.Bind(wx.EVT_LEFT_DOWN, self.app_photo)
        self.btn_close.Bind(wx.EVT_LEFT_DOWN, self.close_window)
        self.btn_off.Bind(wx.EVT_LEFT_DOWN, self.power_off)

        # 各种定时器
        # 1s更新一下时间
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.show_time, self.timer)
        # 每20分钟更新一下B站粉丝数
        self.timer_video_data = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_fans_and_play, self.timer_video_data)
        # 3s更新一下壁纸
        self.timer_photo = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer_photo, self.timer_photo)
        self.window_show(None)
        # 修改背景颜色
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

    # 初始化UI界面
    def ui_init(self):
        self.MainWindow = wx.BoxSizer(wx.VERTICAL)

        grid_top = wx.GridSizer(1, 2, 0, 0)
        grid_top_2 = wx.GridSizer(1, 2, 0, 0)

        box_time = wx.BoxSizer(wx.HORIZONTAL)

        self.text_hour = wx.StaticText(self, wx.ID_ANY, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_hour.Wrap(-1)

        self.text_hour.SetFont(wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))

        box_time.Add(self.text_hour, 0, wx.ALL, 5)

        self.text_second = wx.StaticText(self, wx.ID_ANY, u"00", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_second.Wrap(-1)

        self.text_second.SetFont(
            wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_second.SetForegroundColour(wx.Colour(255, 0, 128))

        box_time.Add(self.text_second, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        grid_top.Add(box_time, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_video = wx.GridSizer(0, 2, 0, 0)

        box_bilibili = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_bilibili = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/bilibili.png", wx.BITMAP_TYPE_ANY),
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        box_bilibili.Add(self.icon_bilibili, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.text_bili_fan = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_bili_fan.Wrap(-1)

        self.text_bili_fan.SetFont(
            wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_bili_fan.SetForegroundColour(wx.Colour(26, 178, 228))

        box_bilibili.Add(self.text_bili_fan, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_video.Add(box_bilibili, 1, wx.EXPAND, 5)

        box_youtube = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_youtube = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/youtube.png", wx.BITMAP_TYPE_ANY),
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        box_youtube.Add(self.icon_youtube, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.text_youtube_fan = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_youtube_fan.Wrap(-1)

        self.text_youtube_fan.SetFont(
            wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_youtube_fan.SetForegroundColour(wx.Colour(255, 0, 0))

        box_youtube.Add(self.text_youtube_fan, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_video.Add(box_youtube, 1, wx.EXPAND, 5)

        grid_top.Add(grid_video, 1, wx.EXPAND, 5)

        box_date = wx.BoxSizer(wx.VERTICAL)

        self.text_week = wx.StaticText(self, wx.ID_ANY, u"0月0号 周一", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_week.Wrap(-1)

        self.text_week.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))

        box_date.Add(self.text_week, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        grid_top_2.Add(box_date, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_play_num = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/play_num.png", wx.BITMAP_TYPE_ANY),
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.icon_play_num, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_bili_video_play = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_bili_video_play.Wrap(-1)
        self.text_bili_video_play.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_bili_video_play.SetForegroundColour(wx.Colour(26, 178, 228))
        bSizer10.Add(self.text_bili_video_play, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.text_youtube_video_play = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_youtube_video_play.Wrap(-1)
        self.text_youtube_video_play.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_youtube_video_play.SetForegroundColour(wx.Colour(255, 0, 0))
        bSizer10.Add(self.text_youtube_video_play, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_top_2.Add(bSizer10, 1, wx.EXPAND, 5)

        self.MainWindow.Add(grid_top, 1, wx.EXPAND, 5)
        self.MainWindow.Add(grid_top_2, 1, wx.EXPAND, 5)

        grid_photo = wx.GridSizer(0, 2, 0, 0)

        grid_tmp_electricity = wx.GridSizer(2, 1, 0, 0)

        grid_tmp = wx.GridSizer(0, 2, 0, 0)

        box_temperature = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_temperature = wx.StaticBitmap(self, wx.ID_ANY,
                                                wx.Bitmap(u"app/icon/temperature.png", wx.BITMAP_TYPE_ANY),
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.icon_temperature.SetMaxSize(wx.Size(20, -1))
        box_temperature.Add(self.icon_temperature, 0, wx.ALL, 5)

        self.text_temperature = wx.StaticText(self, wx.ID_ANY, u"0℃", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_temperature.Wrap(-1)

        self.text_temperature.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_temperature.SetForegroundColour(wx.Colour(255, 0, 0))

        box_temperature.Add(self.text_temperature, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_tmp.Add(box_temperature, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        box_humidity = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_humidity = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/humidity.png", wx.BITMAP_TYPE_ANY),
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.icon_humidity.SetMaxSize(wx.Size(20, -1))
        box_humidity.Add(self.icon_humidity, 0, wx.ALL, 5)

        self.text_humidity = wx.StaticText(self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_humidity.Wrap(-1)

        self.text_humidity.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))
        self.text_humidity.SetForegroundColour(wx.Colour(62, 187, 221))

        box_humidity.Add(self.text_humidity, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_tmp.Add(box_humidity, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        grid_tmp_electricity.Add(grid_tmp, 1, wx.EXPAND, 5)

        box_electricity = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_electricity = wx.StaticBitmap(self, wx.ID_ANY,
                                                wx.Bitmap(u"app/icon/electricity.png", wx.BITMAP_TYPE_ANY),
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.icon_electricity.SetMaxSize(wx.Size(40, -1))
        box_electricity.Add(self.icon_electricity, 3, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        grid_electricity = wx.GridSizer(2, 2, 0, 0)

        self.text_electricity_remain = wx.StaticText(self, wx.ID_ANY, u"剩余电量0", wx.DefaultPosition, wx.DefaultSize,
                                                     0)
        self.text_electricity_remain.Wrap(-1)

        grid_electricity.Add(self.text_electricity_remain, 0, wx.ALL, 5)

        self.text_electricity_mony = wx.StaticText(self, wx.ID_ANY, u"本月电费0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_electricity_mony.Wrap(-1)

        grid_electricity.Add(self.text_electricity_mony, 0, wx.ALL, 5)

        self.text_electricity_use = wx.StaticText(self, wx.ID_ANY, u"本月用电0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_electricity_use.Wrap(-1)

        grid_electricity.Add(self.text_electricity_use, 0, wx.ALL, 5)

        self.text_electricity_yesterday = wx.StaticText(self, wx.ID_ANY, u"昨日用电0", wx.DefaultPosition,
                                                        wx.DefaultSize, 0)
        self.text_electricity_yesterday.Wrap(-1)

        grid_electricity.Add(self.text_electricity_yesterday, 0, wx.ALL, 5)

        box_electricity.Add(grid_electricity, 7, wx.EXPAND, 5)

        grid_tmp_electricity.Add(box_electricity, 1, wx.EXPAND, 5)

        grid_photo.Add(grid_tmp_electricity, 1, wx.EXPAND, 5)

        self.img_photo = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        self.img_photo.SetMaxSize(wx.Size(300, 110))

        grid_photo.Add(self.img_photo, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.MainWindow.Add(grid_photo, 1, wx.EXPAND, 5)

        grid_menu = wx.GridSizer(1, 7, 0, 0)

        grid_menu.SetMinSize(wx.Size(-1, 60))
        self.btn_right = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/light_off.png", wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        # 设置一下标签表示我们是关灯
        self.btn_right.SetLabelText("off")
        grid_menu.Add(self.btn_right, 0, wx.ALL, 5)

        self.btn_switch = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/switch_off.png", wx.BITMAP_TYPE_ANY),
                                          wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.btn_right.SetLabelText("off")
        grid_menu.Add(self.btn_switch, 0, wx.ALL, 5)

        self.btn_close = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/close.png", wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        grid_menu.Add(self.btn_close, 0, wx.ALL, 5)

        self.btn_off = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"app/icon/off.png", wx.BITMAP_TYPE_ANY),
                                       wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        grid_menu.Add(self.btn_off, 0, wx.ALL, 5)

        self.MainWindow.Add(grid_menu, 1, wx.EXPAND, 5)

        self.SetSizer(self.MainWindow)
        self.Layout()

    # 时间显示功能
    def show_time(self, evt):
        #  获取当前时间
        self.text_hour.SetLabelText(time.strftime("%H:%M", time.localtime()))
        self.text_second.SetLabelText(time.strftime("%S", time.localtime()))
        self.text_week.SetLabelText(time.strftime("%m月%d号 ", time.localtime()) + week_map[datetime.today().weekday()])
        # 获取当前室内温度和湿度信息
        sensor = xiaomi.get_home_temperature()
        self.text_temperature.SetLabelText("%s℃" % sensor["temperature"])
        self.text_humidity.SetLabelText("%s%%" % sensor["humidity"])

    def on_timer_photo(self, evt):
        # 遍历完图片后重新开始遍历
        if self.photo_index >= len(self.photos):
            self.photo_index = 0
        # 显示背景图片
        self.show_photo(os.path.join(self.img_path, self.photos[self.photo_index]))
        self.photo_index += 1

    # 壁纸显示功能
    def show_photo(self, filename):
        width = 230
        img = wx.Image(filename, type=wx.BITMAP_TYPE_ANY)
        # 我们获取一下图片的高度和宽度(这个高度是根据我们屏幕的宽度算出来的，是为了让图片更好展示，避免拉伸)
        img_width = img.GetWidth()
        img_height = int(img.GetHeight() * (width / img_width))
        # 对图片进行缩放，方便我们全屏显示
        self.img_photo.SetBitmap(img.Scale(width, img_height).ConvertToBitmap())

    # 灯光切换
    def light_switch(self, e):
        status = switch_update(self.btn_right, "app/icon/light_on.png", "app/icon/light_off.png")
        xiaomi.light_switch(status)

    # 开关切换
    def switch_switch(self, e):
        # 判断一下当前灯的状态
        status = switch_update(self.btn_switch, "app/icon/switch_on.png", "app/icon/switch_off.png")
        xiaomi.switch_switch(status)

    # 更新播放数和粉丝数
    def update_fans_and_play(self, evt):
        print("更新粉丝数和播放数 %s" % time.strftime("%H:%M", time.localtime()))
        self.text_bili_fan.SetLabelText(bilibili.get_bilibili_fans())
        self.text_bili_video_play.SetLabelText(bilibili.get_video_play())
        # 更新youtube的
        youtube_data = youtube.get_youtube_fan()
        self.text_youtube_fan.SetLabelText(youtube_data["fan"])
        self.text_youtube_video_play.SetLabelText(youtube_data["view"])

    # 更新用电情况
    def update_electricity(self):
        data = electricity.get_electricity_use()
        self.text_electricity_remain.SetLabelText("余额%s" % data["remain"])
        self.text_electricity_mony.SetLabelText("本月电费%.1f" % data["money"])
        self.text_electricity_use.SetLabelText("本月用电%.1f" % data["use"])
        self.text_electricity_yesterday.SetLabelText("昨日用电%s" % data["yesterday"])

    # 关闭界面
    def close_window(self, event):
        self.GetParent().Close()

    # 关机
    def power_off(self, event):
        os.system("sudo shutdown -h now")

    # 打开图库
    def app_photo(self, event):
        panel = PhotoPanel(self)
        panel.Show()
        panel.SetSize(wx.Size(self.GetSize()))
        # 当panel销毁时触发回调
        panel.Bind(wx.EVT_CLOSE, self.window_show)
        self.windows_hide()

    # 界面隐藏时触发
    def window_show(self, event):
        print("显示界面")
        # 每秒显示时间
        self.timer.Start(1000)
        # 3s更新图片
        self.timer_photo.Start(3000)
        # 20分钟更新B站数据
        self.timer_video_data.Start(1000 * 60 * 20)

    # 界面显示时触发
    def windows_hide(self):
        print("隐藏界面")
        # 停止计时器
        self.timer.Stop()
        self.timer_photo.Stop()
        self.timer_video_data.Stop()

    def __del__(self):
        pass
