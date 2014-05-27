'''
Created on Sep 2, 2013

@author: Jetse
'''
from subprocess import Popen, PIPE

class Node(object):
    """The node object tracks whether a job can be submitted to this node or not.
    
    """
    
    def __init__(self, nodeName):
        """The constructor sets the name and checks the free memory and number of available processors.
        
        :param nodeName: The name of the node
        :type nodeName: str
        """
        self.nodeName = nodeName
        
        #Get the free memory
        output,error = Popen("ssh " + self.nodeName + " df -h /state/partition1/jaco001/", shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.freeMem = output.split()[10]
        if self.freeMem[-1] == "T":
            self.freeMem = int(float(self.freeMem[:-1])) * 1000
        else: self.freeMem = int(float(self.freeMem[:-1]))
        self.resMem = 0
        
        #get the number of procs
        output,error = Popen("qhost | grep " + self.nodeName, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.procs = int(int(output.split()[2])/2)
        self.resProcs = 0
    
    def getFreeProcs(self):
        """getFreeProcs is a simple getter for getting the number of free processors
        
        """
        return self.procs - self.resProcs
        
    def getAvailableMem(self):
        """The method getAvailableMem is a simple getter for checking whether there is enough hdd memory on the node
        
        """
        return self.freeMem - self.resMem
    
    def addJob(self, job):
        """When adding a job, the node has to be updated...
        
        """
        self.resProcs = self.resProcs +1
        self.resMem = self.resMem + job.maxMemNeeded
    
    def removeJob(self, job):
        """When removing a job, the node has to be updated...
        
        """
        self.resProcs = self.resProcs -1
        self.resMem = self.resMem - job.maxMemNeeded

