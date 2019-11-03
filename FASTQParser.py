import random
import argparse
import os

#Selects a certain percent of the reads from a FASTQ
#file and outputs a file with these reads
def FASTQSelector(fastq, output, percent):
    fastqFile = open(fastq, 'r')
    parsedFastq = open(output, 'a')
    count = 0
    validLineCount = 10
    for line in fastqFile:
        #Makes sure to write the remaining three lines of the
        #selected line to complete the read.
        if validLineCount < 4:
            validLineCount = validLineCount + 1
            parsedFastq.write(line)
        elif count%4 == 0:
            randomValue = random.random() 
            if randomValue < percent:
                parsedFastq.write(line)
                validLineCount = 1
        count = count + 1
        
    fastqFile.close()
    parsedFastq.close()
    
#Creates a final FASTQ by going through the folder that contains the generated
#FASTQs and calculating the percent of reads needed from each one
def FASTQMerger(percents, directory, output, length, readLen, coverage):
    index = 0
    newOutput = "Final_Reads_" + output + ".fq"
    listOfPercents = readPercents(percents)
    #path = os.fsencode(directory)
    for file in os.listdir(directory):
        #filename = os.fsdecode(file)
        if file.endswith(".fq") and not file.startswith("."):
            inputFile = directory + '/' + file
            readNumber = int(numberOfReads(coverage, length, readLen))
            FASTQLength = int(countReads(inputFile))
            nodeName = file.replace('_read1.fq', '')
            tempPercent = findPercent(listOfPercents, nodeName)
            finalPercent = generatePercent(FASTQLength, readNumber, float(tempPercent))
            
            FASTQSelector(inputFile, newOutput, finalPercent)
            index += 1
            
 
#Returns the number of total reads the user will have on
#the final FASTQ           
def numberOfReads(coverage, totalength, readLength):
    readNumber = (totalength * coverage)/readLength
    return readNumber

#Returns the percent to be used by FASTQSelector    
def generatePercent(FASTQLength, readNumber, percent):
    neededReads = percent * readNumber
    finalPercent = neededReads/FASTQLength
    return finalPercent
        
#Generates a list of percent from a percents text file
def readPercents(percentFile):
    total = 0
    listOfPercents = []
    file = open(percentFile, 'r')
    for line in file:
        words = line.split()
        total += float(words[1])
        listOfPercents.append([words[0].lower(), words[1]])
    file.close()
    if total == 1:
        return listOfPercents
    else:
        print("The percents do not add up to 1!")
        exit()
#Given the name of a node, finds the matching percent on the 
#user input percents file    
def findPercent(percentsList, nodeName):
    for i in range(len(percentsList)):
        #print(percentsList[i])
        if percentsList[i][0] == nodeName.lower():
            return percentsList[i][1]

#Returns the total number of reads in a FASTQ file
def countReads(FASTQFile):
    lines = 0
    mutationReads = open(FASTQFile, 'r')
    for line in mutationReads:
        lines = lines + 1
    mutationReads.close()
    return lines//4
        
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--OUTPUT", help="Output file", metavar="OUTPUT", type=str, required=True)
    parser.add_argument("-p","--PERCENT", help="File with percent of mutations", metavar="PERCENT", type=str, required=True)
    parser.add_argument("-d","--DIRECTORY", help="Directory with reads", metavar="DIRECTORY", type=str, required=True)
    parser.add_argument("-c","--COVERAGE", help="Desired Coverage", metavar="COVERAGE", type=int, required=True)
    parser.add_argument("-l","--LENGTH", help="Length of region", metavar="LENGTH", type=int, required=True)
    parser.add_argument("-r","--READLEN", help="Length of reads", metavar="READLEN", type=int, required=True)
    
    args = parser.parse_args()
    
    percent = args.PERCENT
    output = args.OUTPUT
    directory = args.DIRECTORY
    length = args.LENGTH
    readLen = args.READLEN
    coverage = args.COVERAGE
    
    FASTQMerger(percent, directory, output, length, readLen, coverage)
    
if __name__ == "__main__":
    main()
        
