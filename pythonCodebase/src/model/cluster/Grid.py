'''
Created on Sep 2, 2013

@author: Jetse
'''
import time, Node, logging

useGrid = False

class Grid(object):
    """The Grid object regulates all communication with the SGE.
    
    """
    
    nodes = {}
    
    def __init__(self):
        """The constructor of the grid object creates Node objects for all nodes used for this pipeline. TODO: read nodes from config file.
        
        """
        self.waitingJobs = []
        self.runningJobs = []
        
#         if len(Grid.nodes) == 0:
#             #convert node names to node objects
#             logging.info("checking nodes...")
#             for node in ["compute-0-1", "compute-0-10", "compute-0-11", "compute-0-13", "compute-0-19", "compute-0-2", "compute-0-20", "compute-0-21", "compute-0-22", "compute-0-23", "compute-0-3", "compute-0-6", "compute-0-7"]:  
#                 Grid.nodes[node] = Node.Node(node)
#             logging.info("checked nodes...")
        
    def submitJobs(self, jobs, specificNode=False):
        """The method submitJobs adds all given jobs to the waiting queue and calls the manageJobs function.
        
        :param jobs: The jobs to add to the queue
        :type jobs: List of :py:class:`ClusterJob`
        :param specificNode: When submitting the jobs to a specific node (mostly because of hdd mem usage)
        :type specificNode: boolean
        """
        logging.info("submitting jobs and waiting till finished...")
        self.waitingJobs.extend(jobs)
        self._manageJobs(specificNode)
        logging.info("all jobs finished!")
    
    def _submitJob(self, job, specificNode=False):
        """The method submitJob checks on which node the job can run, and runs the job on this node.
        
        :param job: The job to submit
        :type job: a :py:class:`ClusterJob` instance
        :param specificNode: When submitting the jobs to a specific node (mostly because of hdd mem usage)
        :type specificNode: boolean
        """
        if specificNode == True:
            for node in Grid.nodes.values():
                if node.getAvailableMem() > job.maxMemNeeded and node.getFreeProcs() > 0:
                    job.submit(node.nodeName)
                    job.node = node
                    node.addJob(job)
                    break
        else:
            job.submit()
        self.waitingJobs.remove(job)
        self.runningJobs.append(job)
        
    def _manageJobs(self, specificNode = False):
        """The method manageJobs runs all jobs on the grid, and checks whether a job is finished when a job is finished, a new job can be submitted till all jobs are finished.
        
        :param specificNode: When submitting the jobs to a specific node (mostly because of hdd mem usage)
        :type specificNode: boolean
        """
        while len(self.waitingJobs)>0 or len(self.runningJobs)>0:
            #Resubmit waiting jobs
            for job in self.waitingJobs:
                self._submitJob(job, specificNode)
                
            #Check whether jobs are finished
            for job in self.runningJobs:
                if job.isFinished():
                    if specificNode == True:
                        job.node.removeJob(job)
                    self.runningJobs.remove(job)

            time.sleep(5)
