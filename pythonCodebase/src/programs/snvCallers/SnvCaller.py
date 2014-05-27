from programs import Program, ConversionTools
import time, logging, threading
from model.cluster import Grid

#converting is needed for synchronyzing all threads, samtools has to be called once, not once for each thread!
converting = "not done"

class SnvCaller(threading.Thread, Program.Program):
    """The SnvCaller class regulates all programs which can call the SNV's
    
    """
    def __init__(self, pool, chromosome = None):
        super(SnvCaller, self).__init__()
        self.pool = pool
        self.checkInput(pool)
        self.chromosome = chromosome
    
    def run(self):
        try:
            self.callSnvs()
        except Exception as x:
            logging.error(x)
            
            
    def callSnvs(self, pool):
        raise NotImplementedError("All subclasses have to implement the callSnvs method...")
    
    def checkInput(self, pool):
        """The method callSNVs checks if all conversion steps are executed on the bam file of all samples.
        Then the program to call SNVs with is read from the configuration file with the method: :py:meth:`Configuration.Configuration.getProgram`.
        After this check the read method is executed
        
        """
        if len(pool.samples) == 0:
            logging.warning("No samples to execute SNV caller on")
            return
        
        global converting
        if converting == "not done":
            
            converting = "converting"
            jobs = []
            for sample in pool.samples:
                ct = ConversionTools.ConversionTools()
                ct.addHeaderLine(sample)
                ct.removeDuplicates(sample)
#                     ct.addMdTag(sample.bam)
                
                ct.createBamIndex(sample)

                jobs.append(sample.bam.gridJob)
                
            if Grid.useGrid==True:
                sampleGrid = Grid.Grid()
                if jobs[0].noOfCommands > 0:
                    sampleGrid.submitJobs(jobs)
                
            converting = "finished"
        
        #wait till other thread finished the bam indexing    
        while converting != "finished":
            time.sleep(60)
            
        self.pool = pool
    
    def _convertToVcf(self, vcfFile):
        """This method converts a bcf file to a vcf file of a given file object.
        
        :param vcfFile: The bcf file which has to be converted to vcf.
        :type vcfFile: an instance of a :py:class:`VcfFile.VcfFile` object
        
        """
        if vcfFile == None:
            raise TypeError("Pool contains no vcf file!")
        
        if vcfFile.bcf == False:
            return
        outputFile = vcfFile.getNewFileName()
        cmd = Program.config.getPath("bcftools") + " view " + self.getProgramArguments("bcftools view") + " " + vcfFile.getFile() + " > " + outputFile
        self.execute(cmd,"bcftools view", vcfFile)
        vcfFile.bcf = False
        vcfFile.setFile(outputFile)
    