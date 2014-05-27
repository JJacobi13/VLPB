'''
Created on Jun 21, 2013

@author: Jetse
'''
import os, logging
from model import BeagleFile


def run_once(f):
    """Simple decorator method to run a function only once in the program.
    
    """
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

class Pool(object):
    """The Pool object represents a pool of samples where programs can be executed on
    
    """

    
    def __init__(self, poolName, outputDir):
        """The constructor of the Pool sets the instance variables, creates the output directory and a Logger object.
        :param poolName: The name of this pool
        :type poolName: str
        :param outputDir: The output directory of this pool, a sub directory will be created for each pool.
        :type outputDir: str -- Path to the output direcotory
        
        **Instance variables**
        * samples: an array of all :py:class:`Sample.Sample`s in this pool
        * vcf: an dictionary with the chromosome as key and a  :py:class:`VcfFile.VcfFile` as value
        * beagleOut: an :py:class:`BeagleFile.BeagleFile` of this pool, None if not created yet
        
        """
        self.samples = []
        self.vcf = {}
        self.beagleFiles = {}
        
        self.poolName = poolName
        self._outputDir = outputDir + "/" + poolName
        if not os.path.isdir(self.outputDir):
            os.makedirs(self.outputDir)
            
        self.configureLogging()
        
    @run_once
    def configureLogging(self):
        """Setting up the variables for the logging module.
        
        """
        logging.basicConfig(filename=self.outputDir + self.poolName + ".log", format="%(asctime)-22s%(levelname)-12s%(message)s", level=logging.DEBUG, datefmt="%m/%d/%Y %I:%M:%S %p")
        console=logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter("%(asctime)-15s%(levelname)-12s%(message)s", "%I:%M:%S %p"))
        logging.getLogger().addHandler(console)
    
    @property
    def outputDir(self):
        """Getter for the output directory, for always retrieving the absolute path of this directory
        
        """
        return os.path.abspath(self._outputDir) + "/"
    
    @outputDir.setter
    def outputDir(self, value):
        """Setter for the output directory, required for the getter...
        
        """
        self._outputDir = value
            
    def addSample(self, sample):
        """Method for adding a sample to the arraylist of samples
        
        """
        self.samples.append(sample)
        
    def addBeagleFile(self, chrom):
        """Method for adding a beagle file to the dictionary of beaglefiles.
        
        """
        beagleFile = BeagleFile.BeagleFile(self, chrom)
        self.beagleFiles[chrom] = beagleFile
        return beagleFile
    
