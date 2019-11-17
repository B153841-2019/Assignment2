#!/user/bin/python3
#BPSM Assignment 2
#17 Nov 2019
#

# To keep all outputs in a specific place, so we create a work directory and logfile
# Import the python modules that we need to use in this project
import os,subprocess, time

# Set the the work directory name and the time
time=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) # set the local time
projectname="Protein_identify"+" "+time # name the project
nowdir=os.getcwd()
os.mkdir(projectname) # make the directory
os.chdir(nowdir+"/"+projectname) # change the directory as the current directory

# keep a log of what is being done and when, and we save it to the project directory
my_logfile=open("my_logfile.txt","w")
my_logfile.write("Start to search the protein sequences."+time+"\n")
my_logfile.close()

# Let the user input the names of the protein and organism 
print("Before input the information, please check the names of protein and organism are official!")
protein_name = input("Enter the protein name\n")  
organism = input("Enter the organism name\n")

# Set a function to download the fasta files from the NCBI and get the number of the sequences
def esearch(protein_name, organism):
    search = "esearch -db protein -query '"+ protein_name + "[protein name]" + " AND " + organism +"[organism]' " + "| efetch -format fasta > protein_seq.fasta"
    My_search = open("search.sh","w") # create the a small unix script 
    print(search,file=My_search)
    My_search.close()
    subprocess.call("chmod 700 search.sh", shell=True) # change the permission of the script
    subprocess.call("./search.sh", shell=True) # run it
    seqnumber= subprocess.getoutput("grep -c '>' protein_seq.fasta") # get the number of the sequences that we download
    return seqnumber

# Use the fuction after get the input information
seqnumber = esearch(protein_name, organism)
seq_number=int(seqnumber) # change the string to integer to compare in the next function

# Set a function to limit the number of sequence and report the situation that there is no result for the search
def sequence_check(seq_number):
  while seq_number <= 1 or seq_number >= 10000:
      print("Sorry,there is no result or over 10000 sequences. Please input again!")
      if seq_number >= 1 and seq_number <= 10000:  
         break
      protein_name = input("Enter the protein name\n")  
      organism = input("Enter the organism name\n")
      seqnumber= esearch(protein_name, organism) # use the first function
      seq_number=int(seqnumber)
  return seq_number

# Use the function 
seq_number=sequence_check(seq_number) 

# Tell the user about the number od sequences that found and ask if countinue or not 
print("the number of sequences is :" + str(seq_number))     
cont = input("Do you want to continue?,Y/N\n")

# Set a loop for the different decisioin that mader by the user 
while cont == 'N':
    if cont == 'Y':
       break
    print("Please input again!")
    protein_name = input("Enter the protein name\n")  
    organism = input("Enter the organism\n")
    seqnumber = esearch(protein_name, organism) # use the first founction
    seq_number =int(seqnumber)
    seq_number=sequence_check(seq_number) # use the second founction
    print("the number of sequences found is :" + str(seq_number)) 
    cont = input("Do you want to continue?,Y/N\n")

# This stage has been done
print("The sequence search has been done and be saved as a output file.")
# Write the logfile
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The sequence search has been done and be saved as a output file."+ time+"\n")



# Use clustalo and set the maximum sequences number is 250
subprocess.call("clustalo -i protein_seq.fasta --full --maxnumseq=250 --outfmt=msf > clustalo_output.msf", shell=True)
# This stage has been done
print("The clustalo has been done and be saved as a file output.")

# Ask the user if display the output
q1 = input("Do you want to display it?,Y/N\n")
if q1 == 'Y':
    print("type q to stop")
    subprocess.call("more clustalo_output.msf", shell=True)
else:
    print("Let's move on!")
# Write the logfile
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The clustalo has been done and be saved as a file output."+ time+"\n")



# Use plotcon to plot the similarity amonge these sequences
subprocess.call("plotcon -sequences clustalo_output.msf -winsize 10 -graph svg", shell=True)
# This stage has been done
print("The plotcon has been done and be saved as a output file.")

# Ask the user if display the output
q2 = input("Do you want to display it?,Y/N\n")
if q2 == 'Y':
    subprocess.call("display plotcon.svg", shell=True)
else:
    print("Let's move on!")
# Write the logfile
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The plotcon has been done and be saved as a output file."+ time+"\n")


# Use infoalign that is a tool for the basic information about sequences in an input multiple sequence alignment. 
# This includes the sequences' USA, name, two measures of length, counts of gaps, and numbers of identical, similar and different residues 
# or bases in this sequence when compared to a reference sequence, together with a simple statistic of the % change between the reference sequence and this sequence
# We use the %change as the standard to choose the most representative sequence
# Download the name part
subprocess.call("infoalign -sequence clustalo_output.msf -only -name -outfile output1.infoalign ", shell=True)
# Download the %change part
subprocess.call("infoalign -sequence clustalo_output.msf -only -change -outfile output2.infoalign ", shell=True)
# Set the name as keys
f1=open("output1.infoalign").read()
f1=f1.rstrip("\n")
keys =f1.split("\n")
# Set the %change as values
f2=open("output2.infoalign").read()
f2=f2.rstrip("\n")
list2 =f2.split("\n")
values = list(map(float, list2))
# Find the minimum %change
a=min(values)
# Create the dictionary
dictionary = dict(zip(keys, values))
# Put the name of the minimum %change into a list
# In case, there is more than one sequence, we use the loop tp do the same things 
result = []
for i in dictionary.keys():
    value = dictionary[i]
    if value == a:
        result.append(i) # add every value that equal to the minimum
# display the result list
print("This the name of the minumim %change sequence.")
print(result)

# Download the file contain the name and %change
subprocess.call("infoalign -sequence clustalo_output.msf -only -heading -name -change -outfile output.infoalign ", shell=True)
# Write the logfile and time
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The infoalign has been done and be saved as a output file."+ time+"\n")
print("The infoalign has been done and be saved as a output file.")


# Download the minimum %changes sequences fasta file
# In case, there is more than one sequence, we use a loop to do the same things
for i in range(len(result)):
 i-=0 # start with 0
 a=result[i]  # This stage has be done
 msearch = "esearch -db protein -query '"+ a + "' | efetch -format fasta > choose"+a+".fasta"
 Motif_search = open("msearch.sh","w") # create the a small unix script to download the fasta file
 print(msearch,file=Motif_search)
 Motif_search.close()
 subprocess.call("chmod 700 msearch.sh", shell=True) # change the permission
 subprocess.call("./msearch.sh", shell=True)
 
# Find the motif in the PROSITE database
 subprocess.getoutput("patmatmotifs -sequence 'choose"+a+".fasta' -outfile "+a+"patmatmotifs.txt") # create the a small unix script to download the fasta file
 subprocess.call("chmod 700 "+a+"patmatmotifs.txt", shell=True) # change the permission
# This stage has be done
print("The patmatmotifs has been done and be saved as output files.")

# Ask the user if display the output
q3 = input("Do you want to display it?,Y/N\n")
if q3 == 'Y':
    print(open(a+"patmatmotifs.txt").read())
else:
    print("Let's move on!")
# Write the logfile and time
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The patmatmotifs has been done and be saved as output files."+ time+"\n")


# Antigenic predicts potentially antigenic regions of a protein sequence, using the method of Kolaskar and Tongaonkar.
# Find the antigenic part of the protein motif
for i in range(len(result)):
 i-=0 # start with 0
 a=result[i] # choose every element in the list
 subprocess.call("antigenic -sequence 'choose"+a+".fasta' -outfile "+a+"report", shell=True) # generate the report
# This stage has be done
print("The antigenic part has been done and be saved as output files.") 

# Ask the user if display the output
q4 = input("Do you want to display it?,Y/N\n")
if q4 == 'Y':
    print(open(a+"report").read())
else:
    print("Let's move on!")
# Write the logfile and time
my_logfile = open("my_logfile.txt", "a")
my_logfile.write("The antigenic part has been done and be saved as output files."+ time+"\n")


# Delete the unimportant files
os.remove("msearch.sh")
os.remove("search.sh")
os.remove("output1.infoalign")
os.remove("output2.infoalign")
# All has been finished
print("All has been finished, check the work directory to find the output files.")















    














 