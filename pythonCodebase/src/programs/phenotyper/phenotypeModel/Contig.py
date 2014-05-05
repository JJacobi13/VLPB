import Snp


class Contig(object):
    """The Contig object represents a contig
    
    """

    def __init__(self, ID, phenotype):
        """The constructor of the contig sets the given parameters as instance variables and creates an empty list of SNPs.
        
        """
        self.ID = ID
        self.phenotype = phenotype
        self.snps = []
        self.ploidy = 2
        
    def addInfo(self, chrom, start, end):
        """The method addInfo is called when reading the vcf file so all information about this contig is known.
        On creation, only the phenotype and ID are known.
        
        """
        self.chrom = chrom
        self.start = start
        self.end = end
        
    def addSnp(self, vcfLine, header):
        """The method addSnp creates a Snp object and adds this object to the list of SNPs.
        
        """
        try:
            snp = Snp.Snp(vcfLine, header, self)
            self.snps.append(snp)
        except ValueError:
            pass
        
        
    def constructHaplotypes(self):
        """The method constructHaplotypes creates an haplotype string representation of all SNPs in all strands.
        
        """
        self.haplotypes = {}
        if len(self.snps) == 0:
            return
        accessions = dict.fromkeys(self.snps[0].alleles.keys())
        
        for accession in accessions.keys():
            for i in range(self.ploidy):
                self.constructHaplotype(accession, i)
        
        self.refHaplotype = ""
        for snp in self.snps:
            self.refHaplotype = self.refHaplotype + snp.ref
           
    def constructHaplotype(self, accession, n):
        """The method constructHaplotype creates an haplotype string representation of all SNPs and their given strand of a given accession.
        :param accession: The accession where to calculate the haplotype string representation from
        :type accession: str
        :param n: The strand
        :type n: int
        """
        haplotypeString = ""
        for snp in self.snps:
            haplotypeString = haplotypeString + snp.alleles[accession][n]
        if haplotypeString in self.haplotypes:
            self.haplotypes[haplotypeString].append(accession)
        else:
            self.haplotypes[haplotypeString] = [accession]
            
    def __str__(self):
        return "Contig[ID: " + self.ID + ", chrom: " + getattr(self, 'chrom', "none") + ", start: " + str(getattr(self, 'start', -1)) + ", end: " + str(getattr(self, 'end', -1)) + ", snps: " + str(len(self.snps)) + "]"
    def __repr__(self):
        return self.__str__()