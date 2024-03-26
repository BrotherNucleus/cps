import sys
import matplotlib
matplotlib.use('Qt5Agg')

import wx

class myFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        panel = wx.Panel(self)

        self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5))
        my_bttn = wx.Button(panel, label='Press Me', pos=(5,55))

        self.Show()

app = wx.App()
frame =myFrame()
app.MainLoop()
