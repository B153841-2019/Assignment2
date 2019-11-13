#!/user/bin/python3
#BPSM Assignment 2
#11 Nov 2019
#

# import the python modules that we need to use in this programme
import os,subprocess, shutil, logging, time

# To keep all outputs in a specific place, so we create a work directory and logfile
time=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
programmename="Protein"+" "+time
nowdir=os.getcwd()
os.mkdir(programmename)
os.chdir(nowdir+"/"+programmename)
logfile= 

# install the edirect in your 
curl    ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.zip -O
unzip edirect.zip
echo  'export PATH=/home/lmt/desktop/edirect/:$PATH'  >>  ~/.zshrc
source ~/.zshrc

#organism ???? eg. mammal mammalia
protein_name = input("Enter the protein name\n")   glucose-6-phosphatase
organism = input("Enter the organism\n")     
# get the UID values
esearch -db nucleotide -query "Cosmoscarta[organism]" | efetch -db nucleotide -format uid > Cosmoscarta.nuc.gis
# get the accession values
esearch -db nucleotide -query "Cosmoscarta[organism]" | efetch -db nucleotide -format acc > Cosmoscarta.nuc.acc
# get the fasta seq
search = "esearch -db protein -query '"+ protein_name + "[protein name]" + " " + "AND" + " " + organism +"[organism]" +" "+ "Not Partial"+"'" + "| efetch -format fasta > M.fa"
My_search = open("search.sh","w")
print(search,file=My_search)
My_search.close()
subprocess.call("chmod 700 search.sh", shell=True)
subprocess.call("./search.sh", shell=True)
head -5 Aves.fa
grep -c ">" Aves.fa

#10000sequences ????

#??specises ????

# alignment??
clustalo -i Aves.fa -o Aves_clustalo.fa

#Blast
testsequence.fasta
makeblastdb -in nem.fasta -dbtype prot -out nem
blastx -db  nem \
  -query testsequence.fasta  \
  -outfmt 7 > blastoutput2.out
# plotcon


# the PROSTE database












 