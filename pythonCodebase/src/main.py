import argparse, os
from model import Sample, Pool, FastqFile, BamFile, VcfFile
from programs import Haplotyper, Mapper, Program
from programs.snvCallers import SamtoolsMpileup, Gatk
from model.cluster import Grid
from programs.phenotyper import AllelicDiversity, LociFinder
from tools import Tools
class VLPBcli(object):
    """The VLPBcli represents the commandline interface of the VLPB project. This class regulates the input parameters and gives the command to execute a program.
    
    """
    
    def main(self):
        """The main is the main of the program, this main parses the arguments, and gives the command to execute a program
        
        """
        argParser = argparse.ArgumentParser(description='Finding some phenotypes of your data...')
        
        argParser.add_argument('inputDirectory', help="The directory where you hid your fastq files in", action="store")
        argParser.add_argument('outputDirectory', help="The directory where to write all mess to", action="store")
        argParser.add_argument("--name", required=True, type=str, help="The name of the pool")
        argParser.add_argument("--mapper", choices=["BWA"], default="BWA")
        argParser.add_argument("--snvCaller", choices=["samtools", "GATK"], default="samtools")
        argParser.add_argument("--inFormat", choices=["fq", "bam","vcf"], default="fq")
        argParser.add_argument("--end", choices=["mapping","snvCalling", "haplotyping","phenotyping","allelicDiversity","findLoci"], default="phenotyping")
        argParser.add_argument("--gff", required=False, type=argparse.FileType())
        argParser.add_argument("--phen", required=False, type=argparse.FileType())
        argParser.add_argument("--bed", required=False, type=argparse.FileType())
        argParser.add_argument("--grid", required=False,action="store_true")
        argParser.add_argument("--multiThread", required=False,action="store_true")
        
        args= argParser.parse_args()

        self.pool = Pool.Pool(args.name, args.outputDirectory)
        
        self.findFastqFiles(args.inputDirectory, args.inFormat)
        
        self.parseOptionalArguments(args)
        
        self.execute(args.end)
        
    def parseOptionalArguments(self, args):
        """The method parseOptionalArguments forwards optional arguments to the configuration object of the program module.
        :param args: the parsed commandline arguments
        :type args: an :py:class:`argparse.Namespace` instance
        
        """
        Program.config.mapper = args.mapper
        Program.config.snvCaller = args.snvCaller
        if args.gff:
            args.gff.close()
            Program.config.gffFile = args.gff.name
        else:
            Program.config.gffFile = None
            
        if args.phen:
            args.phen.close()
            Program.config.phenoData = args.phen.name
        else:
            Program.config.phenoData = None
        if args.grid == True:
            Grid.useGrid = True
        if args.multiThread == True:
            Program.config.multiThread = True
        if args.bed:
            args.bed.close()
            Program.config.bedFile = args.bed.name
        
    def execute(self, executable):
        """The method execute checks which program has to be executed and executes this program
        :param executable: the argument of the commandline which determines which program has to be executed
        :type executable: str
        """
        if executable == "phenotyping":
            print("pheno!")
        elif executable == "haplotyping":
            if Grid.useGrid == True:
                Haplotyper.executeBeagleCluster(self.pool)
            else:
                Haplotyper.executeBeagleMultiThread(self.pool)
        elif executable == "snvCalling":
            if Program.config.snvCaller == "samtools":  # @UndefinedVariable
                SamtoolsMpileup.executeSamtoolsMultiThreaded(self.pool)
            elif Program.config.snvCaller == "GATK":  # @UndefinedVariable
                Gatk.Gatk(self.pool).callSnvs()
        elif executable == "mapping":
            mapper = Mapper.Mapper()
            for sample in self.samples:
                mapper.map(sample)
        elif executable == "allelicDiversity":
            if Program.config.gffFile == None:  # @UndefinedVariable
                print("When calculating the allelic diversity, a gff file is needed, this option can be set with the option --gff <file>")
                exit()
            allelicDiverityCalculator = AllelicDiversity.AllelicDiversity(self.pool, Program.config.gffFile)  # @UndefinedVariable
            allelicDiverityCalculator.getAllelicDiversity()
        elif executable == "findLoci":
            if Program.config.phenoData == None:  # @UndefinedVariable
                print("When finding loci, a gff file is needed, this option can be set with the option --phen <file>")
                exit()
            if Program.config.gffFile == None:  # @UndefinedVariable
                print("When finding loci, a file with phenotype data is needed, this option can be set with the option --gff <file>")
                exit()
            lociFinder = LociFinder.LociFinder()
            lociFinder.findLoci(self.pool)
            
    def getChromosomeFromVcf(self, fileName):
        """The method getChromosomeFromVcf checks a vcf file on which chromosome it contains. 
        When multiple chromosomes are in the file, only the first on will be returned.
        :param fileName: the name of the vcf file
        :type fileName: str.
        
        """
        with open(fileName, 'r') as vcfReader:
            for line in vcfReader:
                if line.startswith("#"):
                    continue
                return line.split("\t")[0]

    def findFastqFiles(self, directory, inFormat):
        """The method findFastqFiles finds all fastq files recursively in a directory, from each directory with fastq files a sample is created.
        :param directory: the directory where the user hid his fastq files
        :type directory: str -- path to the directory
        
        """
        fastqFiles = []
        self.samples = []
        for fileName in os.listdir(directory):
            fileName = directory + "/" + fileName
            if os.path.isdir(fileName):
                self.findFastqFiles(fileName, inFormat)
            else:
                if inFormat == "bam":
                    if fileName.endswith(".bam") or fileName.endswith(".bam.gz"):
                        newSamp = Sample.Sample(self.pool, os.path.basename(os.path.splitext(fileName)[0]))
                        self.samples.append(newSamp)
                        newSamp.bam = BamFile.BamFile(self.pool, newSamp, fileName, sortedBam = True, headerLine = True, duplicates = False, mdTag = True, index = True)
                        self.pool.addSample(newSamp)
                elif inFormat == "fq":
                    if fileName.endswith(".fq") or fileName.endswith(".fq.gz"):
                        fastqFiles.append(fileName)
                elif inFormat == "vcf":
                    if fileName.endswith(".vcf") or fileName.endswith(".vcf.gz"):
                        chrom = self.getChromosomeFromVcf(fileName)
                        self.pool.vcf[chrom] = VcfFile.VcfFile(self.pool, fileName, bcf=False, filtered=True, phased=True, chrom=chrom)
                    elif fileName.endswith(".bcf") or fileName.endswith(".bcf.gz"):
                        chrom = Tools.getChromosomeOfFile(Program.config.getPath("refGenome"), fileName)
                        self.pool.vcf[chrom] = VcfFile.VcfFile(self.pool, fileName, bcf=True, filtered=True, phased=True, chrom=chrom)
                        
        if inFormat == "bam" or inFormat =="vcf":
            return
        if len(fastqFiles) > 0:
            #create a library name from the file name
            libName = os.path.basename(fastqFiles[0])
            if libName.endswith("_1.fq") or libName.endswith("_2.fq"):
                libName = libName[:-5]
            if libName.endswith("_1.fq.gz") or libName.endswith("_2.fq.gz"):
                libName = libName[:-8]
            else:
                libName = libName[:-3]
                
            #create the sample
            sample = Sample.Sample(self.pool, libName)
            self.samples.append(sample)
            
            #add the fastq files to the sample
            if len(fastqFiles) == 1:
                sample.setForwardFq(fastqFiles[0])
            elif len(fastqFiles == 2):
                sample.setReversedFq(fastqFiles[1])
            elif len(fastqFiles > 2):
                if fastqFiles[0].endswith("_1.fq"):
                    suffix = "_1.fq"
                elif fastqFiles[0].endswith("_1.fq.gz"):
                    suffix = "_1.fq.gz"
                else:
                    print("WARNING: files do not end with _1.fq or _1.fq.gz or _2.fq or _2.fq.gz, using all files in one directory as 1 sample with only forward reads")
                    suffix = fastqFiles[0][-3:]
                #create a list of forward fastq files and one of reversed fastq files
                forward = []
                reversedFastq = []
                for fastqFile in fastqFiles:
                    if fastqFile.endswith(suffix):
                        forward.append(fastqFile)
                    else:
                        reversedFastq.append(fastqFile)
                        
                #Convert files to fastqFile objects
                for i in range(len(forward)):
                    forward[i] = FastqFile.FastqFile(self.pool, sample, forward[i])
                for i in range(len(reversedFastq)):
                    reversedFastq[i] = FastqFile.FastqFile(self.pool, sample, reversedFastq[i], forward=False)
                    
                #add the fastq files to the sample
                sample.forwardFq = forward
                sample.reversedFq = reversedFastq
 
if __name__ == '__main__':        
    VLPBcli().main()           


