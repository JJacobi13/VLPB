class Logger(object):
    """The Logger regulates all writing and layout of the logfile
    
    """
    def __init__(self, logFile):
        """The constructor of the Logger opens a logfile for easy access to the logfile in this object
        
        :param logFile: The log file where to write all information to
        :type logFile: str. -- Path to the log file
        
        """
        
        self.logFile = logFile
        self.fileWriter = open(logFile, "w")
        self.fileWriter.close()
        
        
    def nextProgram(self, programName, command):
        """The method nextProgram print the next program with its command to the log file.
        
        :param programName: The name of the next program
        :type programName: str.
        :param command: The command which is executed right now
        :type command: str.
        
        """
        self.fileWriter = open(self.logFile, "a")
        self.fileWriter.write("########################################################################################################################\n")
        self.fileWriter.write("##\n")
        self.fileWriter.write("##  " + programName + "\n")
        self.fileWriter.write("##  command: " + command + "\n")
        self.fileWriter.write("##\n")
        self.fileWriter.write("########################################################################################################################\n")
        self.fileWriter.close()
    
    def logOut(self, outLines):
        """The method logOut writes the output of the programs to the log file.
        
        :param outLines: the lines which have to be written to the output file.
        :type outLines: str.
        
        """
        self.fileWriter = open(self.logFile, "a")
        self.fileWriter.writelines(outLines)
        self.fileWriter.write("\n")
        self.fileWriter.close()
        
    def logError(self, errorMessage):
        """The method logError writes errors to the log file A little ascii art is also created so the user can scan easy for errors.
        This error is only printed if the message is not empty!
        
        :param errorMessage: the error message which has to be printed.
        :type errorMessage: str.
        
        """
        if errorMessage:
            self.fileWriter = open(self.logFile, "a")
            self.fileWriter.write("##  Error\n")
            self.fileWriter.write("####################\n")
            self.fileWriter.write(errorMessage + "\n")
            print "ERROR: " + errorMessage
            self.fileWriter.close()