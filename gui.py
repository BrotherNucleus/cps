import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
import waves as w
import impulse as i
import noise as n
import analitics as a
import fileManager as FM
import os

import wx
import re
import recon

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
        super(MyFrame, self).__init__(parent, title=title, size=(1080, 720))  # Set resolution here
        self.SetMinSize((1920, 1080))
        self.panel = wx.ScrolledWindow(self)
        self.panel.SetScrollRate(5, 5)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.create_widgets()
        self.waveMem = []
        wave = w.Wave(0, 0, 0, 0, 0)
        wave.result = np.array([[1, 2, 3],[0,0,0], [0,0,0]])
        self.waveMem.append((wave, 'WS'))
        self.WCIM = 1
        self.chosenId = 1
        self.currWave = None
        self.corelationWave = None
        self.Show()
    
    def create_widgets(self):
        # Top-level sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Save and Load buttons
        btn_save = wx.Button(self.panel, label='Save')
        btn_load = wx.Button(self.panel, label='Load')
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        btn_load.Bind(wx.EVT_BUTTON, self.on_load)
        
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
        self.input1_label = wx.StaticText(self.panel, label='Empty:')
        self.input1 = wx.TextCtrl(self.panel, size=(150, -1), value = "1")
        
        self.input2_label = wx.StaticText(self.panel, label='Empty:')
        self.input2 = wx.TextCtrl(self.panel, size=(150, -1), value = "1")
        
        self.input3_label = wx.StaticText(self.panel, label='Empty:')
        self.input3 = wx.TextCtrl(self.panel, size=(150, -1), value = "1")

        self.input4_label = wx.StaticText(self.panel, label='Empty:')
        self.input4 = wx.TextCtrl(self.panel, size=(150, -1), value = "0")

        self.input5_label = wx.StaticText(self.panel, label='Empty:')
        self.input5 = wx.TextCtrl(self.panel, size=(150, -1), value = "0.5")

        self.input6_label = wx.StaticText(self.panel, label='Empty:')
        self.input6 = wx.TextCtrl(self.panel, size=(150, -1), value = "64")

        self.check1 = wx.CheckBox(self.panel, label = "Quantisize")

        btn_generate = wx.Button(self.panel, label='Generate')
        btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)

        self.choice3_label = wx.StaticText(self.panel, label='Choose Wave Slot:')
        self.choices3 = ['New Slot']
        self.choice3 = wx.Choice(self.panel, choices=self.choices3)
        self.choice3.Bind(wx.EVT_CHOICE, self.on_choice3)

        btn_calc = wx.Button(self.panel, label="Calculate")
        btn_calc.Bind(wx.EVT_BUTTON, self.on_calculate)

        self.inputC_label = wx.StaticText(self.panel, label = "Equasion:")
        self.inputC = wx.TextCtrl(self.panel, size=(150, -1))

        self.inputHist_label = wx.StaticText(self.panel, label = "Hist spaces:")
        self.inputHist = wx.Slider(self.panel, value = 5, minValue = 5, maxValue = 20)
        self.inputHist.Bind(wx.EVT_SLIDER, self.on_slider)

        self.histValue = wx.StaticText(self.panel, label = "5")

        self.choice4_label = wx.StaticText(self.panel, label = "Choose reconstruction type:")
        self.choices4 = ["Rank Zero Extrapolation", "Rank One Interpolation", "sinc"]
        self.choice4 = wx.Choice(self.panel, choices = self.choices4)

        self.choice5_label = wx.StaticText(self.panel, label = "Choose filter Type:")
        self.choices5 = ["None", "Low Pass Filter / Rect", "Low Pass Filter / Hanning", "High Pass Filter / Rect", "High Pass Filter / Hanning"]
        self.choice5 = wx.Choice(self.panel, choices = self.choices5)

        self.input7_label = wx.StaticText(self.panel, label='Cutoff Frequency:')
        self.input7 = wx.TextCtrl(self.panel, size=(150, -1), value = "4")

        self.input8_label = wx.StaticText(self.panel, label='Rank:')
        self.input8 = wx.TextCtrl(self.panel, size=(150, -1), value ="32")
        
        btn_reconstruct = wx.Button(self.panel, label="Reconstruct")
        btn_reconstruct.Bind(wx.EVT_BUTTON, self.on_reconstruct)

        self.choice6_label = wx.StaticText(self.panel, label='Choose Wave Slot:')
        self.choice6 = wx.Choice(self.panel, choices=self.choices3)
        self.choice6.Bind(wx.EVT_CHOICE, self.on_choice6)

        btn_corelate = wx.Button(self.panel, label = 'Corelation')
        btn_corelate.Bind(wx.EVT_BUTTON, self.on_corelate)

        btn_fft = wx.Button(self.panel, label = 'FFT')
        btn_fft.Bind(wx.EVT_BUTTON, self.on_fft)

        btn_dct = wx.Button(self.panel, label = 'DCT')
        btn_dct.Bind(wx.EVT_BUTTON, self.on_dct)

        btn_dft = wx.Button(self.panel, label = 'DFT')
        btn_dft.Bind(wx.EVT_BUTTON, self.on_dft)

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
        left_sizer.Add(self.check1, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(btn_generate, 0, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(self.choice3_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.choice3, 0, wx.ALL, 5)
        left_sizer.Add(btn_calc, 0, wx.ALL|wx.BOTTOM, 5)
        left_sizer.Add(self.inputC_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.inputC, 0, wx.LEFT|wx.RIGHT, 5)
        left_sizer.Add(self.inputHist_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.inputHist, 0, wx.LEFT|wx.RIGHT, 5)
        left_sizer.Add(self.histValue, 0, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(self.choice4_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.choice4, 0, wx.ALL, 5)
        left_sizer.Add(btn_reconstruct, 0, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(self.choice5_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.choice5, 0, wx.ALL, 5)
        left_sizer.Add(self.input7_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input7, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(self.input8_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.input8, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        left_sizer.Add(self.choice6_label, 0, wx.LEFT|wx.TOP, 5)
        left_sizer.Add(self.choice6, 0, wx.ALL, 5)
        left_sizer.Add(btn_corelate, 0, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(btn_fft, 0, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(btn_dct, 0, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(btn_dft, 0, wx.ALL | wx.CENTER, 5)
        
        # Add left sizer to main sizer
        self.sizer.Add(left_sizer, 0, wx.ALL, 5)

        # Right sizer for plots and text
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Plot panels
        self.plot_panel_tl = PlotPanel(self.panel, size=(6, 4))
        self.plot_panel_tr = PlotPanel(self.panel, size=(6, 4))
        self.plot_panel_bl = PlotPanel(self.panel, size=(6, 3))
        self.plot_panel_br = PlotPanel(self.panel, size=(6, 3))

        # Add plot panels to right sizer
        self.right_sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        self.right_sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        
        self.right_sizer_top.Add(self.plot_panel_tl, 0, wx.LEFT, 5)
        self.right_sizer_top.Add(self.plot_panel_tr, 0, wx.LEFT, 5)
        self.right_sizer_bottom.Add(self.plot_panel_bl, 0, wx.LEFT, 5)
        self.right_sizer_bottom.Add(self.plot_panel_br, 0, wx.LEFT, 5)

        self.right_sizer.Add(self.right_sizer_top, 1, wx.EXPAND)
        self.right_sizer.Add(self.right_sizer_bottom, 1, wx.EXPAND)

        # Add right sizer to main sizer
        self.sizer.Add(self.right_sizer, 1, wx.EXPAND)

        self.panel.SetSizer(self.sizer)

        self.choice3.SetSelection(0)

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
            self.input3_label.SetLabel('Time')
            if choice2 == 'Single':
                self.input2_label.SetLabel('Impulse Probe: ')
            elif choice2 == 'Random':
                self.input2_label.SetLabel('Probability of Impulse: ')
            elif choice2 == 'Jump':
                self.input2_label.SetLabel('Time of jump: ')
            else:
                self.input3_label.SetLabel('')
            self.input4_label.SetLabel('')
            self.input5_label.SetLabel('')
        elif choice1 == 'Noise':
            self.input1_label.SetLabel('Amplitude:')
            self.input3_label.SetLabel('Time:')
            self.input2_label.SetLabel('')
            self.input4_label.SetLabel('')
            self.input5_label.SetLabel('')
        self.input6_label.SetLabel('Probe Number: ')

    def choose_func(self, name, A, f, t, phi, k, pr):
        match(name):
            case 'Sine':
                return w.SinWave(A, f, t, phi, self.WCIM)
            case 'One sided Sine':
                return w.SinHalfWave(A, f, t, phi, self.WCIM)
            case 'Two sided Sine':
                return w.SinModWave(A, f, t, phi, self.WCIM)
            case 'Square':
                return w.SquareWave(A, f, t, phi, self.WCIM)
            case 'Symmetrical Square':
                return w.SymSquareWave(A, f, t, phi, self.WCIM)
            case 'Triangle':
                return w.TriangleWave(A, f, t, phi, k, self.WCIM)
            case 'Single':
                return i.singleImpulse(A, pr, t, f, self.WCIM)
            case 'Random' :
                return i.randomImpulse(A, pr, t, f, self.WCIM)
            case 'Jump' :
                return i.jump(A, pr, t, f, self.WCIM)
            case 'Gaussian':
                return n.gaussianNoise(A, t, self.WCIM)
            case 'Linear':
                return n.linearNoise(A, t, self.WCIM)

    def on_slider(self, event):
        y = self.currWave.result[:,[1]]
        v = self.inputHist.GetValue()
        self.histValue.SetLabel(str(v))
        self.plot_panel_bl.ax.clear()
        self.plot_panel_bl.ax.hist(y, v)
        self.plot_panel_bl.canvas.draw()

    def show_plots(self, res):
        x = res[:,[0]]
        y = res[:,[1]]
        z = res[:,[2]]
        print(self.currWave.calculated)
        if(self.currWave.noquant == None and self.currWave.filed == False and type(self.currWave) != n.gaussianNoise and \
            type(self.currWave) != n.linearNoise and type(self.currWave) != i.singleImpulse and type(self.currWave) != i.randomImpulse and \
                type(self.currWave) != i.jump and self.currWave.calculated == False):
            x2 = np.linspace(x[0], x[len(x)-1], 3000)
            y2 = np.zeros(len(x2))
            z2 = np.zeros(len(x2))
            for k in range(len(x2)):
                #print(k)
                y2[k] = self.currWave.func(x2[k])
                z2[k] = 0

        anl = a.analizer(self.currWave)
        # Calculate statistics
        mean = anl.mean()
        absMean = anl.meanAbs()
        stdDev = anl.rms()
        pow = anl.power()
        var = anl.variance()

        mse = 0
        snr = 0
        md = 0
        if(self.currWave.noquant != None):
            mse = anl.MSE(self.currWave.noquant)
            snr = anl.SNR(self.currWave.noquant)
            md = anl.MD(self.currWave.noquant)

        # Display statistics as text on bottom right panel
        self.plot_panel_br.ax.clear()
        text = f"Mean: {mean:.2f}\nAbsolute Mean: {absMean:.2f}\nStd Dev: {stdDev:.2f}\nVariance: {var:.2f}\nPower: {pow:.2f}\n Mean Squared Error: {mse:.2f}\nSNR: {snr:.2f}\nMaximum DIffrence: {md:.2f}"
        self.plot_panel_br.ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)
        self.plot_panel_br.ax.axis('off')
        self.plot_panel_br.canvas.draw()

        self.plot_panel_tr.ax.clear()
        if(self.currWave.noquant == None and self.currWave.filed == False and type(self.currWave) != n.gaussianNoise and \
            type(self.currWave) != n.linearNoise and type(self.currWave) != i.singleImpulse and type(self.currWave) != i.randomImpulse and \
            type(self.currWave) != i.jump and self.currWave.calculated == False):
            self.plot_panel_tr.ax.plot(x2, z2)
            self.plot_panel_tr.ax.plot(x, z, 'bo')
            print(z)
        else:
            self.plot_panel_tr.ax.plot(x, z)
        self.plot_panel_tr.ax.set_xlabel('Time')
        self.plot_panel_tr.ax.set_ylabel('Amplitude')
        self.plot_panel_tr.ax.set_title('Generated Plot')

        self.plot_panel_tr.canvas.draw()

        # Plot data on all plot panels
        for plot_panel in [self.plot_panel_tl]:
            plot_panel.ax.clear()
            if(self.currWave.noquant == None and self.currWave.filed == False and type(self.currWave) != n.gaussianNoise and \
                type(self.currWave) != n.linearNoise and type(self.currWave) != i.singleImpulse and type(self.currWave) != i.randomImpulse and \
                type(self.currWave) != i.jump and self.currWave.calculated == False):
                plot_panel.ax.plot(x2, y2)
                plot_panel.ax.plot(x, y, 'bo')
            else:
                plot_panel.ax.plot(x, y)
            plot_panel.ax.set_xlabel('Time')
            plot_panel.ax.set_ylabel('Amplitude')
            plot_panel.ax.set_title('Generated Plot')

            plot_panel.canvas.draw()

    def shortName(self, wave):
        match(type(wave)):
            case w.Wave:
                return 'WS'
            case w.SinWave:
                return 'WS'
            case w.SinHalfWave:
                return 'WSZ'
            case w.SinModWave:
                return 'WSM'
            case w.SquareWave:
                return 'WSq'
            case w.SymSquareWave:
                return 'WSSq'
            case w.TriangleWave:
                return 'WT'
            case i.impulse:
                return 'IS'
            case i.singleImpulse:
                return 'IS'
            case i.randomImpulse:
                return 'IR'
            case i.jump:
                return 'IJ'
            case n.gaussianNoise:
                return 'NG'
            case n.linearNoise:
                return 'NL'

    def Quant(self, val):
        ret = val
        ret[:, [1]] = np.round(val[:, [1]], 1)
        return ret
    def on_reconstruct(self, event):
        choice = self.choice4.GetStringSelection()
        i = 0
        if choice == "Rank Zero Extrapolation":
            i = 1
        elif choice == "Rank One Interpolation":
            i = 2
        elif choice == "sinc":
            i = 3
        else:
            return
        fileM = FM.FileM('/')
        res = recon.reconstruct(self.currWave.result, i)
        choice2 = self.choice5.GetStringSelection()
        ct = float(self.input7.GetValue())
        rank = int(self.input8.GetValue())
        if choice2 == "Low Pass Filter / Rect":
            res = recon.lowPassFilter(res, ct, len(res[:, 1]), rank)
        elif choice2 == "Low Pass Filter / Hanning":
            res = recon.lowPassFilterHan(res, ct, len(res[:, 1]), rank)
        elif choice2 == "High Pass Filter / Rect":
            res = recon.highPassFilter(res, ct, len(res[:, 1]), rank)
        elif choice2 == "High Pass Filter / Hanning":
            res = recon.highPassFilterHan(res, ct, len(res[:, 1]), rank)
        temp = self.currWave
        print(type(temp))
        self.currWave = fileM.interpret(res, self.WCIM)
        self.currWave.noquant = temp

        self.show_plots(res)

        choices2 = ['Sine', 'One sided Sine', 'Two sided Sine', 'Square', 'Symmetrical Square', 'Triangle']

        self.choice1.SetSelection(0)
        self.choice2.SetItems(choices2)
        self.choice2.SetSelection(0)

        self.input1_label.SetLabel('Amplitude:')
        self.input2_label.SetLabel('Frequency:')
        self.input3_label.SetLabel('Time:')
        self.input4_label.SetLabel('Phase:')
        self.input5_label.SetLabel('')
        self.input6_label.SetLabel('Probe Number: ')

        self.input1.SetValue(str(self.currWave.amplitude))
        self.input2.SetValue(str(self.currWave.frequency))
        self.input3.SetValue(str(self.currWave.time))
        self.input4.SetValue(str(self.currWave.phase))
        self.input6.SetValue(str(self.currWave.probeNum))

        self.on_slider(wx.EVT_SLIDER)

        self.currWave.id = self.WCIM

        self.choices3.append('Slot ' + str(self.currWave.id))
        self.choice3.Append('Slot ' + str(self.currWave.id))
        self.choice6.Append('Slot ' + str(self.currWave.id))
        self.choice3.SetSelection(self.currWave.id)
        self.choice6.SetSelection(self.currWave.id)

        self.waveMem.append((self.currWave, 'WS'))
        self.WCIM = self.WCIM + 1

        return

    def on_generate(self, event):
        # Generate plot data
        if self.input2.GetValue() == '':
            freq = None
        else:
            freq = float(self.input2.GetValue())
        amp = float(self.input1.GetValue())
        if self.input4.GetValue() == '':
            phase = None
        else:
            phase = float(self.input4.GetValue())
        time = float(self.input3.GetValue())
        if(self.choice2.GetStringSelection() == 'Triangle'):
            coeff = float(self.input5.GetValue())
        else:
            coeff = None
        probes = int(self.input6.GetValue())
        wave = self.choose_func(self.choice2.GetStringSelection(), amp, freq, time, phase, coeff, probes)
        self.currWave = wave
        res = wave.calculate(probes)
        if(self.check1.GetValue()):
            res = self.Quant(res)
            wave.result = res
        self.show_plots(res)
        self.on_slider(wx.EVT_SLIDER)
        # if(self.choice3.GetStringSelection() == 'New Slot'):
        short = self.shortName(self.currWave)
        self.waveMem.append((self.currWave, short))
        self.choices3.append('Slot ' + str(self.currWave.id))
        self.choice3.Append('Slot ' + str(self.currWave.id))
        self.choice3.SetSelection(self.currWave.id)
        self.choice6.Append('Slot ' + str(self.currWave.id))
        self.choice6.SetSelection(self.currWave.id)
        self.WCIM = self.WCIM + 1
        self.chosenId = self.currWave
        # else:
        #     print(self.chosenId)
        #     print(self.waveMem[self.chosenId])
        #     print(type(self.waveMem[self.chosenId][0]))
        #     print(type(self.currWave))
        #     self.waveMem[self.chosenId] = (self.currWave, self.shortName(self.currWave))


    def on_save(self, event):
        # Open file dialog for saving
        wildcard = "NumPy files (*.npy)|*.npy|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "Choose a file", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        cwd = os.getcwd()

        default_dir = cwd + "/waves"  # Replace this with your desired default directory
        dlg.SetDirectory(default_dir)

        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetFilename()  # Get the name of the file
            folder_path = dlg.GetDirectory()  # Get the folder path
            fileM = FM.FileM(folder_path)
            fileM.setValue(self.currWave.result)

            fileM.serialize(file_name)
        dlg.Destroy()

    def on_load(self, event):
        # Open file dialog for loading
        wildcard = "NumPy files (*.npy)|*.npy|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "Choose a file", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        cwd = os.getcwd()

        default_dir = cwd + "/waves"  # Replace this with your desired default directory
        dlg.SetDirectory(default_dir)

        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetFilename()  # Get the name of the file
            folder_path = dlg.GetDirectory()  # Get the folder path

            fileM = FM.FileM(folder_path)
            res = fileM.load(file_name)
            self.currWave = fileM.interpret(res, self.WCIM)
            self.currWave.filed = True

        dlg.Destroy()

        if(self.check1.GetValue()):
            res = self.Quant(res)
            self.currWave.result = res

        self.show_plots(res)

        choices2 = ['Sine', 'One sided Sine', 'Two sided Sine', 'Square', 'Symmetrical Square', 'Triangle']

        self.choice1.SetSelection(0)
        self.choice2.SetItems(choices2)
        self.choice2.SetSelection(0)

        self.input1_label.SetLabel('Amplitude:')
        self.input2_label.SetLabel('Frequency:')
        self.input3_label.SetLabel('Time:')
        self.input4_label.SetLabel('Phase:')
        self.input5_label.SetLabel('')
        self.input6_label.SetLabel('Probe Number: ')

        self.input1.SetValue(str(self.currWave.amplitude))
        self.input2.SetValue(str(self.currWave.frequency))
        self.input3.SetValue(str(self.currWave.time))
        self.input4.SetValue(str(self.currWave.phase))
        self.input6.SetValue(str(self.currWave.probeNum))

        self.on_slider(wx.EVT_SLIDER)

        self.currWave.id = self.WCIM

        self.choices3.append('Slot ' + str(self.currWave.id))
        self.choice3.Append('Slot ' + str(self.currWave.id))
        self.choice3.SetSelection(self.currWave.id)
        self.choice6.Append('Slot ' + str(self.currWave.id))
        self.choice6.SetSelection(self.currWave.id)

        self.waveMem.append((self.currWave, 'WS'))
        self.WCIM = self.WCIM + 1

    def typeReader(self, str):
        match(str):
            case 'WS':
                return [0, 0]
            case 'WSZ':
                return [0, 1]
            case 'WSM':
                return [0, 2]
            case 'WSq':
                return [0, 3]
            case 'WSSq':
                return [0, 4]
            case 'WT':
                return [0, 5]
            case 'IS':
                return [1, 0]
            case 'IR':
                return [1, 1]
            case 'IJ':
                return [1, 2]
            case 'NG':
                return [2, 0]
            case 'NL':
                return [2, 1]

    def interpretSlot(self, str):
        return re.sub(r'\D', '', str)

    def findWaveById(self, id):
        for wave in self.waveMem:
            if(wave[0].id == id):
                return wave

    def on_choice6(self, event):
        check = self.choice6.GetStringSelection()
        if check == 'New Slot':
            t = 0
        else:
            trim = self.interpretSlot(check)
            t = int(trim)
        v = self.findWaveById(t)
        self.corelationWave = v[0]

    def on_corelate(self, event):
        print(type(self.corelationWave))
        res = recon.corelate(self.currWave.result, self.corelationWave.result)
        fileM = FM.FileM("/")
        self.currWave = fileM.interpret(res, self.WCIM)
        self.currWave.filed = True

        self.show_plots(res)

        choices2 = ['Sine', 'One sided Sine', 'Two sided Sine', 'Square', 'Symmetrical Square', 'Triangle']

        self.choice1.SetSelection(0)
        self.choice2.SetItems(choices2)
        self.choice2.SetSelection(0)

        self.input1_label.SetLabel('Amplitude:')
        self.input2_label.SetLabel('Frequency:')
        self.input3_label.SetLabel('Time:')
        self.input4_label.SetLabel('Phase:')
        self.input5_label.SetLabel('')
        self.input6_label.SetLabel('Probe Number: ')

        self.input1.SetValue(str(self.currWave.amplitude))
        self.input2.SetValue(str(self.currWave.frequency))
        self.input3.SetValue(str(self.currWave.time))
        self.input4.SetValue(str(self.currWave.phase))
        self.input6.SetValue(str(self.currWave.probeNum))

        self.on_slider(wx.EVT_SLIDER)

        self.currWave.id = self.WCIM

        self.choices3.append('Slot ' + str(self.currWave.id))
        self.choice3.Append('Slot ' + str(self.currWave.id))
        self.choice3.SetSelection(self.currWave.id)
        self.choice6.Append('Slot ' + str(self.currWave.id))
        self.choice6.SetSelection(self.currWave.id)

        self.waveMem.append((self.currWave, 'WS'))
        self.WCIM = self.WCIM + 1

        

    def on_choice3(self, event):

        check = self.choice3.GetStringSelection()
        if check == 'New Slot':
            t = 0
        else:
            trim = self.interpretSlot(check)
            t = int(trim)
        v = self.findWaveById(t)
        self.currWave = v[0]
        self.chosenId = self.currWave.id
        self.show_plots(v[0].result)

        read = self.typeReader(v[1])
        self.choice1.SetSelection(read[0])
        self.choice2.SetSelection(read[1])

        self.input1.SetValue('')
        self.input2.SetValue('')
        self.input3.SetValue('')
        self.input4.SetValue('')
        self.input5.SetValue('')
        self.input6.SetValue('')

        self.input1.SetValue(str(self.currWave.amplitude))
        if(read[0] == 0):
            self.input2.SetValue(str(self.currWave.frequency))
            self.input4.SetValue(str(self.currWave.phase))
            if(read[1] == 5):
                self.input5.SetValue(str(self.currWave.coeff))               
        elif(read[0] == 1 and read[1] == 0):
            self.input2.SetValue(str(self.currWave.imProbe))
        elif(read[0] == 1 and read[1] == 1):
            self.input2.SetValue(str(self.currWave.chance))
        elif(read[0] == 1 and read[1] == 2):
            self.input2.SetValue(str(self.currWave.jumpTime))
        self.input3.SetValue(str(self.currWave.time))
        self.input6.SetValue(str(self.currWave.probeNum))

    def on_calculate(self, event):
        val = str(self.inputC.GetValue())
        eq = val.split()
        waveDisc1 = int(eq[0])
        operator = eq[1]
        waveDisc2 = int(eq[2])

        wave1 = self.findWaveById(waveDisc1)
        wave2 = self.findWaveById(waveDisc2)

        if operator == '+':
            wave = wave1[0] + wave2[0]
        elif operator == '-':
            wave = wave1[0] - wave2[0]
        elif operator == '*':
            wave = wave1[0] * wave2[0]
        elif operator == '/':
            wave = wave1[0] / wave2[0]
        
        #print(type(wave))
        self.currWave = wave

        self.currWave.calculated = True

        self.show_plots(self.currWave.result)

        choices2 = ['Sine', 'One sided Sine', 'Two sided Sine', 'Square', 'Symmetrical Square', 'Triangle']

        self.choice1.SetSelection(0)
        self.choice2.SetItems(choices2)
        self.choice2.SetSelection(0)

        self.input1_label.SetLabel('Amplitude:')
        self.input2_label.SetLabel('Frequency:')
        self.input3_label.SetLabel('Time:')
        self.input4_label.SetLabel('Phase:')
        self.input5_label.SetLabel('')
        self.input6_label.SetLabel('Probe Number: ')

        self.input1.SetValue(str(self.currWave.amplitude))
        self.input2.SetValue(str(self.currWave.frequency))
        self.input3.SetValue(str(self.currWave.time))
        self.input4.SetValue(str(self.currWave.phase))
        self.input6.SetValue(str(self.currWave.probeNum))

        self.currWave.id = self.WCIM

        self.choices3.append('Slot ' + str(self.currWave.id))
        self.choice3.Append('Slot ' + str(self.currWave.id))
        self.choice3.SetSelection(self.currWave.id)
        self.choice6.Append('Slot ' + str(self.currWave.id))
        self.choice6.SetSelection(self.currWave.id)

        self.waveMem.append((self.currWave, 'WS'))
        self.WCIM = self.WCIM + 1
        
    def on_close(self, event):
        self.Destroy()
        wx.Exit()

    def on_fft(self, event):
        fft = a.calculate_FFT(self.currWave.result, self.currWave.time)
        plots_frame = PlotsFrame(fft, self.currWave.time)  # Create an instance of PlotsFrame
        plots_frame.Show()  # Show the PlotsFrame instance

    def on_dct(self, event):
        dct = a.calculate_dct(self.currWave.result, self.currWave.time)
        plots_frame = PlotsFrame(dct, self.currWave.time)  # Create an instance of PlotsFrame
        plots_frame.Show()  # Show the PlotsFrame instance

    def on_dft(self, event):
        dft = a.calculate_DFT(self.currWave.result, self.currWave.time)
        plots_frame = PlotsFrame(dft, self.currWave.time)  # Create an instance of PlotsFrame
        plots_frame.Show()  # Show the PlotsFrame instance
class PlotsFrame(wx.Frame):
    def __init__(self, res, t):
        super().__init__(None, title="Plots Window", size=(800, 600))
        self.panel = wx.Panel(self)
        self.results = res
        self.time = t
        self.create_plots()
    
    def create_plots(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create a figure and subplots
        self.figure, self.axes = plt.subplots(2, 2)
        self.figure.tight_layout(pad=3.0)
        
        # Top-left plot
        x = self.results[:, 0]
        y = self.results[:, 1]
        self.axes[0, 0].plot(x, y)
        self.axes[0, 0].set_title('Real / frequency')
        
        # Top-right plot
        z = self.results[:, 2]
        self.axes[0, 1].plot(x, z)
        self.axes[0, 1].set_title('Imaginary / frequency')
        
        # Bottom-left plot
        cm = np.zeros(len(y), complex)
        for i in range(len(cm)):
            cm[i] = complex(y[i], z[i])
        ab = np.zeros(len(y))
        for a in range(len(ab)):
            ab[a] = abs(cm[a])
        self.axes[1, 0].plot(x, ab)
        self.axes[1, 0].set_title('Absolute / frequency')
        
        # Bottom-right plot with text
        an = np.angle(cm)
        #print(an)
        self.axes[1, 1].plot(x, an)
        self.axes[1, 1].set_title('Angle / frequency')
        
        # Create a canvas and add it to the panel
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(self.panel, label="IFFT")
        btn1.Bind(wx.EVT_BUTTON, self.on_IFFT)
        btn2 = wx.Button(self.panel, label="IDFT")
        btn2.Bind(wx.EVT_BUTTON, self.on_IDFT)
        btn3 = wx.Button(self.panel, label="IDCT")
        btn3.Bind(wx.EVT_BUTTON, self.on_IDCT)
        btn_sizer.Add(btn1, 0, wx.ALL, 5)
        btn_sizer.Add(btn2, 0, wx.ALL, 5)
        btn_sizer.Add(btn3, 0, wx.ALL, 5)
        
        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        
        self.panel.SetSizer(main_sizer)
        main_sizer.Fit(self.panel)
    
    def on_IFFT(self, event):
        ifft = a.calculate_ifft(self.results, self.time)
        pfi = PlotsFrameInverse(ifft, self.time)
        pfi.Show()
    
    def on_IDFT(self, event):
        idft = a.calculate_IDFT(self.results, self.time)
        pfi = PlotsFrameInverse(idft, self.time)
        pfi.Show()
    
    def on_IDCT(self, event):
        idct = a.calculate_idct(self.results, self.time)
        pfi = PlotsFrameInverse(idct, self.time)
        pfi.Show()

class PlotsFrameInverse(wx.Frame):
    def __init__(self, res, t):
        super().__init__(None, title="Plots Window", size=(800, 600))
        self.panel = wx.Panel(self)
        self.results = res
        self.time = t
        self.create_plots()
    
    def create_plots(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create a figure and subplots
        self.figure, self.axes = plt.subplots(2, 2)
        self.figure.tight_layout(pad=3.0)
        
        # Top-left plot
        x = self.results[:, 0]
        y = self.results[:, 1]
        self.axes[0, 0].plot(x, y)
        self.axes[0, 0].set_title('Real / frequency')
        
        # Top-right plot
        z = self.results[:, 2]
        self.axes[0, 1].plot(x, z)
        self.axes[0, 1].set_title('Imaginary / frequency')
        
        # Bottom-left plot
        cm = np.zeros(len(y), complex)
        for i in range(len(cm)):
            cm[i] = complex(y[i], z[i])
        ab = np.zeros(len(y))
        for a in range(len(ab)):
            ab[a] = abs(cm[a])
        self.axes[1, 0].plot(x, ab)
        self.axes[1, 0].set_title('Absolute / frequency')
        
        # Bottom-right plot with text
        an = np.angle(cm)
        #print(an)
        self.axes[1, 1].plot(x, an)
        self.axes[1, 1].set_title('Angle / frequency')
        
        # Create a canvas and add it to the panel
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)

            # Add buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(self.panel, label="Save")
        btn1.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(btn1, 0, wx.ALL, 5)
        
        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        
        self.panel.SetSizer(main_sizer)
        main_sizer.Fit(self.panel)
    
    def on_save(self, event):
        # Open file dialog for saving
        wildcard = "NumPy files (*.npy)|*.npy|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "Choose a file", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        cwd = os.getcwd()

        default_dir = cwd + "/waves"  # Replace this with your desired default directory
        dlg.SetDirectory(default_dir)

        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetFilename()  # Get the name of the file
            folder_path = dlg.GetDirectory()  # Get the folder path
            fileM = FM.FileM(folder_path)
            fileM.setValue(self.results)

            fileM.serialize(file_name)
        dlg.Destroy()

def startGui():
    app = wx.App()
    frame = MyFrame(None, title='Signaler v2.0')
    app.MainLoop()
