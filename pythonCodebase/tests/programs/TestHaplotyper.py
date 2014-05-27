import unittest, shutil, os, sys 
sys.path.append("../../src")
from programs import Haplotyper, Program
from model import Pool, VcfFile, Sample, BamFile
from model.cluster import Grid

class TestHaplotyper(unittest.TestCase):

    inputVcf = "../testFiles/input/testFiltered.vcf"
    chrIndex = "SL2.40ch11_22900-24100"
    
    inputBam = "../testFiles/input/test.bam"

    def setUp(self):
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
            
        TestHaplotyper.testPool = Pool.Pool("testPool", "../testFiles/output/")
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        TestHaplotyper.testPool.vcf[TestHaplotyper.chrIndex] = VcfFile.VcfFile(TestHaplotyper.testPool, TestHaplotyper.inputVcf, bcf=False, chrom=TestHaplotyper.chrIndex)
        TestHaplotyper.haplotyper = Haplotyper.Haplotyper(TestHaplotyper.testPool, TestHaplotyper.chrIndex)

    def testCreateBeagleInput(self):
        Grid.useGrid=False
        expOutFile = "../testFiles/output/testPool/testPoolSL2.40ch11_22900-24100.BEAGLE.PL"
        expSize = 185
        beagleOut = TestHaplotyper.haplotyper._createBeagleInput(TestHaplotyper.testPool.vcf[TestHaplotyper.chrIndex], TestHaplotyper.chrIndex)
        self.assertEqual(os.path.abspath(beagleOut.fileName),os.path.abspath(expOutFile) , os.path.abspath(beagleOut.fileName) + " not is " +  os.path.abspath(expOutFile))
        self.assertEqual(expSize, os.path.getsize(expOutFile), "filesize: " +  str(os.path.getsize(expOutFile)) + " is not " + str(expSize))
             
    def testExecuteBeagleMultiThread(self):
        expOutFile = "../testFiles/output/testPool/SL2.40ch11_22900-24100_testFiltered.vcf"
        Haplotyper.executeBeagleMultiThread(TestHaplotyper.testPool)
        createdOutFile = TestHaplotyper.testPool.vcf[TestHaplotyper.chrIndex].fileName
        self.assertEqual(os.path.abspath(createdOutFile),os.path.abspath(expOutFile) , os.path.abspath(createdOutFile) + " not is " +  os.path.abspath(expOutFile))
        self.checkNoOfSnps(expOutFile)
               
    def testExecuteBeagle(self):
        Grid.useGrid=False
        expOutFile = "../testFiles/output/testPool/out.testPoolSL2.40ch11_22900-24100.BEAGLE.PL.phased.gz"
        TestHaplotyper.haplotyper._executeBeagle(TestHaplotyper.testPool, TestHaplotyper.chrIndex)
        createdOutFile = TestHaplotyper.testPool.beagleFiles.values()[0].phasedFile
        self.assertEqual(os.path.abspath(createdOutFile),os.path.abspath(expOutFile) , os.path.abspath(createdOutFile) + " not is " +  os.path.abspath(expOutFile))
        self.checkNoOfSnps(expOutFile)
    
    def checkNoOfSnps(self, outputFile):
        noOfSnps = 0
        with open(outputFile, 'r') as inReader:
            for line in inReader:
                if line.startswith("#"):
                    continue
                else:
                    noOfSnps += 1
        self.assertEqual(noOfSnps,1, "number of snps: " +  str(noOfSnps) + " is not " + str(1))
             
    def testExecuteBeagleGrid(self):
        expOutFile = "../testFiles/output/testPool/SL2.40ch11_22900-24100_testFiltered.vcf"
        Haplotyper.executeBeagleCluster(TestHaplotyper.testPool)
        createdOutFile = TestHaplotyper.testPool.vcf[TestHaplotyper.chrIndex].fileName
        self.assertEqual(os.path.abspath(createdOutFile),os.path.abspath(expOutFile) , os.path.abspath(createdOutFile) + " not is " +  os.path.abspath(expOutFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(expOutFile)
     
    def testHaplotyperPath(self):
        Grid.useGrid=False
        expOutFile = "../testFiles/output/testPool/out.testPoolSL2.40ch11_22900-24100.BEAGLE.PL.phased.gz"
          
        TestHaplotyper.testPool.vcf ={}
        TestHaplotyper.sample = Sample.Sample(TestHaplotyper.testPool, "testLib")
        TestHaplotyper.testPool.addSample(TestHaplotyper.sample)
        TestHaplotyper.sample.bam = BamFile.BamFile(TestHaplotyper.testPool, TestHaplotyper.sample, TestHaplotyper.inputBam, sortedBam = True, headerLine = True, duplicates = False, mdTag = True, index = True)
  
        TestHaplotyper.haplotyper.callHaplotypes()
        createdOutFile = TestHaplotyper.testPool.beagleFiles.values()[0].phasedFile
        self.assertEqual(os.path.abspath(createdOutFile),os.path.abspath(expOutFile) , os.path.abspath(createdOutFile) + " not is " +  os.path.abspath(expOutFile))
        self.checkNoOfSnps(expOutFile)
         
    def testHaplotyperPathGrid(self):         
        TestHaplotyper.testPool.vcf ={}
        TestHaplotyper.sample = Sample.Sample(TestHaplotyper.testPool, "testLib")
        TestHaplotyper.testPool.addSample(TestHaplotyper.sample)
        TestHaplotyper.sample.bam = BamFile.BamFile(TestHaplotyper.testPool, TestHaplotyper.sample, TestHaplotyper.inputBam, sortedBam = True, headerLine = True, duplicates = False, mdTag = True, index = True)
 
        Haplotyper.executeBeagleCluster(TestHaplotyper.testPool)
#         self.assertEqual(os.path.abspath(createdOutFile),os.path.abspath(expOutFile) , os.path.abspath(createdOutFile) + " not is " +  os.path.abspath(expOutFile))
        self.checkNoOfSnps("../testFiles/output/testPool/SL2.40ch11_22900-24100_testPool_SL2.40ch11_22900-24100.vcf")


    def testHaplotyperFullPathGrid(self):
        expOutFile = "../testFiles/output/testPool/SL2.40ch11_22900-24100_testPool_SL2.40ch11_22900-24100.vcf"
        gzFile = "../testFiles/input/test.fq.gz"
        refGzFile = "../testFiles/input/revTest.fq.gz"
        TestHaplotyper.testPool.vcf ={}
        TestHaplotyper.sample = Sample.Sample(TestHaplotyper.testPool, "testLib")
        TestHaplotyper.testPool.addSample(TestHaplotyper.sample)
        TestHaplotyper.sample.setForwardFq(gzFile)
        TestHaplotyper.sample.setReversedFq(refGzFile)
        TestHaplotyper.sample.reversedFq.forward = False
        
        Haplotyper.executeBeagleCluster(TestHaplotyper.testPool)
#         createdOutFile = TestHaplotyper.testPool.vcf[TestHaplotyper.chrIndex].fileName
#         self.assertEqual(os.path.abspath(createdOutFile),os.path.abspath(expOutFile) , os.path.abspath(createdOutFile) + " not is " +  os.path.abspath(expOutFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(expOutFile)
        
        
        
if __name__ == '__main__':        
    unittest.main()