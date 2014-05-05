from subprocess import Popen, PIPE
from VlpbConfig import Configuration
import logging
from model.cluster import Grid

class Program(object):
    """The Program is a class which represents an executable program.

    """

    def execute(self, command, programName, analyzerFile):
        """This method executes the command created by its children
        
        :param command: The command to execute
        :type command: str.
        :param programName: The name of the program to execute
        :type programName: str
        :param file: the file this commands is executed on, #TODO create per file object a check if the output is valid
        :type file: an instance of a :py:class:`File.File` object
        
        """
        if Grid.useGrid == True:
            analyzerFile.gridJob.addCommand(command)
            return
        logging.info("starting " + programName)
        logging.debug("command: " + command)

       
        error,output = Popen(command, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        if(len(output) > 0):
            logging.info(output)
        if(len(error) > 0):
            logging.info(error)
        self.checkOutput(output)
        self.checkOutput(error)
        logging.info("finished " + programName)

    def checkOutput(self, outputString):
        if "[bam_plp_destroy] memory leak" in outputString:
            logging.error(outputString)
            logging.error("Error: Sort the bamfile first!")
        elif "The GATK no longer supports SAM files without read groups" in outputString:
            logging.error(outputString)
            logging.error("Error: Add read groups before executing GATK!")
        elif "Invalid command line" in outputString:
            logging.error(outputString)
            logging.error("Error: an invalid commandline was entered, look log file for details")
        elif "Key AF found in VariantContext field INFO" in outputString:
            logging.error(outputString)
            logging.error("Error: Use the --unsafe LENIENT_VCF_PROCESSING for gatk and it works...")
        elif "Segmentation fault" in outputString:
            logging.error(outputString)
            logging.error("Error: Samtools failed, probably error in reference index....")    
        elif "ERROR" in outputString.upper():
            logging.error(outputString)
            logging.error("An error occured:\n" + outputString)
        elif "WARNING" in outputString.upper():
            logging.warning(outputString)
            logging.error("A warning occured:\n" + outputString)
    
    def getProgramArguments(self, programName):
        """The method getProgramArguments asks the configuration object for all arguments and parses these to one space separated string.
        When the program needs the arguments in a different way, this method can be overrided.
        
        :param programName: The name of the program where to retrieve the options from
        :type programName: str.
        :returns: The program arguments as a <space> separated string.
        
        """
        args = config.getProgramOptions(programName)
        argsCmd = " "
        for arg in args:
            argsCmd = argsCmd + arg + " "
            if args[arg]:
                argsCmd = argsCmd + args[arg] + " "
        return argsCmd

config = Configuration.Config() 
