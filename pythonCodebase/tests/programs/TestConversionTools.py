import unittest, os, sys, shutil
sys.path.append("../../src")
from programs import ConversionTools, Program
from model import Pool,Sample, BamFile
from subprocess import Popen, PIPE

class TestConversionTools(unittest.TestCase):
    
    samFile = "../testFiles/input/test.sam"
    bamFile = "../testFiles/input/test.bam"
    sortedBamFile = "../testFiles/input/testSorted.bam"
    gzFile = "../testFiles/input/pairedTest.tar.gz"
    expBamOutFile= "../testFiles/output/testPool/testLib/testLib.bam"
    
    def setUp(self):
        for delFile in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", delFile)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestConversionTools.testPool = Pool.Pool("testPool", "../testFiles/output/")
        Program.config.setPath("refGenome","../testFiles/input/smallRefGenome.fa")
        TestConversionTools.sample = Sample.Sample(TestConversionTools.testPool, "testLib")
        TestConversionTools.testPool.addSample(TestConversionTools.sample)
        TestConversionTools.convTools = ConversionTools.ConversionTools()
         
        
    def testConvertToBam(self):
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.samFile, sam=True)
        self.convTools.convertToBam(TestConversionTools.sample)
        self.assertTrue(os.path.exists(TestConversionTools.expBamOutFile), "output file not created...")
        output ,error = Popen(Program.config.getPath("samtools") + " view -h " + TestConversionTools.expBamOutFile +" | wc -l", shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.assertEqual(output.rstrip(), "1282", "number of lines: " +  output.rstrip() + " is not " + str(1282))
            
    def testSortBam(self):
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.sortBam(TestConversionTools.sample)
        self.convTools.convertToBam(TestConversionTools.sample)
        self.assertTrue(os.path.exists(TestConversionTools.expBamOutFile), "output file not created...")
        output ,error = Popen(Program.config.getPath("samtools") + " view -h " + TestConversionTools.expBamOutFile +" | wc -l", shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.assertEqual(output.rstrip(), "1283", "number of lines: " +  output.rstrip() + " is not " + str(1283))
        
    def testCreateBamIndex(self):
        indexFilesize = 96
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.sortBam(TestConversionTools.sample)
        self.convTools.createBamIndex(TestConversionTools.sample)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertTrue(os.path.isfile(TestConversionTools.expBamOutFile + ".bai") , os.path.abspath(TestConversionTools.expBamOutFile + ".bai") + " is not created")
        self.assertEqual(indexFilesize, os.path.getsize(TestConversionTools.expBamOutFile + ".bai"), "filesize: " +  str(os.path.getsize(TestConversionTools.expBamOutFile + ".bai")) + " is not " + str(indexFilesize))
            
    def testAddHeaderLine(self):
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.addHeaderLine(TestConversionTools.sample)
        self.convTools.convertToBam(TestConversionTools.sample)
        self.assertTrue(os.path.exists(TestConversionTools.expBamOutFile), "output file not created...")
        output ,error = Popen(Program.config.getPath("samtools") + " view -h " + TestConversionTools.expBamOutFile +" | wc -l", shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.assertEqual(output.rstrip(), "1284", "number of lines: " +  output.rstrip() + " is not 1284")
            
    def testRemoveDuplicates(self):
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.removeDuplicates(TestConversionTools.sample)
        self.convTools.convertToBam(TestConversionTools.sample)
        self.assertTrue(os.path.exists(TestConversionTools.expBamOutFile), "output file not created...")
        output ,error = Popen(Program.config.getPath("samtools") + " view -h " + TestConversionTools.expBamOutFile +" | wc -l", shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.assertEqual(output.rstrip(), "1266", "number of lines: " +  output.rstrip() + " is not " + str(1266))
            
    def testAddMdTag(self):
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.addMdTag(TestConversionTools.sample)
        self.assertTrue(os.path.exists(TestConversionTools.expBamOutFile), "output file not created...")
        output ,error = Popen(Program.config.getPath("samtools") + " view -h " + TestConversionTools.expBamOutFile +" | wc -l", shell=True, stdout=PIPE, stderr=PIPE).communicate()
        self.assertEqual(output.rstrip(), "1283", "number of lines: " +  output.rstrip() + " is not " + str(1283))

if __name__ == '__main__':        
    unittest.main()
    
    
