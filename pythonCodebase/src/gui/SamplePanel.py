import wx

class SamplePanel(wx.Panel):
    def __init__(self, parent, filePath):
        wx.Panel.__init__(self, parent)
        
        self.Parent.vcfPanel.Disable()
        
        self.SetBackgroundColour("red")
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(wx.StaticText(self, label=filePath), 1, wx.EXPAND)
        
        self.remButton = wx.Button(self, 5, "remove", size = (50,20))
        self.Bind(wx.EVT_BUTTON, self.removeSample, id=5)
        self.hbox.Add(self.remButton,0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        
        self.SetSizer(self.hbox)
        
    def removeSample(self, event):
        self.Hide()
        self.Parent.samples.remove(self)
        self.GetParent().Layout()
        self.GetParent().parent.fSizer.Layout()
        if len(self.Parent.samples) == 0 and self.Parent.parent.programPanel.finalJob.GetValue() in ["snvCalling","haplotyping","allelicDiversity","findLoci","phenotyping"]:
            self.Parent.vcfPanel.Enable()
        del self
        