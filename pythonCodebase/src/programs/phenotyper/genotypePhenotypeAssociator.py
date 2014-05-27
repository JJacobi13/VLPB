import Readers, Mendel

phenotypeFile = "C:/Users/Jetse/data/test/testPhenotyper/phenotypeFictive.txt"
lociFile = "C:/Users/Jetse/data/test/testPhenotyper/lociFictive.txt"
gffFile = "C:/Users/Jetse/data/test/testPhenotyper/geneModelChr12.gff3"
vcfFile = "C:/Users/Jetse/data/test/testPhenotyper/fictiveSNPs.vcf"

lociReader = Readers.LociReader()
lociReader.readFile(lociFile)
phenotypes = lociReader.phenotypes

gffReader = Readers.GffReader(phenotypes)
gffReader.readFile(gffFile)
contigs = gffReader.contigs

vcfReader = Readers.VcfReader(contigs.values())
vcfReader.readFile(vcfFile)

phenotypeReader = Readers.PhenotypeReader(phenotypes)
phenotypeReader.readFile(phenotypeFile)

phenotyper = Mendel.Mendel()
# for descr in phenotypes:
descr = "BricksValue"
chancesPerContig = phenotyper.calculatePhenotypeChances(phenotypes[descr])

print(chancesPerContig)
