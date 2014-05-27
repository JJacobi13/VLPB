'''
Created on Jun 21, 2013

@author: Jetse
'''
import File
from model.cluster import ClusterJob

class BeagleFile(File.File):
    """The BeagleFile represents a BeagleFile file and contains instance variables to indicate the processes used on this BeagleFile file.
    The beaglefile contains multiple output files.
    
    """
    
    def __init__(self, pool, chrom, fileName = None, beageleInput=True):
        """The constructor of the BeagleFile sets the instance variables.
        :param chrom: The name of the chromosome
        :type chrom: str
        
        """
        self.chrom = chrom
        self.beageleInput = beageleInput
        super(BeagleFile,self).__init__(pool, fileName=fileName)
        
        self.gridJob = ClusterJob.getClusterJob(pool, chrom=chrom)
        
        if beageleInput == False:
            self.setFile(fileName)
        else:
            self.doseFile = None
            self.gprobsFile = None
            self.phasedFile = None
            self.rTwoFile = None
        
        

        
    def getSuffix(self):
        """implements the getSuffix of the file object. In the beagle file it is an prefix
        returns the chromosome for not overwriting files with differend chromosomes
        """
        return self.chrom
    
    def setFile(self, fileName):
        """Overrides the setFile of the :py:class:`File.File` sets all files to the automatic generated files of beagle.
        :param fileName: The index filename of the beagle output
        :type fileName: str. -- path to the file + index
        """
        self.fileName = fileName
        self.doseFile = fileName + ".dose.gz"
        self.gprobsFile = fileName + ".gprobs.gz"
        self.phasedFile = fileName + ".phased.gz"
        self.rTwoFile = fileName + ".r2"
        
    def getFile(self, outFile=None):
        """The method getFile overrides the super method getFile. When there is no outFile given, the index is returned.
        Else the output file of the given outFile is returned. When an file is compressed, the decompressed file is returned!
        Beagle returns compressed files by default.
        
        :param outFile: The file where to get the (extracted) filename of 
        :type outFile: "dose", "gprobs" or "phased"
        :returns: the name of the (extracted) file
        """
        if outFile == None:
            return super(BeagleFile, self).getFile()
        else:
            outFiles = {"dose": self.doseFile, "gprobs":self.gprobsFile, "phased":self.phasedFile,"rTwo":self.rTwoFile}
            oldFilename = self.fileName
            self.fileName = outFiles[outFile]
            toReturn = super(BeagleFile, self).getFile()
            outFiles[outFile] = self.fileName
            self.fileName = oldFilename
            return toReturn
        