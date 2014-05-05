'''
Created on Sep 12, 2013

@author: Jetse
'''

import sys, unittest, os, shutil, logging
sys.path.append("../../src")
from model import Pool, VcfFile
from programs import Program
from programs.phenotyper import LociFinder


class LociTester(unittest.TestCase):

    unPhasedVcf = "../testFiles/input/testFiltered.vcf"
    phasedVcf= "../testFiles/input/phenoTest.vcf"
    Program.config.gffFile = "../testFiles/input/chr12Accession.gff"
    csvFile = "../testFiles/input/phenotypeData.csv"
    
    
    def setUp(self):
        for handler in logging.getLogger().handlers:
            handler.close()
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        LociTester.testPool = Pool.Pool("testPool", "../testFiles/output/")
        LociTester.testPool.vcf["SL2.40ch11_22900-24100"] = VcfFile.VcfFile(LociTester.testPool, LociTester.phasedVcf, bcf = False, filtered = True, phased=True)
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        Program.config.phenoData = LociTester.csvFile
        LociTester.lociFinder = LociFinder.LociFinder()

    def testConvertExcelToCsv(self):
        xlsFile = "../testFiles/input/phenotypeData.xls"
        expCsvFile = "../testFiles/output/testPool/phenotypeData.csv"
        convertedCsv = LociTester.lociFinder.convertExcelToCsv(xlsFile, LociTester.testPool.outputDir)
        self.assertEqual(os.path.abspath(expCsvFile),os.path.abspath(convertedCsv) , os.path.abspath(convertedCsv) + " not is " +  os.path.abspath(expCsvFile))
        self.assertEqual(os.path.getsize(expCsvFile), os.path.getsize(LociTester.csvFile), "filesize: " +  str(os.path.getsize(expCsvFile)) + " is not " + str(os.path.getsize(LociTester.csvFile)))
    
    def testFindLoci(self):
        expCsvFile = "../testFiles/output/testPool/Brix_SL2.40ch11_22900-24100_pvals.csv"
        LociTester.lociFinder.findLoci(LociTester.testPool)
        print "output file:"
        with open(expCsvFile) as inReader:
            for line in inReader:
                print line.strip()
        
if __name__ == "__main__":
    unittest.main()