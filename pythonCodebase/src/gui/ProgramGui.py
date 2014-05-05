import wx, PoolPanel
import ProgramPanel

class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame,self).__init__(None, title="VLPB ", size=(600,800))
        
        self.createGui()
        self.Show()
        
    def createGui(self):
        self.SetBackgroundColour((0,0,0))
        self.fSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.programPanel = ProgramPanel.ProgramPanel(self)
        self.fSizer.Add(self.programPanel, 0, wx.EXPAND | wx.TOP |wx.BOTTOM|wx.LEFT, 10)
        
        self.poolPanel = PoolPanel.PoolPanel(self)
        self.fSizer.Add(self.poolPanel, 1, wx.EXPAND | wx.TOP |wx.BOTTOM|wx.RIGHT , 10)
        self.SetSizer(self.fSizer)

if __name__ == '__main__':  
    app = wx.App(redirect=False)     
    MainFrame()
    app.MainLoop()