import wx
from wx._core import EVT_COMBOBOX

class ProgramPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour((100,100,100))
        
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(14)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        header = wx.StaticText(self, label="Programs")
        header.SetFont(font)
        self.vbox.Add(header, 0, wx.EXPAND|wx.ALL, 10)
        
        mapperLabel = wx.StaticText(self, label="Mapper")
        self.vbox.Add(mapperLabel, 0, wx.EXPAND|wx.ALL, 10)
        
        self.mapper = wx.ComboBox(self, style=wx.CB_READONLY, choices = ["bwa","bowtie"])
        self.mapper.SetValue("bwa")
        self.vbox.Add(self.mapper, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        snvCallerLabel = wx.StaticText(self, label="SNP caller")
        self.vbox.Add(snvCallerLabel, 0, wx.EXPAND|wx.ALL, 10)
        
        self.snvCaller = wx.ComboBox(self, style=wx.CB_READONLY, choices = ["samtools mpileup","GATK"])
        self.snvCaller.SetValue("samtools mpileup")
        self.vbox.Add(self.snvCaller, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        finalJobLabel = wx.StaticText(self, label="Final job")
        self.vbox.Add(finalJobLabel, 0, wx.EXPAND|wx.ALL, 10)
        
        self.finalJob = wx.ComboBox(self, style=wx.CB_READONLY, choices = ["mapping","snvCalling","haplotyping","phenotyping","allelicDiversity","findLoci"])
        self.finalJob.SetValue("phenotyping")
        self.finalJob.Bind(EVT_COMBOBOX, self.comboChange, self.finalJob)
        self.vbox.Add(self.finalJob, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.runButton = wx.Button(self, 7, "Run pipeline")
        self.Bind(wx.EVT_BUTTON, self.runAnalysis, id=7)
        self.vbox.Add(self.runButton,0,wx.EXPAND|wx.ALL, 10)

        self.SetSizer(self.vbox)
        
    def comboChange(self, event):
        pp = self.parent.poolPanel
        if self.finalJob.GetValue() in ["mapping","snvCalling"]:
            pp.vcfPanel.Disable()
            pp.gffPanel.Disable()
            pp.phenotypePanel.Disable()
        elif self.finalJob.GetValue() in ["snvCalling","haplotyping","allelicDiversity"]:
            if len(pp.samples) == 0:
                pp.vcfPanel.Enable()
            pp.gffPanel.Enable()
            pp.phenotypePanel.Disable()
        elif self.finalJob.GetValue() in ["phenotyping","findLoci"]:
            if len(pp.samples) == 0:
                pp.vcfPanel.Enable()
            pp.gffPanel.Enable()
            pp.phenotypePanel.Enable()
    
    def runAnalysis(self, event):
        pp = self.parent.poolPanel
        success = wx.MessageDialog(self,"Can run pipeline!","success", wx.OK)
        fail = wx.MessageDialog(self,"All fields have to be filled!","failed...", wx.OK)
        if self.finalJob.GetValue() in ["snvCalling","haplotyping","allelicDiversity","findLoci"]:
            if (pp.vcfPanel.inputFileText.GetValue() != "" or len(pp.samples) > 0) and pp.gffPanel.inputFileText.GetValue() != "":
                success.ShowModal()
                success.Destroy()
            else:
                fail.ShowModal()
                fail.Destroy()
        
        elif self.finalJob.GetValue() == "phenotyping":
            if (pp.vcfPanel.inputFileText.GetValue() != "" or len(pp.samples) > 0) and pp.gffPanel.inputFileText.GetValue()  != "" and pp.phenotypePanel.inputFileText.GetValue() != "":
                success.ShowModal()
                success.Destroy()
            else:
                fail.ShowModal()
                fail.Destroy()
        
        elif self.finalJob.GetValue() in ["mapping","snvCalling"]:
            if len(pp.samples) > 0:
                success.ShowModal()
                success.Destroy()
            else:
                fail.ShowModal()
                fail.Destroy()
         
        
        