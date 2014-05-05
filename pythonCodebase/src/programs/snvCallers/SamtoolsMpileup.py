import os
from model import VcfFile
from model.cluster import Grid
from programs import Program
from tools import Tools
from SnvCaller import SnvCaller

class SamtoolsMpileup(SnvCaller):
    
              
    def callSnvs(self):
        """The method samtoolsMpileup calls the single nucleotide variations of a pool with samtools mpileup.
        
        :param pool: the pool to call all SNVs from
        :type pool: an instance of a :py:class:`Pool.Pool` object
        :raises: LookupError if the pool has no samples to execute samtools on
        """
        if len(self.pool.samples) == 0:
                raise LookupError("no samples for executing samtools")
            
        if self.chromosome not in self.pool.vcf:
            self.pool.vcf[self.chromosome] = VcfFile.VcfFile(self.pool, chrom=self.chromosome, bcf=True)
            inputFileString = ""
            for sample in self.pool.samples:
                inputFileString = inputFileString + " " + sample.bam.getFile()
                
            outputFile = self.pool.vcf[self.chromosome].fileName
            
            cmd = Program.config.getPath("samtools") + " mpileup " + self.getProgramArguments("samtools mpileup")
            if self.chromosome !=None:
                cmd = cmd + " -r " + self.chromosome
            cmd = cmd + " -gf " + os.path.abspath(Program.config.getPath("refGenome")) + inputFileString + " > " + outputFile
    
            self.execute(cmd, "samtools mpileup", self.pool.vcf[self.chromosome])
            
        self._filterVcf(self.pool.vcf[self.chromosome])
        
    def _filterVcf(self, vcfFile):
        """The method filterVcf removes the insignificant SNVs from the vcf file.
        
        :param vcfFile: The vcf file which has to be filtered, when it is bcf, it first will be converted to vcf.
        :type vcfFile: an instance of a :py:class:`VcfFile.VcfFile` object
        
        """
        if vcfFile.filtered == True:
            return
        self._convertToVcf(vcfFile)
        
        outputFile = vcfFile.getNewFileName()
        cmd = "perl " + Program.config.getPath("vcfutils") + " varFilter " + self.getProgramArguments("vcfutils varFilter") + " " + vcfFile.getFile() + " > " + outputFile
        self.execute(cmd,"vcfutils varFilter", vcfFile)
        vcfFile.filtered = True
        vcfFile.setFile(outputFile)
        
def executeSamtoolsMultiThreaded(pool):
    Grid.useGrid=False
    threads = []
    for chrom in Tools.getChromosomes(Program.config.getPath("refGenome")):
        samtools = SamtoolsMpileup(pool, chrom)
        samtools.start()
        threads.append(samtools)
    
    #wait till jobs are finished
    for thread in threads:
        thread.join()
        
def executeSamtoolsCluster(pool):
    Grid.useGrid=True
    samtoolsCommands = {}
    jobs = []
    #Fill the job files
    for chrom in Tools.getChromosomes(Program.config.getPath("refGenome")):
        samtoolsCommands[chrom] = SamtoolsMpileup(pool, chrom)
        samtoolsCommands[chrom].callSnvs()
    
    #Get all jobs    
    for vcf in pool.vcf.values():
        jobs.append(vcf.gridJob)
    
    #submit jobs to grid
    grid = Grid.Grid() 
    grid.submitJobs(jobs)
        
        
        
        