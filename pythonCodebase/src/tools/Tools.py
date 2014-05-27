import csv, os, subprocess
def getChromosomes(refGenome):
    """The method getChromosomes retrieves the chromosomes of a reference file
    :param refGenome: path to the reference genome where to retrieve the reference sequences from
    :type refGenome: str
    
    """
    refIndex = refGenome + ".fai"
    if os.path.exists(refIndex) == False:
        exitStatus = subprocess.call("samtools faidx " + refIndex)
        if exitStatus == 1:
            print("ERROR: Failed to create a fai index file for the reference genome, do I have permissions to write in the directory of the reference genome?")
            exit(1)
    chromosomes = []
    with open(refIndex) as indexFile:
        indexReader = csv.reader(indexFile, delimiter="\t")
        for line in indexReader:
            chromosomes.append(line[0])
    return chromosomes

def getChromosomeOfFile(refGenome, fileName):
    chroms = getChromosomes(refGenome)
    for chrom in chroms:
        if chrom in fileName:
            return chrom
    return None