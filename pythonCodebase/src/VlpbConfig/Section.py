'''
Created on Jun 7, 2013

@author: Jetse
'''
class Section:
    
    def __init__(self, name):
        self.name = name
        self.options = {}
        
    def getOption(self, name):
        return self.options[name]
    
    def setOption(self, name, value):
        self.options[name] = value
        
    def getAllOptions(self):
        return self.options