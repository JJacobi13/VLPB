'''
Created on Aug 12, 2013

@author: Jetse
'''
class Accession(object):
    """The Accession object describes a single accession with a phenotype allele and a haplotype for combining information.
    
    """
    
    def __init__(self, accessionNo, phenoAllele, haplotype):
        """The constructor of the accession object sets the given variables as instance variables
        
        :param accessionNo: The accession number
        :type accessionNo: int
        :param phenoAllele: The allele of the phenotype of this accession
        :type phenoAllele: str
        :param haplotype: The haplotype of this gene with this accession number
        :type haplotype: str
        """
        self.accessionNo = accessionNo
        self.phenoAllele = phenoAllele
        self.haplotype = haplotype
        
    def __str__(self):
        return "Accession[no: " + self.accessionNo + ", phenoAllele: " + self.phenoAllele + ", haplo: " + self.haplotype + "]"
    def __repr__(self):
        return self.__str__()