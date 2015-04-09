from __future__ import unicode_literals
import wx


myEVT_SCAN = wx.NewEventType()
EVT_SCAN = wx.PyEventBinder(myEVT_SCAN)


class ScanEvent(wx.PyCommandEvent):

    def __init__(self, etype, eid, freqs=None):
        super(ScanEvent, self).__init__(etype, eid)
        self.freqs = freqs


class App(wx.App):

    def __init__(self, scanner, *args, **kwargs):
        self.scanner = scanner
        super(App, self).__init__(*args, **kwargs)

    def OnInit(self):
        self.main_window = MainWindow(parent=None, size=(800, 600))
        self.SetTopWindow(self.main_window)
        self.main_window.Center()
        self.scanner.start(88e6, 108e6, 125e3)
        return True


class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Scanner'
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scan_panel = ScanPanel(parent=self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Show(show=True)

    def OnClose(self, event):
        self.Destroy()


class ScanPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(ScanPanel, self).__init__(*args, **kwargs)
        self.right_panel = ScanRightPanel(parent=self)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.right_panel, 0, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)


class ScanRightPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(ScanRightPanel, self).__init__(*args, **kwargs)

        self.freq_list = FreqListCtrl(parent=self, size=(200, 400))
        self.scan_controls_panel = ScanControlsPanel(parent=self)
        self.inspect_button = InspectButton(parent=self)
        self.toggle_scan_button = ToggleScanButton(parent=self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.freq_list, 1, wx.EXPAND)
        self.sizer.Add(self.scan_controls_panel, 0, wx.EXPAND)
        self.sizer.Add(self.inspect_button, 0, wx.EXPAND)
        self.sizer.Add(self.toggle_scan_button, 0, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)


class ScanControlsPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(ScanControlsPanel, self).__init__(*args, **kwargs)

        self.low_freq = wx.TextCtrl(parent=self, value='88e6', style=wx.TE_RIGHT)
        self.high_freq = wx.TextCtrl(parent=self, value='108e6', style=wx.TE_RIGHT)
        self.step_freq = wx.TextCtrl(parent=self, value='125e3', style=wx.TE_RIGHT)

        self.sizer = wx.GridBagSizer(vgap=2, hgap=5)

        for i, (label, ctrl) in enumerate(zip(['low', 'high', 'step'],
                                              [self.low_freq, self.high_freq, self.step_freq])):
            self.sizer.Add(wx.StaticText(parent=self, label=label), pos=(i, 0), flag=wx.ALIGN_CENTER_VERTICAL)
            self.sizer.Add(ctrl, pos=(i, 1), flag=wx.EXPAND)
            self.sizer.Add(wx.StaticText(parent=self, label='Hz'),
                           pos=(i, 2),
                           flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL)

        self.sizer.AddGrowableCol(1)
        self.SetSizerAndFit(self.sizer)


class FreqListCtrl(wx.ListCtrl):

    def __init__(self, *args, **kwargs):
        kwargs['style'] = kwargs.setdefault('style', wx.LC_REPORT) | wx.LC_REPORT
        super(FreqListCtrl, self).__init__(*args, **kwargs)

        self.InsertColumn(0, 'Frequency', width=100)
        self.InsertColumn(1, 'dBFS', width=100)

        self.scanner = wx.GetApp().scanner

        self.scanner.events.on_analyzed_data += lambda freqs: wx.CallAfter(self.on_analyzed_data, freqs)

    def on_analyzed_data(self, freqs):
        freqs = [(f, dbfs) for f, dbfs in freqs.iteritems()]
        str_freqs = [(str(f), str(dbfs)) for f, dbfs in freqs]

        old_freqs = set()
        for i in range(self.GetItemCount()):
            if self.GetItem(i, 1).GetText():
                # don't count cols marked as disappeared
                # during the previous iteration
                old_freqs.add(self.GetItem(i, 0).GetText())

        new_freqs = {f[0] for f in str_freqs}

        appeared_freqs = new_freqs - old_freqs
        disappeared_freqs = old_freqs - new_freqs

        self.DeleteAllItems()

        i = 0  # declare i for the next loop in case str_freqs is empty
        for i, (f, dbfs) in enumerate(str_freqs):
            self.InsertStringItem(i, '')
            self.SetStringItem(i, 0, f)
            self.SetStringItem(i, 1, dbfs)
            if f in appeared_freqs:
                self.SetItemBackgroundColour(i, wx.Colour(32, 255, 32))

        for j, f in enumerate(disappeared_freqs, i+1):
            self.InsertStringItem(j, f)
            self.SetItemBackgroundColour(j, wx.Colour(255, 32, 32))


class ToggleScanButton(wx.Button):

    START_LABEL = 'START'
    STOP_LABEL = 'STOP'

    def __init__(self, *args, **kwargs):
        kwargs['label'] = self.STOP_LABEL
        super(ToggleScanButton, self).__init__(*args, **kwargs)

        self.scanner = wx.GetApp().scanner

        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        if self.GetLabelText() == self.STOP_LABEL:
            # scan is running
            self.scanner.stop()
            self.GetParent().freq_list.DeleteAllItems()
            self.SetLabel(self.START_LABEL)
        else:
            # scan is not running
            self.scanner.start(88e6, 108e6, 125e3)
            self.SetLabel(self.STOP_LABEL)


class InspectButton(wx.Button):

    def __init__(self, *args, **kwargs):
        kwargs['label'] = 'INSPECT'
        super(InspectButton, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        pass
