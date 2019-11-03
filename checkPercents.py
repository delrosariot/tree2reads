import sys
#Checks if the percent file provided by the user is valid
def checkPercents(percentFile):
    total = 0
    file = open(percentFile, 'r')
    for line in file:
        words = line.split()
        total += float(words[1])
    file.close()
    if total != 1:
        print("The percents do not add up to 1! Check your percents file")
        return exit(1)
        
checkPercents(sys.argv[1])