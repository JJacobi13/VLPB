from programs import Program, QualityControl
from model import BamFile
import subprocess, os

class Mapper(Program.Program):
    """The class Mapper regulates all mapping processes, available mapper: BWA
    
    """
    
    def map(self, sample):
        """The method map checks which mapper has to be executed from the :class:`Configuration` object.
        First the quality control has to be done to the samples, after the quality control, the mapping will be executed.
        
        :param sample: The sample to map against his reference genome
        :type sample: an instance of :py:class:`Sample.Sample`
        
        """
        QualityControl.QualityControl().doQualityControl(sample)

        if Program.config.getProgram(["BWA"]):
            self._executeBwa(sample.forwardFq, sample.reversedFq)
    
    def _executeBwa(self,forwardFq, reversedFq=None):
        """The method executeBwa executes the mapping with BWA.
        
        :param forwardFq: The forward fastq file to map against the reference genome
        :type forwardFq: an instance of :py:class:`FastqFile.FastqFile`
        :param reversedFq: The reversed fastq file to map against the reference genome
        :type reversedFq: an instance of :py:class:`FastqFile.FastqFile`, None if the data has no paired end reads.
        
        """
        if os.path.exists(Program.config.getPath("refGenome") + ".pac") == False:
            exitStatus = subprocess.call("bwa index " + Program.config.getPath("refGenome"))
            if exitStatus == 1:
                print("ERROR: Failed to create a bwa index file for the reference genome, do I have permissions to write in the directory of the reference genome?")
                exit(1)
        ##Build the command
        cmd = Program.config.getPath("bwa")  # @UndefinedVariable
        if reversedFq == None:
            cmd = cmd + " samse "
        else:
            cmd = cmd + " sampe " + self.getProgramArguments("BWA")
            
        cmd = cmd + Program.config.getPath("refGenome")

        #add the .sai files to the command
        forwardMapped = self._bwaAlign(forwardFq)
        cmd = cmd + " " + forwardMapped
        if reversedFq != None:
            reversedMapped = self._bwaAlign(reversedFq)
            cmd = cmd + " " + reversedMapped
        
        #add the high quality reads to the command
        cmd = cmd + " " + forwardFq.fileName
        if reversedFq != None:
            cmd = cmd + " " + reversedFq.fileName
        
        #add the output file to the command
        forwardFq.sample.bam = BamFile.BamFile(forwardFq.pool, forwardFq.sample, sam=True)
        cmd = cmd +  " > " + forwardFq.sample.bam.getFile()
        
        ##Execute the command
        self.execute(cmd, "BWA", forwardFq.sample.bam)
        
        ##Cleanup the mess
        self.execute("rm " + forwardMapped, "rm", forwardFq)
        if reversedFq != None:
            self.execute("rm " + reversedMapped, "rm", reversedFq)

    def _bwaAlign(self, inputFile):
        """The method bwaAlign aligns the reads with bwa aln to the reference genome
        
        :param inputFile: The file to map against the reference genome
        :type inputFile: an instance of :py:class:`FastqFile.FastqFile`

        """
        
        outputFile = inputFile.sample.outputDir + inputFile.sample.libName  + "_0.sai"
        if inputFile.forward == False:
            outputFile = inputFile.sample.outputDir + inputFile.sample.libName  + "_1.sai"
            
        cmd = Program.config.getPath("bwa") + " aln " + self.getProgramArguments("BWA aln") + Program.config.getPath("refGenome") + " " + inputFile.getFile() + " > " + outputFile
        self.execute(cmd, "BWA aln", inputFile)
        return outputFile
    
    
    
    
