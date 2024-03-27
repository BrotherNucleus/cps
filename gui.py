import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar

import wx

class PlotPanel(wx.Panel):
    def __init__(self, parent, size):
        super(PlotPanel, self).__init__(parent)

        self.figure, self.ax = plt.subplots(figsize=size)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(1920, 1080))  # Set resolution here
        self.SetMinSize((1920, 1080))
        self.panel = wx.Panel(self)
        self.create_widgets()
        
        self.Show()
    
    def create_widgets(self):
        # Top-level sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Save and Load buttons
        btn_save = wx.Button(self.panel, label='Save')
        btn_load = wx.Button(self.panel, label='Load')
        
        # Adjusting button positions
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add((10, 10), 1)
        button_sizer.Add(btn_save, 0, wx.ALL, 5)
        button_sizer.Add(btn_load, 0, wx.ALL, 5)
        
        # Choice list 1
        self.choice1_label = wx.StaticText(self.panel, label='Choose Type:')
        choices1 = ['Wave', 'Impulse', 'Noise']
        self.choice1 = wx.Choice(self.panel, choices=choices1)
        self.choice1.Bind(wx.EVT_CHOICE, self.on_choice1)
        
        # Choice list 2
        self.choice2_label = wx.StaticText(self.panel, label='Choose Option:')
        choices2 = []
        self.choice2 = wx.Choice(self.panel, choices=choices2)
        self.choice2.Bind(wx.EVT_CHOICE, self.on_choice2)
        
        # Input spaces
        self.input1_label = wx.StaticText(self.panel, label='Input 1:')
        self.input1 = wx.TextCtrl(self.panel, size=(150, -1))
        
        self.input2_label = wx.StaticText(self.panel, label='Input 2:')
        self.input2 = wx.TextCtrl(self.panel, size=(150, -1))
        
        self.input3_label = wx.StaticText(self.panel, label='Input 3:')
        self.input3 = wx.TextCtrl(self.panel, size=(150, -1))

        self.input4_label = wx.StaticText(self.panel, label='Input 3:')
        self.input4 = wx.TextCtrl(self.panel, size=(150, -1))

        self.input5_label = wx.StaticText(self.panel, label='Input 3:')
        self.input5 = wx.TextCtrl(self.panel, size=(150, -1))

        self.input6_label = wx.StaticText(self.panel, label='Input 3:')
        self.input6 = wx.TextCtrl(self.panel, size=(150, -1))

        btn_generate = wx.Button(self.panel, label='Generate')
        btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)
        
        # Add widgets to sizer
        left_sizer.Add(button_sizer, 0, wx.TOP | wx.RIGHT, 5)
        left_sizer.Add(self.choice1_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.choice1, 0, wx.ALL, 5)
        left_sizer.Add(self.choice2_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.choice2, 0, wx.ALL, 5)
        left_sizer.Add(self.input1_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input1, 0, wx.LEFT|wx.RIGHT, 5)
        left_sizer.Add(self.input2_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input2, 0, wx.LEFT|wx.RIGHT, 5)
        left_sizer.Add(self.input3_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input3, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(self.input4_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input4, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(self.input5_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input5, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(self.input6_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input6, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(btn_generate, 0, wx.ALL | wx.CENTER, 5)
        
        # Add left sizer to main sizer
        self.sizer.Add(left_sizer, 0, wx.ALL, 5)

        # Right sizer for plots and text
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Plot panels
        self.plot_panel_tl = PlotPanel(self.panel, size=(6, 4))
        self.plot_panel_tr = PlotPanel(self.panel, size=(6, 4))
        self.plot_panel_bl = PlotPanel(self.panel, size=(6, 4))
        self.plot_panel_br = PlotPanel(self.panel, size=(6, 4))

        # Add plot panels to right sizer
        self.right_sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        self.right_sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        
        self.right_sizer_top.Add(self.plot_panel_tl, 0, wx.EXPAND | wx.LEFT, 5)
        self.right_sizer_top.Add(self.plot_panel_tr, 0, wx.EXPAND | wx.LEFT, 5)
        self.right_sizer_bottom.Add(self.plot_panel_bl, 0, wx.EXPAND | wx.LEFT, 5)
        self.right_sizer_bottom.Add(self.plot_panel_br, 0, wx.EXPAND | wx.LEFT, 5)

        self.right_sizer.Add(self.right_sizer_top, 1, wx.EXPAND)
        self.right_sizer.Add(self.right_sizer_bottom, 1, wx.EXPAND)

        # Add right sizer to main sizer
        self.sizer.Add(self.right_sizer, 1, wx.EXPAND)

        self.panel.SetSizer(self.sizer)
    
    def on_choice1(self, event):
        choice1 = self.choice1.GetStringSelection()
        if choice1 == 'Wave':
            choices2 = ['Sine', 'One sided Sine', 'Two sided Sine', 'Square', 'Symmetrical Square', 'Triangle']
        elif choice1 == 'Impulse':
            choices2 = ['Single', 'Random', 'Jump']
        elif choice1 == 'Noise':
            choices2 = ['Gaussian', 'Linear']
        
        self.choice2.SetItems(choices2)
        self.choice2.SetSelection(0)
        
        self.update_input_labels()
        self.sizer.Layout()
    
    def on_choice2(self, event):
        self.update_input_labels()
        self.sizer.Layout()

    def update_input_labels(self):
        choice1 = self.choice1.GetStringSelection()
        choice2 = self.choice2.GetStringSelection()
        if choice1 == 'Wave':
            self.input1_label.SetLabel('Amplitude:')
            self.input2_label.SetLabel('Frequency:')
            self.input3_label.SetLabel('Time')
            self.input4_label.SetLabel('Phase:')
            if choice2 == 'Triangle' :
                string = 'Coefficent: '
            else:
                string = ''
            self.input5_label.SetLabel(string)
        elif choice1 == 'Impulse':
            self.input1_label.SetLabel('Amplitude:')
            self.input2_label.SetLabel('Time')
            if choice2 == 'Single':
                self.input3_label.SetLabel('Impulse Probe: ')
            elif choice2 == 'Random':
                self.input3_label.SetLabel('Probability of Impulse: ')
            elif choice2 == 'Jump':
                self.input3_label.SetLabel('Time of jump: ')
            else:
                self.input3_label.SetLabel('')
            self.input4_label.SetLabel('')
            self.input5_label.SetLabel('')
        elif choice1 == 'Noise':
            self.input1_label.SetLabel('Amplitude:')
            self.input2_label.SetLabel('Time:')
            self.input3_label.SetLabel('')
            self.input4_label.SetLabel('')
            self.input5_label.SetLabel('')
        self.input6_label.SetLabel('Probe Number: ')

    def on_generate(self, event):
        # Generate plot data
        x = np.linspace(0, 10, 1000)
        freq = float(self.input1.GetValue())
        amp = float(self.input2.GetValue())
        phase = float(self.input3.GetValue())
        y = amp * np.sin(2 * np.pi * freq * x + phase)

        # Plot data on all plot panels
        for plot_panel in [self.plot_panel_tl, self.plot_panel_tr, self.plot_panel_bl, self.plot_panel_br]:
            plot_panel.ax.clear()
            plot_panel.ax.plot(x, y)
            plot_panel.ax.set_xlabel('Time')
            plot_panel.ax.set_ylabel('Amplitude')
            plot_panel.ax.set_title('Generated Plot')

            plot_panel.canvas.draw()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, title='GUI Example')
    app.MainLoop()
