from programs import Program
import re, os, tarfile

class Decompressor(Program.Program):
    """The Decompressor class regulates all Decompress functions
    
    .. module:: programs
    
    .. moduleauthor:: Jetse Jacobi
    
    """    
    def extract(self, inputFile):
        """This function calls extractGz if the file .gz compressed, if this file is .tar.gz compressed, the method extractTarGz is called
        
        :param inputFile: The compressed .gz or . tar.gz file which has to be extracted
        :type inputFile: instance of a child object of the :py:class:`File.File` object
        :returns: str -- The paths to the extracted file, if multiple files are extracted, the first file is returned
        :raises: TypeError -- When the file type is not recognized
        
        """
        if inputFile.sample !=None: outDir = inputFile.sample.outputDir
        else: outDir = inputFile.pool.outputDir
        if inputFile.fileName.endswith(".tar.gz"):
            return self._extractTarGz(inputFile, outDir)
        elif inputFile.fileName.endswith(".gz"):
            return self._extractGz(inputFile, outDir)
        else:
            raise TypeError("Unrecognized file format!")
    
    def _extractGz(self, inputFile, outDir):
        """This function extracts the .gz compressed files
        
        :param inputFile: The .gz file to extract
        :type inputFile: instance of a child object of the :py:class:`File.File` object
        :returns: str -- The path to the extracted file
        
        """
        
        match = re.search(r"(.*)\.([a-zA-Z0-9]*)\.gz", os.path.basename(inputFile.fileName))
        outFile = outDir + match.group(1) + "." + match.group(2)
        cmd = "gunzip -c " + inputFile.fileName + " > " + outFile
        self.execute(cmd, "gunzip", inputFile)
        inputFile.fileName = outFile
        return outFile
    
    def _extractTarGz(self, inputFile, outDir):
        """This function extracts the given .tar.gz compressed files
        
        :param inputFile: The .tar.gz file to extract
        :type inputFile: instance of a child object of the :py:class:`File.File` object
        :returns: str. -- The path to the extracted file, if multiple files, only the first file is returned
        
        """
        
        tar = tarfile.open(inputFile.fileName, "r:gz")
        filesInTar = tar.getmembers()
        for fileInTar in filesInTar:
            outFile = outDir + fileInTar.name
            tar.extract(fileInTar, outDir)
            return outFile
        
