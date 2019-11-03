# Tree2Reads

This pipeline allows the user to simulate data for a heterogeneous tumor using an evolution tree in dot format as input. The output data is in the form of a set of reads in a FASTQ file. It makes use of the read simulator [NEAT genreads](https://github.com/zstephens/neat-genreads). 


Tree2Reads takes as input a reference file from which to generate the reads, along with a list of the percents associated with each of the nodes, a tree of the mutations to be generated, and two sets of VCFs. The program parses through the dot file that represents the tree and outputs all of the nodes/mutations. This list is then used to generate a VCF for each of the nodes, taking into account the variants inserted in their ancestor(s) and including them into this new VCF. Once all of these VCFs are generated, the pipeline uses NEAT genreads to generate reads. This program takes as input a VCF file and a reference FASTA and outputs a FASTQ file with the reads. Once all of the FASTQ files are generated, the pipeline uses a merger script to put all of the FASTQs into a single FASTQ with the correct percentage of each mutation (provided as input by the user in a percents.txt file). The percentage taken from each FASTQ depends on what the user inputs for final coverage and average read length. 

![Flowchart with the process of converting a tree into a set of reads](https://github.com/delrosariot/tree2reads/blob/master/Sample_Files/Tree2Reads.png "Flowchart with the process of converting a tree into a set of reads")
---

## Requirements

* NetworkX 1.11
* Python 2.7
* Numpy 1.9.1 +
* NEAT genreads (NEAT can be downloaded and installed separately, but the location containing the NEAT folder must be specified in the config file (*config.txt*). )

---

## Usage

### Tree2Reads
```
Options: 
	-h	Shows information about the program.
	-r	Reference file [FASTA]. **Required**.
	-d	Tree of the mutations [DOT]. **Required**.
	-o	Output name for the run [STR]. **Required**.
	-p	Percents of each of the mutations [TXT]. **Required**.
	-l	Length of the reads. All of the reads will be this length. Default=100 [INT].
	-b	Bed file with regions to focus on [BED].
	-c	Total coverage of the reads. Default=15 [INT].
	-i	Average coverage for the reads of each mutation/node. Default=10 [INT]. 
	-s	Somatic VCF to use for non-root mutations [VCF]. 
	-g	Germline VCF to use for root mutations [VCF].
```

Sample command using default files:
```
	bash Tree2Reads.bash -r Reference/Chromosome19_hg38.fa -d Sample_Files/SimpleTree.gv -o testRun -p Sample_Files/percents.txt -b Sample_Files/Small19Region.bed
```


This command will output a FASTQ file called *Final_Reads_testRun.fq*. These reads represent all of the mutations of the input tree (SimpleTree.gv). Additionally, the pipeline creates two folders: *VCFs_testRun*, which contains the VCFs with the variants inserted in each of the mutations, and *Reads_testRun*, which contains the reads generated for each of the mutations.  


---

## Examples

### Sample dot tree file:
```
	graph { 
		mut1 -- mut2;
		mut1 -- mut3;
		root -- mut1;
	}
```
Note that these files must have only one edge per line. Additionally, one of the nodes must be named “root”. This is the node in the tree that has no ancestors. The other nodes may be named in any manner, but be aware that the program does not distinguish lowercase from uppercase (e.g. mut1 is the same node as Mut1 and MUT1). 


### Sample percents file:
```
	root	0.2
	mut1	0.5
	mut2	0.1
	mut3	0.2
```

This file must be tab delimited, with the first column being the node name and the second column the percent [FLOAT between 0 and 1] associated with that mutation. The sum of all the values in column two must add up to 1. 
 
 
### Simulate reads on targeted regions:
```
	bash Tree2Reads.bash -r ref.fa -d tree.gv -o outputName -p percents.txt -b targets.bed
```


### Simulate reads with a custom VCF for somatic mutations:
```
	bash Tree2Reads.bash -r ref.fa -d tree.gv -o outputName -p percents.txt -s custom.vcf
```



### Sample files:
These files are included in the *Sample_Files* folder.
```
	-b   Small19Region.bed - A small region within chromosome 19. Mapped to GRCh38 [BED].
	-d   SimpleTree.gv - A simple tree with the correct naming conventions [DOT].
	-p   percents.txt - A percents file that matches SimpleTree.gv  [Percents File].
	-r   Chromosome19_hg38.fa - A reference file of chromosome 19, mapped to GRCh38 [FASTA].
	Chromosome19_hg38.fa.fai - The matching index to the given sample Reference [FAI].
```

### Note:
The somatic and germline VCF files used must both use the same human genome reference (e.g. hg19 or hg38) as the reference FASTA. Otherwise, the program will not be able to insert any valid variants.  

	
The reference file must be indexed in order for the program to run properly. This can be achieved with samtools [ samtools faidx ref.fa ]. Both files must be in the same location and be named the same (e.g. ref.fa and ref.fa.fai); note that this is the samtools output. 

	
This pipeline will output files from each step automatically into different folders, but the final file (FASTQ) will be in the format *Final_Reads_Output.fq*.
	
	
	
 
