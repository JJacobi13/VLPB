'''
Created on Jun 21, 2013

@author: Jetse
'''
import File
from model.cluster import ClusterJob

class FastqFile(File.File):
    """The FastqFile represents a fq file and contains instance variables to indicate the processes used on this fq file
    This fastq file holds the forward and reversed reads in an array list of files
    
    """
    
    def __init__(self, pool, sample, fileName=None, forward=True, hq=False):
        """The constructor of the fastq file sets the variable whether the quality control is done. 
        :param hq: Whether the quality control is already done on this file, so the reads all have a High Quality
        :param forward: Whether this fastq file are the forward reads or the reversed reads
        """
        super(FastqFile,self).__init__(pool, sample=sample, fileName=fileName)
        self.hq = hq
        self.forward = forward
        self.gridJob = ClusterJob.getClusterJob(pool, sample)
        
    def getSuffix(self):
        if self.forward == True:
            return "_0.fq"
        else:
            return "_1.fq"