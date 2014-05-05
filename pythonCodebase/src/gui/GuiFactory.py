import wx
'''
Created on Aug 27, 2013

@author: Jetse
'''
def createFileInputPanel(parent, label):
    fileInputPanel = wx.Panel(parent) 
    poolFileSizer = wx.BoxSizer(wx.HORIZONTAL)
    
    gffLabel = wx.StaticText(fileInputPanel, label=label)
    poolFileSizer.Add(gffLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
    
    fileInputPanel.inputFileText = wx.TextCtrl(fileInputPanel)
    poolFileSizer.Add(fileInputPanel.inputFileText,1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
    
    browseButton = wx.Button(fileInputPanel, 8, "Browse", size = (50,20))
    def browse(event):
        dialog = wx.FileDialog(None, style = wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            fileInputPanel.inputFileText.Clear()
            fileInputPanel.inputFileText.write(dialog.GetPath())
            parent.Layout()
    
    fileInputPanel.Bind(wx.EVT_BUTTON, browse, browseButton)
    poolFileSizer.Add(browseButton, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 10)
    
    fileInputPanel.SetSizer(poolFileSizer)
    fileInputPanel.Layout()
    return fileInputPanel