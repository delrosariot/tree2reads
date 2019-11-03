import sys 

def extensionRemover(filename):
    filename = filename.strip('.vcf')
    print filename
    return filename

extensionRemover(sys.argv[1])