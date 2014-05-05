import os
from model import FastqFile, BamFile

class Sample(object):
    """The sample class represents a sample.
    
    """
    
    def __init__(self, pool, libName):
        """The constructor of the Sample object sets the given parameters as instance variables and creates the output directory if not exists
        :param pool: the pool this sample is a part of
        :type pool: :py:class:`Pool.Pool`
        :param libName: The name of this sample
        :type libName: Str
        
        """
        self.pool = pool
        self.outputDir = pool.outputDir + "/" + libName + "/"
        self.libName = libName
        
        self.forwardFq = None
        self.reversedFq = None
        self.bam = None
        
        if not os.path.isdir(self.outputDir):
            os.makedirs(self.outputDir)
        
    def setForwardFq(self, fileName):
        """Setter for setting the forward fastq file as a :py:class:`FastqFile.FastqFile`
        
        """
        self.forwardFq = FastqFile.FastqFile(self.pool, self, fileName)
        
    def setReversedFq(self, fileName):
        """Setter for setting the reversed fastq file as a :py:class:`FastqFile.FastqFile`
        
        """
        self.reversedFq = FastqFile.FastqFile(self.pool, self, fileName, forward=False)
    
    def setbam(self, fileName):
        """Setter for setting the bam file as a :py:class:`FastqFile.FastqFile`
        
        """
        self.bam = BamFile.BamFile(self.pool, self, fileName)
        
    def __str__(self):
        return "Sample[forwardFq: " + str(self.forwardFq) + ", " + "reversedFq: " + str(self.reversedFq) + " Library name: " + self.libName + " bam: " + str(self.bam) + " ]"

    def __repr__(self):
        return self.__str__()