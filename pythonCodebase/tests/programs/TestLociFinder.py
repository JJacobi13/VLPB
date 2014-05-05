'''
Created on Sep 4, 2013

@author: Jetse
'''
import sys, unittest, os, shutil, traceback
sys.path.append("../../src")
from model import Pool, VcfFile
from programs import Program
from programs.phenotyper import LociFinder


class TestLociFinder(unittest.TestCase):

    unPhasedVcf = "../testFiles/input/testFiltered.vcf"
    phasedVcf= "../testFiles/input/testPhased.vcf"
    gffFile = "../testFiles/input/chr12Accession.gff"
    
    
    def setUp(self):
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestLociFinder.testPool = Pool.Pool("testPool", "../testFiles/output/")
        TestLociFinder.testPool.vcf["SL2.40ch11_22900-24100"] = VcfFile.VcfFile(TestLociFinder.testPool, TestLociFinder.phasedVcf, bcf = False, filtered = True, phased=True)
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        TestLociFinder.lociFinder = LociFinder.LociFinder()

    def testLociFinder(self):
        TestLociFinder.lociFinder.findLoci(TestLociFinder.testPool)


if __name__ == "__main__":
    unittest.main()