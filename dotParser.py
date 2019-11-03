import sys
import argparse
import random
import re
import os
import networkx as nx

#Parses through a graph in a dot file.
def dotParser(dotFile):
    inputFile = open(dotFile, 'r')
    insideGraph = False
    #Lists of mutations
    SetOfMutations = set([])
    OrderedMutations = []
    #Lists of mutations with their parents
    Mutations_Parents= []
       
    newGraph = nx.Graph()
    for line in inputFile:
        words = line.split()
        #If we find an undirected graph, record that in the 
        #variable 'insideGraph'
        if words[0] == 'graph':
            insideGraph = True
        #Once we reach the end of a graph, record it in the
        #variable 'insideGraph'
        elif words [0] == '}':
            insideGraph = False
        #If we are still inside the graph, parse through the
        #content, getting rid of new line characters and other 
        #not-useful stuff.
        elif insideGraph:
            parsedLine = line.replace(';','')
            parsedLine = parsedLine.replace('\n', '')
            parsedLine = parsedLine.replace(' ', '')
            currentPair = parsedLine.split('--')
            #Adds the mutations/nodes to their respective lists
            for i in range(2):
                if currentPair[i] not in SetOfMutations:
                    SetOfMutations.add(currentPair[i])
                    newGraph.add_node(currentPair[i])
           
    inputFile.close()
    #Second run through the file to add edges to the graph
    inputFileTwo = open(dotFile, 'r')
    for line in inputFileTwo:
        words = line.split()
        if words[0] == 'graph':
            insideGraph = True
        elif words [0] == '}':
            insideGraph = False
        elif insideGraph:
            parsedLine = line.replace(';','')
            parsedLine = parsedLine.replace('\n', '')
            parsedLine = parsedLine.replace(' ', '')
            currentPair = parsedLine.split('--')
            newGraph.add_edge(currentPair[1], currentPair[0])
    inputFileTwo.close()
    #Orders the graph in a breadth-first order
    Mutations_Parents = list(nx.bfs_edges(newGraph,'root'))
    OrderedMutations.append("root")
    #Adds the nodes in level-order
    for j in range(len(Mutations_Parents)):
        OrderedMutations.append(Mutations_Parents[j][1])
    return OrderedMutations, Mutations_Parents

#Method that creates the germline VCF, which is an
#ancestor of all of the remaining nodes.
def germlineCreator(germline, output):
    #os.makedirs(os.path.dirname(output), exist_ok=True)
    newGermlineVCF = open (output, 'w')
    for line in germline:
        if line[0] == '#':
            newGermlineVCF.write(line)
        else:
            columns = line.split()
            #if columns[0] == '19':
            randomPercent = random.random()
            if randomPercent <= 0.0016:
                newGermlineVCF.write(line)
    
    newGermlineVCF.close()
    
#Method that creates every somatic mutation VCF,
#both adding new mutations to the VCF and taking all
#of the mutations from the ancestral VCF.
def somaticCreator(ancestor, somatic, output):
    newSomaticVCF = open (output, 'w')
    ancestorVCF = open(ancestor, 'r')
    baseSomatic = open(somatic, 'r')
    bases = ['A', 'T', 'C', 'G']
    for line in ancestorVCF:
        newSomaticVCF.write(line)
    for line in baseSomatic:
        columns = line.split()
        #TODO this is specific for chromosome 19 at the moment
        #if columns[0] == '19' and columns [3] in bases and columns[4] in bases:
        if line[0] != "#" and columns[3] in bases and columns[4] in bases:
            randomPercent = random.random()
            if randomPercent <= 0.0038:
                newSomaticVCF.write(line)
            
    newSomaticVCF.close()
    ancestorVCF.close()
    baseSomatic.close()

#The main method that combines the previous ones together.
#It generates the correct amount of VCFs with the correct
#ancestry.
def VCFGenerator(mutations, mutationsWithParents, outputName, germline, somatic):
    germlineFile = open(germline, 'r')
    somaticFile = somatic
    #A list of the already generated VCF files for easy access
    mutationFiles = []
    #Folder for the created VCFs
    VCFFolder = 'VCFs_' + outputName
    for i in range(len(mutations)):
        nodeName = mutations[i].lower()
        if nodeName == 'root':
            output = VCFFolder + '/' + nodeName + '.vcf'
            mutationFiles.append(output)
            germlineCreator(germlineFile, output)
            germlineFile.close()
        else:
            ancestor = ''
            #Find the ancestor of the current node
            for sublist in mutationsWithParents:
                if sublist[1] == mutations[i]:
                    ancestor = sublist[0].lower()
                    break
            output = VCFFolder + '/' + nodeName + '.vcf'
            mutationFiles.append(output)
            ancestorFile = VCFFolder + '/' + ancestor + '.vcf'
            somaticCreator(ancestorFile, somaticFile, output)            
        '''
        else:
            ancestorIndex = re.sub('[^0-9]','',mutationsWithParents[i-1][1])
            ancestorVCF = mutationFiles[int(ancestorIndex)]
            output = VCFFolder + '/' + 'SOMATIC' + str(i) + '_' + outputName + '.vcf'
            mutationFiles.append(output)
            somaticCreator(ancestorVCF, somaticFile, output) 
    #print('VCF files have been generated.')
    '''
    '''        
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--DOT", help="Input dot File", metavar="DOT", type=str, required=True)
    parser.add_argument("-o","--OUT", help="Output name", metavar="OUT", type=str, required=True)
    parser.add_argument("-s","--SOM", help="Somatic VCF", metavar="SOM", type=str, default='CosmicCodingMuts.vcf', required=False)
    parser.add_argument("-g","--GERM", help="Germline VCF", metavar="GERM", type=str, default='Germline_UCSC.vcf', required=False)
    
    args = parser.parse_args()
    dotFile = args.DOT
    outputName = args.OUT
    germline = args.GERM
    somatic = args.SOM
    
    ListOfMutations, Mutations_Parents = dotParser(dotFile)
    VCFGenerator(ListOfMutations, Mutations_Parents, outputName, germline, somatic)

       
if __name__ == "__main__":
    main()
    '''