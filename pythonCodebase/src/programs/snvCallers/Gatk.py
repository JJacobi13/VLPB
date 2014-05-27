'''
Created on Sep 13, 2013

@author: Jetse
'''
import os, subprocess
from programs.snvCallers import SnvCaller
from programs import Program
from model import VcfFile

class Gatk(SnvCaller.SnvCaller):
        
    def callSnvs(self):
        """The method samtoolsMpileup calls the single nucleotide variations of a pool with samtools mpileup.
        
        :param pool: the pool to call all SNVs from
        :type pool: an instance of a :py:class:`Pool.Pool` object
        :raises: LookupError if the pool has no samples to execute samtools on
        """
        if len(self.pool.samples) == 0:
                raise LookupError("no samples for executing samtools")
        
        if os.path.exists(Program.config.getPath("refGenome") + ".dict") == False:
            exitStatus = subprocess.call("java -jar CreateSequenceDictionary.jar R="+Program.config.getPath("refGenome")+" O="+Program.config.getPath("refGenome")+".dict ")
            if exitStatus == 1:
                print("ERROR: Failed to create a bwa index file for the reference genome, do I have permissions to write in the directory of the reference genome?")
                exit(1)
        
            
        if self.chromosome not in self.pool.vcf:
            self.pool.vcf[self.chromosome] = VcfFile.VcfFile(self.pool, chrom=self.chromosome, bcf=False)
            inputFileString = ""
            for sample in self.pool.samples:
                inputFileString = inputFileString + " -I " + sample.bam.getFile()
                
            outputFile = self.pool.vcf[self.chromosome].fileName
            cmd = "java -jar " + Program.config.getPath("gatk") + " -T UnifiedGenotyper -R " + os.path.abspath(Program.config.getPath("refGenome")) + inputFileString + " -o " + outputFile + " -L " + self.chromosome
            if Program.config.bedFile != None:
                cmd = cmd + " -L " + Program.config.bedFile + " -isr INTERSECTION"
            self.execute(cmd, "GATK", self.pool.vcf[self.chromosome])
