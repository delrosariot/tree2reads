import sys
#Takes a bed file and returns its length.
#Supports multiple regions
def bedLength(bedFile):
    length = 0
    regionFile = open(bedFile, 'r')
    for line in regionFile:
        columns = line.split()
        length += (int(columns[2]) - int(columns[1]))
    regionFile.close()
    print(length)
    
bedLength(sys.argv[1])
        