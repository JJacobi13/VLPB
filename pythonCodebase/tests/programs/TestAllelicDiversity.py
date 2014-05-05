'''
Created on Jul 16, 2013

@author: Jetse
'''

import sys, unittest, os, shutil
sys.path.append("../../src")
from model import Pool, VcfFile
from programs import Program
from programs.phenotyper import AllelicDiversity


class TestAllelicDiversity(unittest.TestCase):

    unPhasedVcf = "../testFiles/input/testFiltered.vcf"
    phasedVcf= "../testFiles/input/testPhased.vcf"
    gffFile = "../testFiles/input/chr12Accession.gff"
    
    
    def setUp(self):
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestAllelicDiversity.testPool = Pool.Pool("testPool", "../testFiles/output/")
        TestAllelicDiversity.testPool.vcf["SL2.40ch11_22900-24100"] = VcfFile.VcfFile(TestAllelicDiversity.testPool, TestAllelicDiversity.phasedVcf, bcf = False, filtered = True, phased=True)
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        TestAllelicDiversity.aDCalculator = AllelicDiversity.AllelicDiversity(TestAllelicDiversity.testPool, TestAllelicDiversity.gffFile)

#     def testGetAllelicDiversity(self):
#         expSize = 202
#         expOutFile = "../testFiles/output/testPool/SL2.40ch11_22900-24100_allelicDiversity.csv"
#         TestAllelicDiversity.aDCalculator.getAllelicDiversity()
#         self.assertEqual(expSize, os.path.getsize(expOutFile), "filesize: " +  str(os.path.getsize(expOutFile)) + " is not " + str(expSize))
        
    def testAllelicDiversityPath(self):
        expSize = 167
        TestAllelicDiversity.testPool.vcf["SL2.40ch11_22900-24100"] = VcfFile.VcfFile(TestAllelicDiversity.testPool, TestAllelicDiversity.unPhasedVcf, bcf = False, filtered = True, phased=False)
        expOutFile = "../testFiles/output/testPool/SL2.40ch11_22900-24100_allelicDiversity.csv"
        TestAllelicDiversity.aDCalculator.getAllelicDiversity()
        self.assertEqual(expSize, os.path.getsize(expOutFile), "filesize: " +  str(os.path.getsize(expOutFile)) + " is not " + str(expSize))
        

        
        
        
if __name__ == "__main__":
    unittest.main()