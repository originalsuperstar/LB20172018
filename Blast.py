from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML 
from Bio import SeqIO
from bs4 import BeautifulSoup
import requests
import os
import xlsxwriter

#performs blast search
def blast(path,form='fasta'):
    records=list(SeqIO.parse(path,form))
    for record in records:
        print('Start Search....')
        result_handle = NCBIWWW.qblast('blastp','swissprot',record.format(form),expect=3.0,hitlist_size=10)
        filename=saveBlastOutput(result_handle,record.id.strip())
        verifyBlast(filename,record.id.strip(),str(record.seq))

#saves result from search in xml file   
def saveBlastOutput(result_handle,id):
    filename='Blast/BlastOutput/blast_output_'+id+'.xml'
    save_file=open(filename,'w')
    save_file.write(result_handle.read())
    save_file.close()
    result_handle.close()
    return filename

#parse the xml file from output into an excel file
def verifyBlast(filename,id,sequence):
    #Start excel FILE
    workbook = xlsxwriter.Workbook('Blast/BlastOutput/blast_'+id+'_align.xlsx')
    worksheet = workbook.add_worksheet("Blast Results")
    bold = workbook.add_format({'bold': True})
    worksheet.write("A1", "Sequence", bold)
    worksheet.write("B1", "Sequence length", bold)
    worksheet.write("C1", "Score", bold)
    worksheet.write("D1", "Gaps" ,bold)
    worksheet.write("E1", "E-value" ,bold)
    worksheet.write("F1", "hsp.query", bold)
    worksheet.write("G1", "hsp.match", bold)
    worksheet.write("H1", "hsp.sbjct", bold)
    worksheet.write("I1", "Acession", bold)
    worksheet.write("J1", "Function", bold)
    worksheet.write("K1", "Pathway", bold)
    worksheet.write("L1", "Location", bold)
    #End excel file
    row = 1
    col = 0
    #start make sequences file
    f=open('MultipleAlign/sequences_'+id+'.txt','w')
    print('>'+id,file=f)
    print(sequence+'\n',file=f)
    #end make sequences file 
    result=open(filename, 'r')
    records=NCBIXML.parse(result)
    item=next(records)
    for alignment in item.alignments:
         for hsp in alignment.hsps:
            if hsp.expect <0.05:
                worksheet.write(row, col,alignment.hit_id)
                col+=1
                worksheet.write(row, col,alignment.length)
                col+=1
                worksheet.write(row, col,hsp.score)
                col+=1
                worksheet.write(row, col,hsp.gaps)
                col+=1
                worksheet.write(row, col,hsp.expect)
                col+=1
                worksheet.write(row, col,hsp.query[0:75])
                col+=1

                worksheet.write(row, col,hsp.match[0:75])
                col+=1
                worksheet.write(row, col,hsp.sbjct[0:75])
                col+=1
                row,col=getFunctions(alignment.accession,row,col,worksheet)
                row+=1
                col=0
                print('>'+alignment.hit_id,file=f)
                print(hsp.sbjct+'\n',file=f)
    result.close()
    workbook.close()

# get functions from uniprot for each hit   
def getFunctions(accession,row,col,worksheet):
    url='http://www.uniprot.org/uniprot/'+accession+'.xml'
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'lxml')
    worksheet.write(row, col,accession)
    col+=1
    worksheet.write(row, col,soup.find('comment',{'type':'function'}).text)
    col+=1
    worksheet.write(row, col,soup.find('comment',{'type':'pathway'}).text)
    col+=1
    worksheet.write(row, col,soup.find('location').text)
    col+=1
    
    return (row,col)

# parse blast outputs. does not perform a search. Used to avoid searching all the time and save time, only possible when there is previous output   
def parseBlastNoSearch(filename):
    filelist=os.listdir('Blast/BlastOutput')
    fasta_sequences=list(SeqIO.parse(open(filename),'fasta'))
    i=0
    for file in filelist:
       if 'xml' in file:
            sequence=str(fasta_sequences[i].seq)
            filename=''.join(file).split('.')
            id=filename[0].split('_')
            id=id[2]
            filename='Blast/BlastOutput/'+''.join(file)
            verifyBlast(filename,id,sequence)


#blast('Blast/sequences.fasta')
parseBlastNoSearch('Blast/sequences.fasta')