import unittest, sys,os,shutil,logging
sys.path.append("../../src")
from programs import Program
from programs.snvCallers import SamtoolsMpileup, Gatk, SnvCaller
from model import Pool, Sample, BamFile
from model.cluster import Grid

class TestSnvCaller(unittest.TestCase):
    inputBam = "../testFiles/input/test.bam"
    
    expVcfFile = "../testFiles/output/testPool/testPool.vcf"
    expBcfFile = "../testFiles/output/testPool/testPool.bcf"
        
    def setUp(self):
        for handler in logging.getLogger().handlers:
            handler.close()
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestSnvCaller.testPool = Pool.Pool("testPool", "../testFiles/output/")
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        TestSnvCaller.sample = Sample.Sample(TestSnvCaller.testPool, "testLib")
        TestSnvCaller.testPool.addSample(TestSnvCaller.sample)
        TestSnvCaller.sample.bam = BamFile.BamFile(TestSnvCaller.testPool, TestSnvCaller.sample, TestSnvCaller.inputBam, sortedBam = True, headerLine = True, duplicates = False, mdTag = True, index = True)
     
    def checkNoOfSnps(self, outputFile):
        noOfSnps = 0
        with open(outputFile, 'r') as inReader:
            for line in inReader:
                if line.startswith("#"):
                    continue
                else:
                    noOfSnps += 1
        self.assertEqual(noOfSnps,1, "number of snps: " +  str(noOfSnps) + " is not " + str(1))
 
    def testSamtoolsMpileupSingleThread(self):
        Grid.useGrid = False
        SamtoolsMpileup.SamtoolsMpileup(TestSnvCaller.testPool).callSnvs()
        outputFile = TestSnvCaller.testPool.vcf[None].fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(TestSnvCaller.expVcfFile)
          
    def testSamtoolsMpileupMultiThread(self):
        expOutFile = "../testFiles/output/testPool/testPool_SL2.40ch11_22900-24100.vcf"
        SamtoolsMpileup.executeSamtoolsMultiThreaded(TestSnvCaller.testPool)
        outputFile = TestSnvCaller.testPool.vcf["SL2.40ch11_22900-24100"].fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(expOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(expOutFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(expOutFile)
              
    def testSamtoolsPath(self):
        SnvCaller.converting = "not done"
        gzFile = "../testFiles/input/test.fq.gz"
        refGzFile = "../testFiles/input/revTest.fq.gz"
        TestSnvCaller.sample.bam =None
        TestSnvCaller.sample.setForwardFq(gzFile)
        TestSnvCaller.sample.setReversedFq(refGzFile)
        TestSnvCaller.sample.reversedFq.forward = False
        samt = SamtoolsMpileup.SamtoolsMpileup(TestSnvCaller.testPool)
        samt.callSnvs()
        outputFile = TestSnvCaller.testPool.vcf[None].fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(TestSnvCaller.expVcfFile)
           
    def testSamtoolsMultiple(self):
        #add an extra sample to the pool
        TestSnvCaller.sample2 = Sample.Sample(TestSnvCaller.testPool, "testLib2")
        TestSnvCaller.sample2.bam = BamFile.BamFile(TestSnvCaller.testPool, TestSnvCaller.sample2, TestSnvCaller.inputBam)
        TestSnvCaller.testPool.addSample(TestSnvCaller.sample2)
              
        #Execute and check execution output
        SamtoolsMpileup.SamtoolsMpileup(TestSnvCaller.testPool).callSnvs()
        outputFile = TestSnvCaller.testPool.vcf[None].fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(TestSnvCaller.expVcfFile)
      
    def testGatk(self):
        Gatk.Gatk(TestSnvCaller.testPool).callSnvs()
        outputFile = TestSnvCaller.testPool.vcf[None].fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(TestSnvCaller.expVcfFile)
         
    def testGatkPath(self):
        SnvCaller.converting = "not done"
        gzFile = "../testFiles/input/test.fq.gz"
        refGzFile = "../testFiles/input/revTest.fq.gz"
        TestSnvCaller.sample.bam =None
        TestSnvCaller.sample.setForwardFq(gzFile)
        TestSnvCaller.sample.setReversedFq(refGzFile)
        TestSnvCaller.sample.reversedFq.forward = False
        gatk = Gatk.Gatk(TestSnvCaller.testPool)
        gatk.callSnvs()
        outputFile = TestSnvCaller.testPool.vcf[None].fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        #Check if the file contains exactly one snp
        self.checkNoOfSnps(TestSnvCaller.expVcfFile)

#     def testSamtoolsGrid(self):
#         expOutFile = "../testFiles/output/testPool/testPool_SL2.40ch11_22900-24100.vcf"
#         SamtoolsMpileup.executeSamtoolsCluster(TestSnvCaller.testPool)
#         outputFile = TestSnvCaller.testPool.vcf["SL2.40ch11_22900-24100"].fileName
#         self.assertEqual(os.path.abspath(outputFile),os.path.abspath(expOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(expOutFile))
#         #Check if the file contains exactly one snp
#         self.checkNoOfSnps(expOutFile)
    
if __name__ == '__main__':        
    unittest.main()
