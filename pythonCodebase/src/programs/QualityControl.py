from programs import Program
import os, stat

class QualityControl(Program.Program):
    """The class qualityControl regulates all processes which have to do with the quality control.
    
    """
    
    def doQualityControl(self, sample):
        """The method doQualityControl executes the quality control on the raw data of the forward and reversed reads of the sample
        
        :param sample: The sample where to do a quality control on
        :type sample: :py:class:`Sample.Sample`
        :raises: ValueError when the sample has no forward fastq file
        
        """
        
        if sample.forwardFq == None:
            raise ValueError("The sample has no forward fastq file!")
        
#         if sample.forwardFq.hq[0] == False:  
#         self._doQualityControlOnFile(sample.forwardFq)
        
#         if sample.reversedFq != None and sample.reversedFq.hq == False:
#             self._doQualityControlOnFile(sample.reversedFq)
        
    def _doQualityControlOnFile(self, fqFile):
        """This method regulates the multiple input fastq files of the sample. This method calls the method _executeQualityControl for each file in given files, 
        executes this method once when not an list is given.
        Also an empty output file is created where the method _executeQualityControl can write his output to to merge all given fastq files
        
        :param fqFile: The file to do the quality control on
        :type fqFile: instance of a child object of the :py:class:`File.File` object
        
        """
        
        if type(fqFile) is list:
            outFile = fqFile[0].getNewFileName()
            open(outFile, 'w').close()
            for fastqFile in fqFile:
                self._executeQualityControl(fastqFile, outFile)
        else:
            outFile = fqFile.getNewFileName()
            open(outFile, 'w').close()
            self._executeQualityControl(fqFile, outFile)
            
    def _executeQualityControl(self, fqFile, outFile):
        """This method executes the quality control on a given fastq file. It adds the output to an existing file for when the input consists of multiple fastq files.
        :param fqFile: The file to do the quality control on
        :type fqFile: instance of a child object of the :py:class:`FastqFile.FastqFile` object
        :param outFile: The file to write the output to
        :type outputFile: str -- path to the output file
        
        """
        
        inFile = fqFile.getFile()   
        self.execute("cat " + inFile + " >> " + outFile, "qc (not implemented, just merging the fastq files...)", fqFile)
        os.chmod(outFile, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR)
        fqFile.setFile(outFile)
        fqFile.hq = True