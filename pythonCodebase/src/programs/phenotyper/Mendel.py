from collections import Counter

class Mendel(object):
    """The Mendel class does all difficult calculations to calculate the phenotype of the haplotype.
    
    """
    
    def calculatePhenotypeChances(self, phenotype):
        """The method calculatePhenotypeChances constructs an dictionary with dictionaries.
        The key of the first dictionary is a haplotype, the value is a dictionary with all chances on an allele.
        In this second dictionary the key is the allele and the value is the chance on this allele.
        
        """
        contigsWithSnps = []
        hapChancesPerContig = {}
        for contig in phenotype.contigs:
            if len(contig.snps) == 0:
                continue
            contigsWithSnps.append(contig)
            haplotypes = contig.haplotypes
            hapToAllele = self.getHaplotypeToAlleleConversionDict(haplotypes, phenotype) 
            hapChances = {}
            for haplotype in hapToAllele:
                if self.isNumeric(phenotype.alleles.values()):
                    hapChances[haplotype] = self._calculateAverageHaplotype(hapToAllele[haplotype])
                else:
                    hapChances[haplotype] = self._calculateChances(hapToAllele[haplotype])
            hapChancesPerContig[contig] = hapChances
        return hapChancesPerContig
          
         
           
    def getHaplotypeToAlleleConversionDict(self, haplotypes, phenotype):  
        haplotypeToAllele = {}
        for haplotype in haplotypes:
            for accession in haplotypes[haplotype]:
                if haplotype in haplotypeToAllele:
                    haplotypeToAllele[haplotype].append(phenotype.alleles[accession])
                else:
                    haplotypeToAllele[haplotype] = [phenotype.alleles[accession]]
        return haplotypeToAllele
               
    
    def _calculateAverageHaplotype(self, values):
        return sum(map(float, values)) / float(len(values))
        
    def _calculateChances(self, alleles):
        """The method _calculateChances calculates the chance on a allele of a given set of phenotypes
        
        """
        counts = Counter(alleles)
  
        chances= {}
        for allele in counts:
            chances[allele] = float(counts[allele]) / float(sum(counts.values()))
        return chances
            
    def isNumeric(self, array):
        try:
            int(array[0])
            return True
        except ValueError:
            try: 
                float(array[0])
                return True
            except ValueError:
                return False
    
        