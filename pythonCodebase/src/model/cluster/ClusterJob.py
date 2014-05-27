from subprocess import Popen, PIPE
import re, logging, time, os

class ClusterJob():
    """The clusterJob tracks all executed commands, which can be executed on the Cluster. These jobs can also be executed when a single job has failed (on cluster or locally)
    
    """
    def __init__(self, jobFile):
        """The constructor creates the job file
        
        :param jobFile: The path to the file this clusterjob has to write its commands to.
        :type jobFile: str. - path to the file
        """
        self.jobFile = jobFile
        with open(self.jobFile, "w") as jobWriter:
            jobWriter.write("#!/bin/bash" + "\n")
        self.maxMemNeeded = 0 #in GB
        self.maxVMNeeded = "41g"
        self.noOfCommands = 0
        
    def addCommand(self, command):
        """This method is always called when a program is executed. It adds the command to the job file
        
        :param command: the command to add to the shell file
        """
        self.noOfCommands = self.noOfCommands+1
        with open(self.jobFile, "a") as jobWriter:
            jobWriter.write(command + "\n")
    
    def getNode(self):
        """The method getNode checks on which node this job is beeing executed.
        
        """
        try:
            output,error = Popen("qstat | grep "+self.jobId, shell=True, stdout=PIPE, stderr=PIPE).communicate()
            if self.jobId in output:
                return output.split("\t")[7]
            if len(error) > 0:
                logging.error(error)
        except ValueError:
            logging.info("Error: waiting for not submitted job...")
        
    def submit(self, nodeName=None):
        """The method submit submits a job, submits to a specific node if given.
        
        :param nodeName: The node to submit to, None if just submitted to the grid.
        :type nodeName: str.
        """
        command = "qsub -l mem_free=" + self.maxVMNeeded + ",h_vmem="+ self.maxVMNeeded +" -e " + os.path.abspath(self.jobFile) + ".err -o " + os.path.abspath(self.jobFile) + ".out " + os.path.abspath(self.jobFile)
        if nodeName != None:
            command = "qsub -q all.q@" + nodeName + ".local -l mem_free=" + self.maxVMNeeded + ",h_vmem="+ self.maxVMNeeded +" -e " + os.path.abspath(self.jobFile) + ".err -o " + os.path.abspath(self.jobFile) + ".out " + os.path.abspath(self.jobFile)
        output,error = Popen(command, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        try:
            self.jobId = re.search("Your job (\d+) \(",output).groups()[0]
        except:
            pass
        if len(error) > 0:
            logging.error("command: " + command + " failed")
            logging.error(error)
    
    def isFinished(self):
        """The method isFinished checks whether this job is running in the queue. If not in the queue, returns True.
        
        :raises ValueError: when this job has no ID, so never is submitted...
        """
        try:
            output = Popen("qstat | grep "+self.jobId, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
            if self.jobId in output:
                if output.split()[4] == "Eqw":
                    #If the job fails, print a warning, and wait a minute so the user can check why the job fails,
                    #before resubmitting the job.
                    logging.warning("job " + output.split()[2] + " failed to run, resubmitting in one minute")
                    time.sleep(60)
                    output = Popen("qdel "+self.jobId, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
                    self.submit()
                return False
            else:
                logging.info("job with ID: " + self.jobId + " is finished.")
                return True
                
        except ValueError:
            logging.info("Error: waiting for not submitted job...")
    
    def waitfor(self):
        """The method waitfor waits till this job is finished.
        
        """
        finished = False
        while finished == False:
                time.sleep(5)
                finished = self.isFinished()
    
    def __str__(self):
        return "ClusterJob[Filename: " +self.jobFile+ "]"
    def __repr__(self):
        return self.__str__()
    
clusterJobs = {}            
def getClusterJob(pool, sample=None, chrom=None):     
    """Method for getting only a single clusterjob per sample and per chromosome. when sample and chrom are none, 
    a single threaded snv calling/haplotyping will be done...
    
    """   
    if sample != None:
        if sample not in clusterJobs:
            clusterJobs[sample] = ClusterJob(sample.outputDir + sample.libName + "Job.sh")
        return clusterJobs[sample]
    elif chrom != None:
        if chrom not in clusterJobs:
            clusterJobs[chrom] = ClusterJob(pool.outputDir + chrom +"_" + pool.poolName + "Job.sh")
        return clusterJobs[chrom]
    clusterJobs[pool] = ClusterJob(pool.outputDir + pool.poolName + "Job.sh")
    return clusterJobs[pool]
    
    
    
    
    