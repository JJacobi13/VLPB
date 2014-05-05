import Contig
class Phenotype(object):
    """An instance of the Phenotype object represents one single Phenotype.
    
    """
    def __init__(self, description):
        """The constructor of the phenotype object sets the given description as instance variable, creates a list of contigs with the given contig.
        Also an empty list of alleles is created.
        :param description: the description of this phenotype
        :type description: str
        :param contigId: the ID of the contig
        :type contigId: str
        
        """
        self.contigs = []
        self.alleles = {}
        self.description = description
        
    def addContig(self, contigId):
        """The method addContig creates a contig object and adds this object to the list of contigs involved with this phenotype.
        
        """
        self.contigs.append(Contig.Contig(contigId, self))
        
    def __str__(self):
        return "Phenotype[Description: " + self.description + ", no of contigs: " + str(len(self.contigs)) + "]"
    def __repr__(self):
        return self.__str__()