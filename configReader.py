import sys
#Gets the path where genreads.py is located
def neatPathGetter(configFile):
    config = open(configFile, 'r')
    path = ""
    for line in config:
        if line[0] != "#":
            columns = line.split()
            path = columns[2].replace('"', '')
    genreadsLocation = path + "/genReads.py"
    config.close()
    print(genreadsLocation)
    
neatPathGetter(sys.argv[1])