import sys
#Takes a FASTA reference file and looks for its index
#in the same directory to determine its length. 
def fastaLength(fastaFile):
    length = 0
    fastaIndexFile = fastaFile + '.fai'
    regionFile = open(fastaIndexFile, 'r')
    for line in regionFile:
        columns = line.split()
        length += columns[1]
    regionFile.close()
    print(length)
    
fastaLength(sys.argv[1])
        