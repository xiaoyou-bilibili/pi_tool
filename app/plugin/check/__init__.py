# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class TaskList
###########################################################################

class TaskList(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        grid_main = wx.GridSizer(1, 2, 0, 0)

        box_left = wx.BoxSizer(wx.VERTICAL)

        self.text_date = wx.StaticText(self, wx.ID_ANY, u"3月4号 周一 21:15:37", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_date.Wrap(-1)

        box_left.Add(self.text_date, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        grid_time = wx.GridSizer(0, 1, 0, 0)

        self.text_time = wx.StaticText(self, wx.ID_ANY, u"30:30", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_time.Wrap(-1)

        self.text_time.SetFont(wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "宋体"))

        grid_time.Add(self.text_time, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        box_left.Add(grid_time, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        grid_settings = wx.GridSizer(3, 2, 0, 0)

        self.btn_post_time = wx.Button(self, wx.ID_ANY, u"正计时", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_post_time.SetMinSize(wx.Size(100, 40))

        grid_settings.Add(self.btn_post_time, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_tomato = wx.Button(self, wx.ID_ANY, u"番茄计时", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_tomato.SetMinSize(wx.Size(100, 40))

        grid_settings.Add(self.btn_tomato, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_start = wx.Button(self, wx.ID_ANY, u"开始", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_start.SetMinSize(wx.Size(100, 40))

        grid_settings.Add(self.btn_start, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_stop = wx.Button(self, wx.ID_ANY, u"停止", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_stop.SetMinSize(wx.Size(100, 40))

        grid_settings.Add(self.btn_stop, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_setting = wx.Button(self, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_setting.SetMinSize(wx.Size(100, 40))

        grid_settings.Add(self.btn_setting, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_quit = wx.Button(self, wx.ID_ANY, u"退出", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_quit.SetMinSize(wx.Size(100, 40))

        grid_settings.Add(self.btn_quit, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        box_left.Add(grid_settings, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        grid_tomato_data = wx.GridSizer(0, 2, 0, 0)

        self.text_tomato_today = wx.StaticText(self, wx.ID_ANY, u"今日番茄 1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_tomato_today.Wrap(-1)

        grid_tomato_data.Add(self.text_tomato_today, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_tomato_total = wx.StaticText(self, wx.ID_ANY, u"总番茄 10", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_tomato_total.Wrap(-1)

        grid_tomato_data.Add(self.text_tomato_total, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)

        box_left.Add(grid_tomato_data, 1, wx.EXPAND, 5)

        grid_main.Add(box_left, 1, wx.EXPAND, 5)

        box_right = wx.BoxSizer(wx.VERTICAL)

        box_check_list = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"今日代办"), wx.VERTICAL)

        check_list_dataChoices = [u"写代码", u"看番", wx.EmptyString]
        self.check_list_data = wx.CheckListBox(box_check_list.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                               wx.DefaultSize, check_list_dataChoices, 0)
        self.check_list_data.SetMinSize(wx.Size(240, 200))

        box_check_list.Add(self.check_list_data, 0, wx.ALL, 5)

        box_right.Add(box_check_list, 1, wx.EXPAND, 5)

        grid_menu_check_list = wx.GridSizer(1, 3, 0, 0)

        self.btn_check_today = wx.Button(self, wx.ID_ANY, u"今日代办", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_check_today.SetMinSize(wx.Size(-1, 40))

        grid_menu_check_list.Add(self.btn_check_today, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.btn_check_all = wx.Button(self, wx.ID_ANY, u"所有代办", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_check_all.SetMinSize(wx.Size(-1, 40))

        grid_menu_check_list.Add(self.btn_check_all, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.btn_check_finish = wx.Button(self, wx.ID_ANY, u"已完成", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_check_finish.SetMinSize(wx.Size(-1, 40))

        grid_menu_check_list.Add(self.btn_check_finish, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        box_right.Add(grid_menu_check_list, 1, wx.EXPAND | wx.ALIGN_RIGHT, 5)

        grid_main.Add(box_right, 1, wx.EXPAND, 5)

        self.SetSizer(grid_main)
        self.Layout()

    def __del__(self):
        pass
