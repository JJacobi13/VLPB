'''
Created on Jun 21, 2013

@author: Jetse
'''
import File
from model.cluster import ClusterJob

class VcfFile(File.File):
    """The VcfFile represents a vcf or bcf file and contains instance variables to indicate the processes used on this vcf file
    
    """
    
    def __init__(self, pool, fileName=None, bcf = False, filtered = False, phased=False, chrom=None):
        """The constructor of the vcf file sets the given variables as instance variables.
        :param bcf: boolean whether the file is bcf or vcf, default: True
        :param filtered: boolean whether the file is already filtered or not, default: True
        """
        self.bcf = bcf
        self.chrom = chrom
        self.filtered = filtered
        self.phased = phased
        super(VcfFile,self).__init__(pool, fileName=fileName)  
        self.gridJob = ClusterJob.getClusterJob(pool, chrom=chrom)
    
    def getSuffix(self):
        if self.chrom == None:
            prefix = ""
        else:
            prefix = "_" + self.chrom
        
        if self.bcf == True:
            return prefix + ".bcf"
        return prefix + ".vcf"