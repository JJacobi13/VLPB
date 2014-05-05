"""The configuration module regulates all configuration settings which are in the ini file.
This is done by 2 objects, :class:`Config` and :class:`Section`.
The :class:`Config` regulates the parsing of the ini file and the communication with other objects
The :class:`Section` represents a section of the ini file
"""
import os

class Config(object):
    """The Config class regulates everything of the configuration of the programs.
    This information is read from the iniFile config.ini which is located in this directory.

    """
    def __init__(self):
        """The constructor opens the ini file for easy access in this object to the ini file.
        
        """
        self.phenoData = None
        self.gffFile = None
        self.bedFile = None
        self.mapper = "BWA"
        self.snvCaller = "samtools"
        self.multiThread = False
        self.parseIni(os.path.dirname(__file__) + "/config.ini")
        
    def getPath(self, item):
        """The method getPath retrieves the path of an item from the ini file.
        
        :param item: the item where to get the path from, can be the reference genome or a program
        :type item: str
        :returns: str -- absolute path to the program
        """
        return self.sections["paths"].getOption(item)
    
    def setPath(self, item, path):
        """For testing and for changing a reference genome the path can be changed with this method.
        :param item: the item where to set the path for, can be the reference genome or a program
        :type item: str
        :param path: the new path of this item
        :type item: str -- path
        """
        self.sections["paths"].setOption(item, os.path.abspath(path))
    
    def getGridOptions(self, item):
        self.sections["grid"].getOption(item)
    
    def getProgramOptions(self, programName):
        """The method getProgramOptions retrieves all options from the ini file for one specific program.
        
        :param programName: The name of the program where to get the options from
        :type programName: str
        :returns: a dictionary with all options (key value pairs, value is empty string if there is no value for param)
        
        """
        
        return self.sections[programName].getAllOptions()
    
    def getProgram(self, possibleNames):
        """The method getPrograms checks which of the possibleNames occurs as a header in the ini file
        
        """
        for possibleName in possibleNames:
            if possibleName in self.sections:
                return possibleName
    
    def parseIni(self, iniFile):
        self.sections = {}
        name="default"
        try:
            with open(iniFile) as ini:
                content = ini.readlines()
            for line in content:
                line = line.rstrip()
                if "[" in line and "]" in line:
                    name = line.replace("[","").replace("]","")
                    self.sections[name] = Section(name)
                elif line:
                    splitLine = line.partition("=")
                    self.sections[name].setOption(splitLine[0], splitLine[2])
        except(IOError):
            raise IOError("can not read configuration file at " + os.path.abspath(iniFile))
                
class Section:
    """The class section represents a section from the ini file.
    This section contains a header name and a dictionary of key-value pairs.
    The value is an empty string if this option has no value
    
    """
    def __init__(self, name):
        self.name = name
        self.options = {}
        
    def getOption(self, name):
        """The method getOption is a getter for retrieving a specific option 
                
        """
        return self.options[name]
    
    def setOption(self, name, value):
        """The method setOption is a setter for setting a new option, overwrites when exist.
        
        """
        self.options[name] = value
        
    def getAllOptions(self):
        """Getter for retrieving the full dictionary in once.
        
        """
        return self.options