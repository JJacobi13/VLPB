
class Snp(object):
    """The Snp object represents a SNP. 
    
    """


    def __init__(self, vcfLine, vcfHeader, contig):
        """The constructor calls a method to parse the line of the vcf file, also the contig is set as an instance variable
        
        """
        self.parseVcfLine(vcfLine, vcfHeader)
        self.contig = contig
        
    def parseVcfLine(self, vcfLine, vcfHeader): 
        """The method parseVcfLine parses one line of a vcf file.
        The position, reference base, alternative base and quality are set as instance variables (all read from the given line).
        This method also calls a method to parse the alleles of this line
        :param vcfLine: the line from the vcf file
        :type vcfLine: a list of elements from the vcf file
        :param vcfHeader: the headerline which contains the accessions
        :type vcfHeader: a list of names indicating whats in the vcfLine 
        
        """
        self.pos = vcfLine[1]
        self.ref = vcfLine[3]
        self.alt = vcfLine[4]
        self.qual = vcfLine[5]
        self.parseAccessionAlleles(vcfLine[9:], vcfHeader[9:])
        
    def parseAccessionAlleles(self, vcfAccessionLines, accNames):
        """The method parseAccessionAlleles parses the alleles of each accession from a given list of alleles per allele
        :param vcfAccessionLines: all lines which contain the information of an accession.
        :type vcfAccessionLines: a list of accession information
        :param accNames: the names of the accessions
        :type accNames: a list
        
        """
        self.alleles = {}
        for i in range(len(vcfAccessionLines)):
            vcfAcc = vcfAccessionLines[i]
            if int(vcfAcc[0]) == 0:
                forward = self.ref
            else:
                forward = self.alt
                
            if int(vcfAcc[2]) == 0:
                rev = self.ref
            else:
                rev = self.alt
            haplotypes = [forward,rev]
            self.alleles[accNames[i]] = haplotypes
                
            
            
    def __str__(self):
        return "Snp[pos: " + self.pos + ", ref: " + self.ref + ", alt: " + self.alt + "]"
    def __repr__(self):
        return self.__str__()  
            
        
        