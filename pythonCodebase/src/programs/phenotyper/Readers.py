from phenotypeModel import Phenotype, Contig
import re, logging, os
"""The module Readers contains all readers for reading tab delimited files of the phenotyping program.

"""

class Reader(object):
    """The reader is an abstract class for reading tab delimited files.
    
    """
    
    def readFile(self, inFile):
        """The method readFile reads a tab delimited file. Lines starting with a '#' are skipped.
        When de line starts with #CHROM this will be the header information of the vcf file.
        Every other line will execute the method _parseLine in the child objects, is required!
        Afterwards the method actionAfterReading in the child objects will be called, is optional
        :param inFile: The file to read
        :type inFile: str -- path to the file
        
        """
        self.header = None
        noOfParsedLines = 0
        with open(inFile) as infile:
                for line in infile:
                    if line.startswith("#"):
                        if line.startswith("#CHROM"):
                            self.header = line[1:].split()     #remove the '#' so line[1:] instead of line
                        else:
                            continue
                    if noOfParsedLines % 100000 == 0:
                        if noOfParsedLines == 0:
                            logging.info("starting to parse " + os.path.basename(inFile))
                        else: logging.info("parsed " + str(noOfParsedLines) + " lines.")
                    noOfParsedLines = noOfParsedLines +1
                    self._parseLine(line.split("\t"))
        self._actionAfterReading()
        
    def _parseLine(self, info, header):
        """The method _parseLine parses the line of a tab separated file.
        This is different in all files so has to be implemented in the child objects
        :param info: The splitted line of a tab separated file
        :type info: list
        :param header: The vcf header, other headers may be implemented later on
        :type header: str
        """
        raise NotImplementedError("implement _parseLine in all subclasses")
    
    def _actionAfterReading(self):
        """If there has an action to be executed always after reading a file, this method can be implemented.
        
        """
        pass
        
class PhenotypeReader(Reader):
    """The method PhenotypeReader reads a phenotype file.
    The phenotype file is a tab separated file, the header line indicates the accessions.
    All other lines indicate the alleles of a phenotype of an accession.
    File format:
    +-----------+---------+---------+---------+
    |description|accession|accession|accession|
    +-----------+---------+---------+---------+
    |phenotype  |allele   |allele   |allele   |
    +-----------+---------+---------+---------+
    
    """
    
    def __init__(self):
        """The constructor of the PhenotypeReader sets the given phenotypes as instance variable
        :param phenotypes: an dictionary phenotype objects where to add the alleles to
        :type phenotypes: an dictionary of :py:class:`Phenotype.Phenotype` objects with the description as key
        
        """
        self.phenotypes = []
    
    def _parseLine(self, info):
        """Implementation of the super method (where the args are explained).
        If the line is the first line, the accessions will be saved as an instance variable.
        Else the alleles will be added to the phenotype object
        
        """
        if self.header == None:
            self.header = info
            for item in info[1:]:
                self.phenotypes.append(Phenotype.Phenotype(item.strip()))
            return
        
        accession = info.pop(0)

        for i in range(len(info)):
            self.phenotypes[i].alleles[accession] = info[i].rstrip()
     
    def genoIDToAccession(self, genoID):
        pass

class VcfReader(Reader):
    """The VcfReader reads a vcf file.
    
    """
    
    def __init__(self, contigs):
        """The constructor sets the given contigs as an instance variable
        :param contigs: a list of Contig objects to check whether the SNPs are in one of used contigs
        :type contigs: a list of :py:class:`Contig.Contig` instances
        """
        self.contigs = contigs[:]
        self.contigs.sort(key = lambda x: int(x.end))
                
    def _parseLine(self, info):
        """Implementation of the super method (where the args are explained).
        this method checks whether the SNP is in a contig, if this one is in a contig, the snp will be added to the contig, else do nothing...
        
        """
        try:
            pos = int(info[1])
        except ValueError: return
        except IndexError:
            if "".join(info).strip() != "":
                logging.warning("skipping line in vcf file:")
                logging.warning(info)
            return
        
        for contig in self.contigs:
            
            if pos > int(contig.start) and pos < int(contig.end):
                contig.addSnp(info, self.header)
              
    def _actionAfterReading(self):
        """Implementation of the super method.
        After reading the file, the haplotypes have to be calculated for each contig.
        
        """
        for contig in self.contigs:
            contig.constructHaplotypes()
        
            
class LociReader(Reader):
    """The LociReader reads a file with all candidate genes of a phenotype.
    This file consists of 2 columns, the first column describes the phenotype, the second column describes the contig ID
    All phenotypes and contigs can occur multiple times!
    Format:
    +----------------+
    |phenotype|contig|
    +---------+------+
    |phenotype|contig|
    +---------+------+
    """
    
    def __init__(self):
        """The constructor of the LociReader creates an empty dictionary to save all contigs per phenotype in.
        
        """
        self.phenotypes = {}
        
    def _parseLine(self, info):
        """Implementation of the super method (where the args are explained).
        This method parses a line of a loci file, this method fills the phenotype dictionary with contigs which are involved in a phenotype.
        
        """
        if info[0] in self.phenotypes:
            self.phenotypes[info[0]].addContig(info[1])
        else:
            self.phenotypes[info[0]] = Phenotype.Phenotype(info[0],info[1])
            
        
            
class GffReader(Reader):
    """The GffReader reads a GFF3 file.
    
    """
    
    idRegex = re.compile("Name=([^;]*)")
    
    def __init__(self, phenotypes=None, chrom=None):
        """The constructor reads of all phenotypes all contigs, and converts this to one dictionary with contig objects with the contig ID as key.
        if the phenotypes == None, an empty dictionary is created and all contigs will be added to this dictionary.
        
        """
        self.phenotypes = phenotypes
        self.chrom = chrom
        self.contigs = {}
        if phenotypes != None:
            for phenotype in phenotypes.values():
                for contig in phenotype.contigs:
                    self.contigs[contig.ID] = contig
        
    def _parseLine(self, info):
        """Implementation of the super method (where the args are explained).
        If the contig ID is in the dictionary of contigs, information is added to this contig.
        If there is no phenotype, all contigs are added to the dictionary of contigs.
        
        """
        try:
            contigId = GffReader.idRegex.search(info[8]).group(1)
        except AttributeError:
            return
        if self.phenotypes != None:
            if contigId in self.contigs.keys():
                self.contigs[contigId].addInfo(info[0],info[3],info[4])
              
        elif info[2] == "gene":
            if self.chrom == None or self.chrom == info[0]:
                self.contigs[contigId] = Contig.Contig(contigId, None)
                self.contigs[contigId].addInfo(info[0],info[3],info[4])

class AccessionConverter(Reader):
    
    def __init__(self):
        self.EusolToAccession = {}
    
    def _parseLine(self, info):
        for item in info[2].split(","):
            self.EusolToAccession[item] = info[0].rstrip()
        
        
    def getAccession(self, eusolID):
        """
        Getter for retrieving the accession of an eusol ID.
        
        :param eusolID: The ID of eusol
        :type eusolID: str.
        :returns: the accession of an eusol ID
        :raises: KeyError when there is no accession ID for this eusol ID.
        
        """
        return self.EusolToAccession[eusolID]
 

    