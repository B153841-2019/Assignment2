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

# install the edirect


# Input
# Before you input the protein name and organism, please check the 
print("Before input the information, please check the name of protein and organism is official.")
protein_name = input("Enter the protein name\n")  
organism = input("Enter the organism\n")

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
      print("please try again!")
      if seq_number >= 1 and seq_number <= 10000:  
         break
      protein_name = input("Enter the protein name\n")  
      organism = input("Enter the organism\n")
      seqnumber= esearch(protein_name, organism)
      seq_number=int(seqnumber)
  return seq_number
      
seq_number=sequence_check(seq_number) 
print("the sequence number is :" + str(seq_number))     
 
cont = input("Do you want to continue?,Y/N\n")
while cont == 'N':
    if cont == 'Y':
       break
    print("try it again!")
    protein_name = input("Enter the protein name\n")  
    organism = input("Enter the organism\n")
    seqnumber = esearch(protein_name, organism)
    seq_number =int(seqnumber)
    seq_number=sequence_check(seq_number)  
    print("the sequence number is :" + str(seq_number)) 
    cont = input("Do you want to continue?,Y/N\n")

# alignment
subprocess.call("clustalo -i protein_seq.fa --full --percent-id  --distmat-out=clustalo_matrix.txt --outfmt=msf > clustalo_output.msf", shell=True)


# infoalign
subprocess.call("infoalign -sequences clustalo_output.msf -outfile 1.infoalign", shell=True)
import pandas as pd
import numpy as np
df = pd.read_csv('1.infoalign', sep='\t')
np.min(df['Differ'])
a=(df.Differ.idxmin())
a=str(a[1])

# download the fasta file

msearch = "esearch -db protein -query '"+ a + "' | efetch -format fasta > test.fasta"
Motif_search = open("msearch.sh","w")
print(msearch,file=Motif_search)
Motif_search.close()
subprocess.call("chmod 700 msearch.sh", shell=True)
subprocess.call("./msearch.sh", shell=True)

# plotcon
subprocess.call("plotcon -sequences output.msf -winsize 10 -graph svg", shell=True)
subprocess.call("display plotcon.svg", shell=True)

#patmatmotifs
subprocess.getoutput("patmatmotifs -sequence 'test.fasta' -outfile patmatmotifs.txt")
subprocess.call("chmod 700 patmatmotifs.txt", shell=True)

f = open("patmatmotifs.txt")             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line:
    print line,                 # 后面跟 ',' 将忽略换行符
    # print(line, end = '')　　　# 在 Python 3中使用
    line = f.readline()
f.close()
# other 






    














 