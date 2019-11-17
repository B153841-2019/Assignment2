#!/user/bin/python3
#BPSM Assignment 2
#11 Nov 2019
#

# import the python modules that we need to use in this programme
import os,subprocess, shutil, time

# To keep all outputs in a specific place, so we create a work directory and logfile
time=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
programmename="Protein"+" "+time
nowdir=os.getcwd()
os.mkdir(programmename)
os.chdir(nowdir+"/"+programmename)
my_logfile=open("my_logfile.txt","w")
my_logfile.write("Start to search the protein sequence."+time+"\n")
my_logfile.close()

# install the edirect


# Input
# Before you input the protein name and organism, please check the 
print("Before input the information, please check the name of protein and organism is official.")
protein_name = input("Enter the protein name\n")  
organism = input("Enter the organism name\n")

# get the fasta seq
def esearch(protein_name, organism):
    search = "esearch -db protein -query '"+ protein_name + "[protein name]" + " AND " + organism +"[organism]" + " Not Partial' " + "| efetch -format fasta > protein_seq.fasta"
    My_search = open("search.sh","w")
    print(search,file=My_search)
    My_search.close()
    subprocess.call("chmod 700 search.sh", shell=True)
    subprocess.call("./search.sh", shell=True)
    seqnumber= subprocess.getoutput("grep -c '>' protein_seq.fasta")
    return seqnumber

seqnumber = esearch(protein_name, organism)
seq_number=int(seqnumber)

#10000sequences
def sequence_check(seq_number):
  while seq_number <= 1 or seq_number >= 10000:
      print("Sorry,there is no result or over 10000 sequences. Please input again!")
      if seq_number >= 1 and seq_number <= 10000:  
         break
      protein_name = input("Enter the protein name\n")  
      organism = input("Enter the organism name\n")
      seqnumber= esearch(protein_name, organism)
      seq_number=int(seqnumber)
  return seq_number
      
seq_number=sequence_check(seq_number) 
print("the number of sequences is :" + str(seq_number))     
 
cont = input("Do you want to continue?,Y/N\n")
while cont == 'N':
    if cont == 'Y':
       break
    print("Please input again!")
    protein_name = input("Enter the protein name\n")  
    organism = input("Enter the organism\n")
    seqnumber = esearch(protein_name, organism)
    seq_number =int(seqnumber)
    seq_number=sequence_check(seq_number)  
    print("the number of sequences found is :" + str(seq_number)) 
    cont = input("Do you want to continue?,Y/N\n")

# alignment
subprocess.call("clustalo -i protein_seq.fasta --full --percent-id  --distmat-out=clustalo_matrix.txt --outfmt=msf > clustalo_output.msf", shell=True)
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The clustalo has been done."+ time+"\n")
print("The clustalo has been done.")

# infoalign
subprocess.call("infoalign -sequence clustalo_output.msf -only -name  -outfile output1.infoalign ", shell=True)
subprocess.call("infoalign -sequence clustalo_output.msf -only -diffcount -outfile output2.infoalign ", shell=True)

f1=open("output1.infoalign").read()
list1 =f1.split("\n")
f2=open("output2.infoalign").read()
list2 =f2.split("\n")
from pandas.core.frame import DataFrame
c={"Name" : list1,
   "Differ" : list2}
data=DataFrame(c)
data=data.set_index('Name')





# download the fasta file
msearch = "esearch -db protein -query '"+ a + "' | efetch -format fasta > choose.fasta"
Motif_search = open("msearch.sh","w")
print(msearch,file=Motif_search)
Motif_search.close()
subprocess.call("chmod 700 msearch.sh", shell=True)
subprocess.call("./msearch.sh", shell=True)

#blast
test.fa
makeblastdb -in protein_seq.fasta -dbtype prot -out proteindatabase
blastp -db proteindatabase -query test1.fa > blastoutput1_1.out

blastp -db  proteindatabase \
  -query test.fa  \
  -outfmt 7 > blastoutput1_2.out


# plotcon
subprocess.call("plotcon -sequences clustalo_output.msf -winsize 10 -graph svg", shell=True)
subprocess.call("display plotcon.svg", shell=True)

#patmatmotifs
subprocess.getoutput("patmatmotifs -sequence 'choose.fasta' -outfile patmatmotifs.txt")
subprocess.call("chmod 700 patmatmotifs.txt", shell=True)

# the wild card  preg pscan fuzzpro
fuzzpro -sequence "choose.fasta" -outfile report
pscan -sequence "choose.fasta" -outfile name








    














 