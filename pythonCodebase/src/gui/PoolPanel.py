import wx, SamplePanel, GuiFactory

class PoolPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.samples = []
        self.SetBackgroundColour((200,200,200))
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.poolPanel = self.getPoolNamePanel()
        self.vbox.Add(self.poolPanel, 0, wx.EXPAND|wx.ALL,5)
        
        self.vcfPanel = GuiFactory.createFileInputPanel(self, "VCF")
        self.vcfPanel.Bind(wx.EVT_TEXT, self.vcfChange, self.vcfPanel.inputFileText)
        self.vbox.Add(self.vcfPanel, 0, wx.EXPAND|wx.ALL,5)
        
        self.gffPanel = GuiFactory.createFileInputPanel(self, "GFF")
        self.vbox.Add(self.gffPanel, 0, wx.EXPAND|wx.ALL,5)
         
        self.phenotypePanel = GuiFactory.createFileInputPanel(self, "Phenotype data")
        self.vbox.Add(self.phenotypePanel, 0, wx.EXPAND|wx.ALL,5)
        
        self.addButton = wx.Button(self, 1, "Add samples", size = (100,30))
        self.Bind(wx.EVT_BUTTON, self.addSample, id=1)
        self.vbox.Add(self.addButton,0,wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.FIXED_MINSIZE, 5)
        
        self.SetSizer(self.vbox)
        
    def getPoolNamePanel(self):
        poolNamePanel = wx.Panel(self)
        self.headerbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.poolLabel = wx.StaticText(poolNamePanel, label="poolname", size = (100,30))
        self.headerbox.Add(self.poolLabel)
        self.changePoolname = wx.Button(poolNamePanel, 2, "Change")
        self.Bind(wx.EVT_BUTTON, self.changePoolName, id=2)
        self.headerbox.Add(self.changePoolname)
        poolNamePanel.SetSizer(self.headerbox)
        return poolNamePanel

    def addSample(self, event):
        dialog = wx.FileDialog(None, style = wx.MULTIPLE)
        dialog.SetWildcard("bam files (*.bam)|*.bam|fastq files (*.fastq,*.fasta,*.fa)|*.fastq,*.fasta,*.fa")
        if dialog.ShowModal() == wx.ID_OK:
            for filePath in dialog.GetPaths():
                sample = SamplePanel.SamplePanel(self, filePath)
                self.samples.append(sample)
                self.vbox.Add(sample,0,wx.EXPAND | wx.ALL,5)
            self.Layout()
            self.parent.fSizer.Layout()
            
    def changePoolName(self, event):
        text = self.poolLabel.GetLabelText()
        self.headerbox.Hide(self.poolLabel)
        self.headerbox.Remove(self.poolLabel)
        self.headerbox.Hide(self.changePoolname)
        self.headerbox.Remove(self.changePoolname)
        
        self.poolLabel = wx.TextCtrl(self.poolPanel)
        self.poolLabel.AppendText(text)
        self.headerbox.Add(self.poolLabel)
        
        self.changePoolname = wx.Button(self.poolPanel, 3, "apply")
        self.Bind(wx.EVT_BUTTON, self.applyNewName, id=3)
        self.headerbox.Add(self.changePoolname)
        
        self.headerbox.Layout()
        self.parent.fSizer.Layout()
        
    def applyNewName(self, event):
        text = self.poolLabel.GetLabelText()
        self.headerbox.Hide(self.poolLabel)
        self.headerbox.Remove(self.poolLabel)
        self.headerbox.Hide(self.changePoolname)
        self.headerbox.Remove(self.changePoolname)
        
        self.poolLabel = wx.StaticText(self.poolPanel, label=text, size = (100,20))
        self.headerbox.Add(self.poolLabel)
        
        self.changePoolname = wx.Button(self.poolPanel, 2, "Change")
        self.Bind(wx.EVT_BUTTON, self.changePoolName, id=2)
        self.headerbox.Add(self.changePoolname)
        
        self.headerbox.Layout()
        self.parent.fSizer.Layout()
    
    def vcfChange(self, event):
        selected = self.parent.programPanel.finalJob.GetValue()
        if self.vcfPanel.inputFileText.GetLabelText() == "":
            self.addButton.Enable()
            self.parent.programPanel.mapper.Enable()
            self.parent.programPanel.snvCaller.Enable()
            self.parent.programPanel.finalJob.Clear()
            self.parent.programPanel.finalJob.AppendItems(["mapping","snvCalling","haplotyping","phenotyping","allelicDiversity","findLoci"])
            self.parent.programPanel.finalJob.SetValue(selected)
            
        else:
            self.addButton.Disable()
            self.parent.programPanel.mapper.Disable()
            self.parent.programPanel.snvCaller.Disable()
            self.parent.programPanel.finalJob.Clear()
            self.parent.programPanel.finalJob.AppendItems(["haplotyping","phenotyping","allelicDiversity","findLoci"])
            self.parent.programPanel.finalJob.SetValue(selected)
            