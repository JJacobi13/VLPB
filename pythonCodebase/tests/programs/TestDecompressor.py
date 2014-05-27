import unittest, sys, os, shutil
sys.path.append("../../src")
from model import Pool, Sample
from programs import Decompressor

class TestDecompressor(unittest.TestCase):
    
    outFileSize = 156850
    forwardOut = "../testFiles/output/testPool/testLib/test.fq"
    revOut = "../testFiles/output/testPool/testLib/revTest.fq"
    fqFile = "../testFiles/input/test.fq"
    gzFile = "../testFiles/input/test.fq.gz"
    refGzFile = "../testFiles/input/revTest.fq.gz"
    tarGzFile = "../testFiles/input/test.tar.gz"
    
    def setUp(self):
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestDecompressor.testPool = Pool.Pool("testPool", "../testFiles/output/")
        TestDecompressor.sample = Sample.Sample(TestDecompressor.testPool, "testLib")
        TestDecompressor.testPool.addSample(TestDecompressor.sample)
        TestDecompressor.sample.setForwardFq(TestDecompressor.gzFile)
        TestDecompressor.sample.setReversedFq(TestDecompressor.refGzFile)
        TestDecompressor.decompressor = Decompressor.Decompressor()

    def testGz(self):
        TestDecompressor.sample.setForwardFq(TestDecompressor.gzFile)
        outputFile = TestDecompressor.decompressor._extractGz(TestDecompressor.sample.forwardFq, TestDecompressor.sample.outputDir)
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestDecompressor.forwardOut), os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestDecompressor.forwardOut))
        self.assertEqual(TestDecompressor.outFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(TestDecompressor.outFileSize))
        
        TestDecompressor.sample.setForwardFq(TestDecompressor.gzFile)
        outputFile = TestDecompressor.decompressor._extractGz(TestDecompressor.sample.reversedFq, TestDecompressor.sample.outputDir)
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestDecompressor.revOut), os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestDecompressor.revOut))
        self.assertEqual(TestDecompressor.outFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(TestDecompressor.outFileSize))
        
    
    def testTarGz(self):
        TestDecompressor.sample.setForwardFq(TestDecompressor.tarGzFile)
        outputFile = TestDecompressor.decompressor._extractTarGz(TestDecompressor.sample.forwardFq, TestDecompressor.sample.outputDir)
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestDecompressor.forwardOut), os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestDecompressor.forwardOut))
        self.assertEqual(TestDecompressor.outFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(TestDecompressor.outFileSize))

    def testExtract(self):
        #test tar.gz
        TestDecompressor.sample.setForwardFq(TestDecompressor.tarGzFile)
        outputFile = TestDecompressor.decompressor.extract(TestDecompressor.sample.forwardFq)
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestDecompressor.forwardOut), os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestDecompressor.forwardOut))
        self.assertEqual(TestDecompressor.outFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(TestDecompressor.outFileSize))
        
        #test .gz
        TestDecompressor.sample.setForwardFq(TestDecompressor.gzFile)
        outputFile = TestDecompressor.decompressor.extract(TestDecompressor.sample.forwardFq)
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestDecompressor.forwardOut), os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestDecompressor.forwardOut))
        self.assertEqual(TestDecompressor.outFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(TestDecompressor.outFileSize))
        
        #test exception
        TestDecompressor.sample.setForwardFq("somerandomFileName.foo")
        self.assertRaises(TypeError, TestDecompressor.decompressor.extract,TestDecompressor.sample.forwardFq)

if __name__ == '__main__':        
    unittest.main()
