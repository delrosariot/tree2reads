import argparse
import dotParser

#A program that generates FASTQ files from a tree

USE_BED= False
USE_CUSTOM_GERM= False
USE_CUSTOM_SOM= False
#Parses through the line of user input
def manageInput():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--REF", help="Input reference file", metavar="REF", type=str, required=True)
    parser.add_argument("-d","--DOT", help="Input dot file", metavar="DOT", type=str, required=True)
    parser.add_argument("-o","--OUT", help="Output name", metavar="OUT", type=str, required=True)
    parser.add_argument("-p","--PER", help="Input percents file", metavar="PER", type=str, required=True)
    parser.add_argument("-l","--LEN", help="Length of the reads", metavar="LEN", type=int, default=100, required=False)
    parser.add_argument("-b","--BED", help="Bed files to use on NEAT run", metavar="BED", type=str, required=False)
    parser.add_argument("-c","--COV", help="Coverage for final FASTQ", metavar="COV", type=int, default=15, required=False)
    parser.add_argument("-i","--IND", help="Coverage for each individual read", metavar="IND", type=int, default=10, required=False)
    parser.add_argument("-s","--SOM", help="Custom somatic VCF", metavar="SOM", type=str, default='Main_VCFs/CosmicCodingMuts.vcf', required=False)
    parser.add_argument("-g","--GER", help="Custom germline VCF", metavar="GER", type=str, default='Main_VCFs/Germline_UCSC.vcf', required=False)
    
    args = parser.parse_args()
    reference = args.REF
    dotFile = args.DOT
    output = args.OUT
    percentFile = args.PER
    coverage = args.COV
    readLen = args.LEN
    
    customBed = args.BED
    if customBed != None:
        USE_BED = True
    
    individualCoverage = args.IND
    
    som = args.SOM   
    germ = args.GER
        
    #Make the VCFs
    generateVCF(dotFile, output, som, germ)

    #Returns a line with all of the commands for NEAT
    print('-r')
    print(reference)
    print('-R')
    print(readLen)
    print('--bam')
    print('--vcf')
    print('-M 0')
    print('-c')
    print(individualCoverage)
    if USE_BED:
        print('-t')
        print(customBed)
        
#Calls the script that makes the VCF files with the parsed user input       
def generateVCF(dotFile, outputName, germline, somatic):
    #Generates a list of all the nodes given in the tree, as well as their ancestors
    ListOfMutations, Mutations_Parents = dotParser.dotParser(dotFile)
    #Uses the generated lists to insert variants in the correct order and create VCF files
    dotParser.VCFGenerator(ListOfMutations, Mutations_Parents, outputName, germline, somatic)
    
def main():
    manageInput()

if __name__ == "__main__":
    main()




