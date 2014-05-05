'''
Created on Jun 21, 2013

@author: Jetse
'''

import File
from model.cluster import ClusterJob
class BamFile(File.File):
    """The bamFile represents a sam or bam file and contains instance variables to indicate the processes used on this bam file
    
    """
    
    def __init__(self,pool, sample, fileName=None, sam=False, sortedBam = False, headerLine = False, duplicates = True, mdTag = False, index = False):
        """The constructor of the bam file sets all default vaules of the instance variables
        :param sam: boolean whether this file is a sam or bam file
        :param sortedBam: boolean whether this file is sorted or not
        :param headerLine: boolean whether this file contains an @rg tag
        :param duplicates: boolean whether the possible pcr duplicates are already removed
        :param mdTag: boolean whether the md tag is already added to this file
        :param index: whether there is already created an index of this bam file
        """
        self.sam = sam
        self.sorted = sortedBam
        self.headerLine = headerLine
        self.duplicates = duplicates
        self.mdTag = mdTag
        self.index = index
        self.gridJob = ClusterJob.getClusterJob(pool, sample)
        super(BamFile,self).__init__(pool, sample,fileName)
        
        
    def getSuffix(self):
        if self.sam == True:
            return ".sam"
        return ".bam"
    
    def __str__(self):
        return "BamFile[fileName=" + self.fileName + ", sam: " + str(self.sam) + ", sorted: "+ str(self.sorted) +"]"
    
    def __repr__(self):
        return self.__str__()