import argparse

#Count the total number of mutations in a FASTQ
def CountLines(mutationsFile):
    lines = 0
    mutationReads = open(mutationsFile, 'r')
    for line in mutationReads:
        lines = lines + 1
    mutationReads.close()
    return lines//4

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--SOM", help="Somatic Mutations file", metavar="SOM", type=str, required=True)
    
    args = parser.parse_args()
    somatic = args.SOM
    print(CountLines(somatic))
       
if __name__ == "__main__":
    main()