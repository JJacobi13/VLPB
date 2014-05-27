import Readers, xlrd, csv, os
from programs import Program, Haplotyper
import numpy # @UnresolvedImport
from scipy import stats  # @UnresolvedImport
import logging

class LociFinder(object):
    
    def convertExcelToCsv(self, xlsFile, outputDir):
        if xlsFile.endswith(".xls") == False and xlsFile.endswith(".xlsx") == False:
            return xlsFile
        newFileName = outputDir + "/" + os.path.splitext(os.path.basename(xlsFile))[0] + ".csv"
        with xlrd.open_workbook(xlsFile) as wb:
            with open(newFileName,"w") as outFile:
                sheet = wb.sheet_by_index(0)
                csvWriter = csv.writer(outFile, csv.excel_tab)
                for row in range(sheet.nrows):
                    csvWriter.writerow(sheet.row_values(row)) 
                
        return newFileName
    
    def findLoci(self, pool):
        #read the input files
        Haplotyper.executeBeagleMultiThread(pool)
        
        phenReader = Readers.PhenotypeReader()
        Program.config.phenoData = self.convertExcelToCsv(Program.config.phenoData, pool.outputDir)
        phenReader.readFile(Program.config.phenoData)
        converter = Readers.AccessionConverter()
        converter.readFile(os.path.dirname(os.path.realpath(__file__)) + "/convertToAccession.txt")
        for phenotype in  phenReader.phenotypes:
            deletedKeys = 0
#             for oldKey in phenotype.alleles.keys():
#                 try:
#                     newKey = converter.getAccession(oldKey)
#                     phenotype.alleles[newKey] = phenotype.alleles.pop(oldKey)
#                 except KeyError:
#                     deletedKeys += 1
#                     del phenotype.alleles[oldKey]
            for (chrom, vcfFile) in pool.vcf.items():
                gffReader = Readers.GffReader(chrom=chrom)
                gffReader.readFile(Program.config.gffFile)  # @UndefinedVariable
                phenotype.contigs = gffReader.contigs 
                
                vcfReader = Readers.VcfReader(phenotype.contigs.values())
                vcfReader.readFile(vcfFile.getFile())
                
                pVals = self.findLociInPheno(phenotype)
                self.writePvaluesToFile(pVals, chrom, pool, phenotype.description)
    
    def writePvaluesToFile(self, pVals, chrom, pool, descr):
        outFile = pool.outputDir + descr +"_" + chrom + "_pvals.csv"
        with open(outFile, "w") as outWriter:
            for (contig, pVal) in pVals.items():
                outWriter.write(contig + "\t" + str(pVal[1]) + "\n")
        
    def findLociInPheno(self, phenotype):
        numpy.seterr(all="raise")
        pValues = {}
        for contig in phenotype.contigs:
            if len(phenotype.contigs[contig].haplotypes) == 0:
                continue
            accessions = {}
            for accession in phenotype.alleles.keys():
                for (haplotype,contigAccessions) in phenotype.contigs[contig].haplotypes.items():
                    for contigAccession in contigAccessions:
                        if haplotype in accessions:
                            try:
                                accessions[haplotype].append(float(phenotype.alleles[accession]))
                            except:
                                pass
                        else:
                            try:
                                accessions[haplotype] = [float(phenotype.alleles[accession])]
                            except: pass
            try:
                pValues[contig] = stats.f_oneway(*accessions.values())
            except Exception as err:
                logging.error("Error in the loci calculation: " + str(err))
        return pValues
