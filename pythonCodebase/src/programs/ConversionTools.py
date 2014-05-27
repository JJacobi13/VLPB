from programs import Program, Mapper

class ConversionTools(Program.Program):
    """The class ConvertionTools regulates the support between the mappers and the programs for SV calling.
    
    """
    
    def sortBam(self, sample):
        """The method sortBam sorts a bam file of a given sample.
        The bam file can only be sorted when this is a bam file. If it is not a bam file, the file first will be converted to a bam file.
        
        :param sample: The sample which contains the bam file to be sorted
        :type sample: an instance of a Sample object
        
        """
        if sample.bam == None or sample.bam.sam == True:
                self.convertToBam(sample) 
            
        if sample.bam.sorted == True:
            return

        outputFile = sample.bam.getNewFileName()
        cmd = Program.config.getPath("samtools") + " sort -o " + sample.bam.getFile() + " " + outputFile + " > " + outputFile
        self.execute(cmd, "samtools sort", sample.bam)
        sample.bam.sorted = True
        sample.bam.setFile(outputFile)
        
    def convertToBam(self, sample):
        """The method convertToBam converts a sam file to a bam file of a given sample, if the file is not a sam file, the file first will be mapped
        by calling the :meth:`Mapper.Mapper.map` function.
        
        :param sample: The sample which contains the sam file to be converted to a bam file
        :type sample: an instance of a Sample object
        
        """
        if sample.bam == None:
            Mapper.Mapper().map(sample)
            
        if sample.bam.sam == False:
            return

        outputFile = sample.bam.getNewFileName()
        cmd = Program.config.getPath("samtools") + " view "+ self.getProgramArguments("samtools view") + " " + sample.bam.getFile() + " > " + outputFile
        self.execute(cmd, "samtools view", sample.bam)
        sample.bam.sam = False
        sample.bam.setFile(outputFile)
        
    def createBamIndex(self, sample):
        """creates a bam index file for the bam file of a given sample.
        
        :param sample: The sample which contains the bam file to create an index for
        :type sample: an instance of a Sample object
        :raises: A typeError when the sample contains no bam file
        
        """
        if sample.bam == None:
            self.convertToBam(sample)

        if sample.bam.index == True:
            return
        cmd = Program.config.getPath("samtools") + " index " + sample.bam.getFile()
        self.execute(cmd, "samtools index", sample.bam)
        sample.bam.index = True
    
    def addHeaderLine(self, sample):
        """Adds a header line to the bam file of a given sample, if the input is not a sorted bam file, first the method :meth:`sortBam` will be executed.
        
        :param sample: The sample which contains the bam file to add the headerline to
        :type sample: an instance of a Sample object
        
        """
        if sample.bam == None or sample.bam.sam == True:
            self.convertToBam(sample)
            
        if sample.bam.headerLine == True:
            return
        
        outputFile = sample.bam.getNewFileName()
        cmd = "java -jar -Djava.io.tmpdir=" + sample.bam.pool.outputDir + " " + Program.config.getPath("picardTools") + "/AddOrReplaceReadGroups.jar I=" + sample.bam.getFile() + " VALIDATION_STRINGENCY=SILENT O=" + outputFile + " LB=" + sample.bam.sample.libName + " PL=illumina PU=lane SM="+sample.bam.sample.libName
        self.execute(cmd, "picardtools AddOrReplaceReadGroups", sample.bam)
        sample.bam.headerLine = True
        sample.bam.setFile(outputFile)
        
    def removeDuplicates(self, sample):
        """The method removeDuplicates removes all possible PCR duplicates of the bam file of a given sample. If the input file is not a sorted bam file, 
        first the method :meth:`sortBam` will be executed.
        
        :param sample: The sample which contains the bam file to remove the duplicates from
        :type sample: an instance of a Sample object
        
        """
        if sample.bam == None or sample.bam.sam == True or sample.bam.sorted == False:
                self.sortBam(sample)
            
        if sample.bam.duplicates == False:
            return
        
        outputFile = sample.bam.getNewFileName()
        cmd = "java -jar -Djava.io.tmpdir=" + sample.bam.pool.outputDir + " " + Program.config.getPath("picardTools") + "/MarkDuplicates.jar INPUT=" + sample.bam.getFile() + " VALIDATION_STRINGENCY=SILENT OUTPUT=" + outputFile + " REMOVE_DUPLICATES=true METRICS_FILE=/dev/null"
        self.execute(cmd, "picardtools MarkDuplicates", sample.bam)
        sample.bam.duplicates = False
        sample.bam.setFile(outputFile)
    
    def addMdTag(self, sample):
        """The method addMdTag adds a md tag to the bam file of a given sample. If the file is not a bam file without duplicates, first the bam file will be converted to bam
        
        :param sample: The sample which contains the bam file to add the md tags to
        :type sample: an instance of a Sample object
        
        """
        if sample.bam == None or sample.bam.sam == True:
                self.convertToBam(sample)
            
        if sample.bam.mdTag == True:
            return
        
        outputFile = sample.bam.getNewFileName()
        cmd = Program.config.getPath("samtools") + " calmd " + self.getProgramArguments("samtools calmd") + " " + sample.bam.getFile() + " " + Program.config.getPath("refGenome") + " > " + outputFile
        self.execute(cmd, "samtools calmd", sample.bam)
        sample.bam.mdTag = True
        sample.bam.setFile(outputFile)
        
