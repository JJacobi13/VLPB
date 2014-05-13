from programs import Program
from model import VcfFile
from model.cluster import Grid
from tools import Tools
import os, copy, threading, logging
from programs.snvCallers import SamtoolsMpileup, Gatk
from programs.snvCallers.SnvCaller import SnvCaller

class Haplotyper(threading.Thread, Program.Program):
    """The Haplotyper class regulates the haplotyping of a vcf file
    
    """
    
    def __init__(self, pool, chrom):
        super(Haplotyper, self).__init__()
        self.pool = pool
        self.chrom = chrom
        
    def run(self):
#         try:
        self.callHaplotypes()
#         except Exception as x:
#             logging.error(x)
    
    def callHaplotypes(self):
        """The method callHaplotypes calls the haplotypes of a vcf file. When the vcf file is not set, first the SNVs are called with the :py:class:`SnvCaller.SnvCaller` object
        In future when multiple programs for haplotyping are implemented, here the check will be performed which haplotyper to execute. First only beagle is implemented so this method will be called
        :param pool: The pool a haplotyping tools has to be executed on
        :type pool: an instance of a :py:class:`Pool.Pool` object
        
        """
        if self.chrom in self.pool.vcf:
            if self.chrom == None:
                logging.info("SNP calling already done")
            else:
                logging.info("SNP calling already done on " + self.chrom)
        else:
            snvCaller = Program.config.snvCaller  # @UndefinedVariable
            if snvCaller == "samtools":
                samThread = SamtoolsMpileup.SamtoolsMpileup(self.pool,self.chrom)
                samThread.callSnvs()
                
            elif snvCaller == "GATK":
                samThread = Gatk.Gatk(self.pool,self.chrom)
                samThread.callSnvs()
        
        
                
        self._executeBeagle(self.pool, self.chrom)
    
    def getPhased(self, fileName):
        with open(fileName) as fileReader:
            for line in fileReader:
                if line.startswith("#"):
                    continue
                if "|" in line.split("\t")[-1]:
                    return True
                return False
    
    def _executeBeagle(self, pool, chrom):
        """The method executeBeagle executes beagle. First the vcf file is converted to a format beagle needs, then beagle is executed.
        :param pool: The pool beagle has to executed on
        :type pool: an instance of a :py:class:`Pool.Pool` object
        
        """
        if self.getPhased(pool.vcf[chrom].fileName):
            return
        
        if pool.vcf[chrom].bcf == True:
            SnvCaller(pool,chrom)._convertToVcf(pool.vcf[chrom])
        
#         self.execute("grep -v [[:space:]]N " + pool.vcf[chrom].fileName + " > " + pool.vcf[chrom].getNewFileName(), "grep", pool.vcf[chrom])
#         pool.vcf[chrom].setFile(pool.vcf[chrom].getNewFileName())
        
        origVcf = copy.copy(pool.vcf[chrom])
        
        beagleFile = self._createBeagleInput(origVcf, chrom)
        
        #execute beagle
        cmd = "java -Djava.io.tmpdir="+pool.outputDir+" -jar -Xmx30g " + Program.config.getPath("beagle")  + " like=" + beagleFile.fileName + " out=" + pool.outputDir + "out"
        self.execute(cmd, "beagle", beagleFile)
        
        #update status of beagle file
        beagleFile.setFile(beagleFile.pool.outputDir + "out." + os.path.basename(beagleFile.fileName))
        beagleFile.beageleInput = False
        self._convertToVcf(beagleFile, chrom, origVcf)
        
    def _createBeagleInput(self, vcf, chromosome):
        """The method createBeagleInput prepares the vcf file of a pool for using this vcf file with beagle.
        :param vcf: The vcf file where to execute beagle on
        :type vcf: an instance of a :py:class:`Vcf.Vcf` object
        :param chromosome: The chromosome which to create the beagle input from
        :type chromosome: str
        
        :returns: The created beagle file as an instance of the :py:class:`BeagleFile.BeagleFile` object
        
        """  
              
        beagleFile = self.pool.addBeagleFile(chromosome)
        outputPrefix = beagleFile.getPreferredFileName()
        
        #build the command
        cmd = Program.config.getPath("vcftools") 
        if vcf.bcf == True:
            SnvCaller(self.pool,chromosome)._convertToVcf(vcf)
        cmd = cmd + " --vcf " + vcf.getFile() 
        cmd = cmd + " --out " + outputPrefix + " --chr " + beagleFile.chrom + " --BEAGLE-PL"
        
        self.execute(cmd, "vcftools", vcf)
        beagleFile.setFile(outputPrefix + ".BEAGLE.PL")
        return beagleFile
        
    
    def _convertToVcf(self, beagleFile, chrom, origVcf):
        """The method convertToVcf converts the beagle output to a phased vcf file.
        
        """
        vcfFile = VcfFile.VcfFile(origVcf.pool, origVcf.pool.outputDir + chrom + "_" + os.path.basename(origVcf.fileName), chrom=chrom)
        cmd = ("java -jar -Xmx30g " + Program.config.getPath("gatk") + 
            " -R " + Program.config.getPath("refGenome") + 
            " -T BeagleOutputToVCF" +
            " -V " + origVcf.fileName +
            " -beagleR2:BEAGLE " + beagleFile.rTwoFile +
            " -beaglePhased:BEAGLE " + beagleFile.getFile("phased") +
            " -beagleProbs:BEAGLE " + beagleFile.getFile("gprobs") +
            " -o " + vcfFile.fileName +
            " --unsafe LENIENT_VCF_PROCESSING -l DEBUG")
        self.execute(cmd, "gatk", vcfFile)
        beagleFile.pool.vcf[chrom] = vcfFile
        vcfFile.phased = True
        return vcfFile
    
def executeBeagleMultiThread(pool):  
    Grid.useGrid=False
    if None in pool.vcf:
        beagle = Haplotyper(pool, None)
        beagle.start()
        beagle.join()
        return
    
    threads = []
    for chrom in Tools.getChromosomes(Program.config.getPath("refGenome")):
        beagle = Haplotyper(pool, chrom)
        beagle.start()
        threads.append(beagle)
   
    #wait till jobs are finished
    for thread in threads:
        thread.join()

def executeBeagleCluster(pool):
    Grid.useGrid=True
    beagleCommands = {}
    
    #Fill the job files
    for chrom in Tools.getChromosomes(Program.config.getPath("refGenome")):
        beagleCommands[chrom] = Haplotyper(pool, chrom)
        beagleCommands[chrom].callHaplotypes()
    
    #Get all jobs
    jobs = []
    for vcf in pool.vcf.values():
        jobs.append(vcf.gridJob)
    
    #submit jobs to grid
    grid = Grid.Grid() 
    grid.submitJobs(jobs)  