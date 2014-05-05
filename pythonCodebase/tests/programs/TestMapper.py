import unittest,shutil, os, sys
sys.path.append("../../src")
from programs import Mapper, Program
from model import Sample, Pool

class TestMapper(unittest.TestCase):

    hqFqFile = "../testFiles/input/test_0Hq.fq"
    revHqFqFile = "../testFiles/input/test_1Hq.fq"
    
    gzFile = "../testFiles/input/test.fq.gz"
    refGzFile = "../testFiles/input/revTest.fq.gz"
    
    expOutFile = "../testFiles/output/testPool/testLib/testLib.sam"
        
    def setUp(self):
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestMapper.testPool = Pool.Pool("testPool", "../testFiles/output/")
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        TestMapper.sample = Sample.Sample(TestMapper.testPool, "testLib")
        TestMapper.testPool.addSample(TestMapper.sample)
        TestMapper.mapper = Mapper.Mapper()

    def testMap(self):
        expPairedEndOutFile = os.path.abspath(TestMapper.expOutFile)
        expPairedEndOutFileSize = 375422
        TestMapper.sample.setForwardFq(TestMapper.gzFile)
        TestMapper.sample.setReversedFq(TestMapper.refGzFile)
        TestMapper.sample.reversedFq.forward = False
        TestMapper.mapper.map(TestMapper.sample)
        self.assertEqual(os.path.abspath(TestMapper.sample.bam.fileName), expPairedEndOutFile, os.path.abspath(TestMapper.sample.bam.fileName) + " not is " +  expPairedEndOutFile)
        self.assertEqual(expPairedEndOutFileSize, os.path.getsize(TestMapper.sample.bam.fileName), "filesize: " +  str(os.path.getsize(TestMapper.sample.bam.fileName)) + " is not " + str(expPairedEndOutFileSize))
        
    def testBwaSingle(self):
        #Test single when high quality fq file is given
        TestMapper.sample.setForwardFq(TestMapper.hqFqFile)
        TestMapper.sample.reversedFq = None
         
        TestMapper.mapper._executeBwa(TestMapper.sample.forwardFq)
        self.assertEqual(os.path.abspath(TestMapper.sample.bam.fileName), os.path.abspath(TestMapper.sample.bam.fileName), "with high quality reads: " + os.path.abspath(TestMapper.sample.bam.fileName) + " not is " +  os.path.abspath(TestMapper.sample.bam.fileName))
        self.assertEqual(183089, os.path.getsize(TestMapper.sample.bam.fileName), "filesize with high quality reads: " +  str(os.path.getsize(TestMapper.sample.bam.fileName)) + " is not 183089")
  
    def testBwaPaired(self):
        expPairedEndOutFile = os.path.abspath(TestMapper.expOutFile)
        expPairedEndOutFileSize = 375422
          
        TestMapper.sample.setForwardFq(TestMapper.hqFqFile)
        TestMapper.sample.setReversedFq(TestMapper.revHqFqFile)
        TestMapper.sample.reversedFq.forward = False
        TestMapper.mapper._executeBwa(TestMapper.sample.forwardFq, TestMapper.sample.reversedFq)
        self.assertEqual(os.path.abspath(TestMapper.sample.bam.fileName),expPairedEndOutFile , os.path.abspath(TestMapper.sample.bam.fileName) + " not is " +  expPairedEndOutFile)
        self.assertEqual(expPairedEndOutFileSize, os.path.getsize(TestMapper.sample.bam.fileName), "filesize: " +  str(os.path.getsize(TestMapper.sample.bam.fileName)) + " is not " + str(expPairedEndOutFileSize))
       
        
if __name__ == '__main__':        
    unittest.main()

