from model.cluster import Grid
from programs import Haplotyper
import Readers, logging, traceback


class AllelicDiversity():
    """The class AllelicDiversity includes all methods and variables needed for calculation of the allelic diversity.
    
    """
    def __init__(self, pool,gffFile):
        """The constructor sets the given variables as instance variables
        
        :param pool: The pool to calculate the allelic diversity for
        :type pool: an instance of a :py:class`Pool.Pool` object
        :param gffFile: The path to the gff file
        :type gffFile: str. - path to the gffFile
        """
        self.gffFile = gffFile
        self.pool = pool
    #"C:/Users/Jetse/data/test/testPhenotyper/geneModelChr12.gff3", vcfFile = "C:/Users/Jetse/data/test/testPhenotyper/fictiveSNPs.vcf"

    def _getAllHaplotypesByAccession(self, contigs):
        """The method getAllHaplotypesByAccession retrieves creates a dictionary with the accession as key and the haplotype as value
        
        :param contigs: The contigs to get the haplotypes from
        :type contigs: an list of :py:class:`Contig.Contig` instances
        
        """
        allHaplotypes = {}
        for key in contigs:
            haplotypes = {}
            if len(self.allContigs[key].snps) > 0:
                for haplotype,accessions in self.allContigs[key].haplotypes.items():
                    for accession in accessions:
                        if accession in haplotypes:
                            haplotypes[accession].append(haplotype)   
                        else:
                            haplotypes[accession] = [haplotype]
                allHaplotypes[key] = haplotypes
                
        return allHaplotypes
    
    def _parseFiles(self, chrom):
        """The method parseFiles creates the reader objects to parse all files.
        
        :param chrom: The chromosome to parse
        :type chrom: str
        """
        gffReader = Readers.GffReader(chrom=chrom)
        gffReader.readFile(self.gffFile)
        self.allContigs = gffReader.contigs
        vcfReader = Readers.VcfReader(self.allContigs.values())
        vcfReader.readFile(self.vcfFile)
        
    def getAllelicDiversity(self):
        """The method getAllelicDiversity calculates the allelic diversity and writes the output to a file.
        
        """
        if Grid.useGrid == True:
            Haplotyper.executeBeagleCluster(self.pool)
        else:
            Haplotyper.executeBeagleMultiThread(self.pool)
        
        for vcf in self.pool.vcf: 
            logging.info("calculating allelic diversity of " + vcf)
            try:
                outputFile = self.pool.outputDir + "/"+vcf + "_" + "allelicDiversity.csv"  
                self.vcfFile = self.pool.vcf[vcf].getFile()
                self._parseFiles(vcf)
                haplotypes = self._getAllHaplotypesByAccession(self.allContigs)
                accessions = haplotypes.values()[0].keys()
                
                with open(outputFile, "w") as outWriter:
                    outWriter.write("contig\toriginal\t")
                    for accession in accessions: outWriter.write( accession + "_1\t" + accession + "_2\t")
                    outWriter.write("\n")
                    for contigId in self.allContigs:
                        outWriter.write(contigId + "\t")
                        try:
                            outWriter.write(self.allContigs[contigId].refHaplotype + "\t")
                        except AttributeError: outWriter.write("-\t")
                        for accession in accessions:
                            for i in range(2):
                                if contigId in haplotypes:
                                    outWriter.write(haplotypes[contigId][accession][i] + "\t")
                                else:
                                    outWriter.write("-\t")
                        outWriter.write("\n")
            except IndexError:
                logging.warning("No SNPs within contigs found of " + vcf)
            
            except Exception as ex:
                logging.error("an error occured during parsing " + vcf)
                logging.error(ex)
                traceback.print_exc()
                exit()
                