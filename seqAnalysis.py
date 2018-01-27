# -*- coding: utf-8 -*-

from Bio import Entrez
from Bio import SeqIO
from bs4 import BeautifulSoup
import IDMapper
import requests
import xlsxwriter
import os

def geneAnalysis(i,genes=None):
    #Start excel FILE
    workbook = xlsxwriter.Workbook('GeneGBInfo/genesGenbank.xlsx')
    worksheet = workbook.add_worksheet("Genebank")
    bold = workbook.add_format({'bold': True})
    worksheet.write("A1", "GeneID", bold)
    worksheet.write("B1", "Location", bold)
    worksheet.write("C1", "Function", bold)
    worksheet.write("D1", "Gene" ,bold)
    worksheet.write("E1", "Locus tag" ,bold)
    worksheet.write("F1", "Note", bold)
    worksheet.write("G1", "Product", bold)
    worksheet.write("H1", "Protein_id", bold)
    worksheet.write("I1", "Sequence", bold)
    row=1
    col=0
    #End excel file

    #parse Genebank data
    handle = Entrez.efetch(db="nucleotide", rettype="gbwithparts", retmode="text",id=i,retmax=10**9,batchSize=1000)
    for seq_record in SeqIO.parse(handle, "gb"):
        g=[]
        protids=[]
        for feat in (seq_record.features):
            if feat.type=="CDS" and feat.qualifiers['locus_tag'][0] in genes :
                gene=feat.qualifiers['db_xref'][0].split(':') # ex. GeneID:19834053
                g.append(gene[1].strip())
                worksheet.write(row, col,gene[1].strip())
                col+=1
                worksheet.write(row, col,str(feat.location))
                col+=1
                worksheet.write(row, col,feat.qualifiers['function'][0])
                col+=1
                if('gene' in feat.qualifiers):
                    worksheet.write(row, col,feat.qualifiers['gene'][0])
                    col+=1
                else: col+=1
                worksheet.write(row, col,feat.qualifiers['locus_tag'][0])
                col+=1
                if('note' in feat.qualifiers):
                    worksheet.write(row, col,feat.qualifiers['note'][0])
                    col+=1
                else: col+=1
                worksheet.write(row, col,feat.qualifiers['product'][0])
                col+=1
                worksheet.write(row, col,feat.qualifiers['protein_id'][0])
                protids.append(feat.qualifiers['protein_id'][0])
                col+=1
                worksheet.write(row, col,str(seq_record.seq))
                col+=1
                
                row+=1
                col=0
              
        
        u=getUniProtIds(g)
        getUniProtInfo(u)
    
    f=open('protids.txt','w')
    for protid in protids:
        print(protid,file=f)
    f.close()
    workbook.close()

#map ncbi ids to uniprot ids
def getUniProtIds(genes):
    u=[]
    f=open('uniprotids.txt','w')
    for gene in genes:
        uniprot=IDMapper.idMapper(gene,'P_ENTREZGENEID','ACC')
        print(uniprot[0],file=f)
        u.append(uniprot[0])
    return u

#get uniprot raw data
def getUniProtInfo(uniprotIds):
    #Start excel FILE
    workbook = xlsxwriter.Workbook('UniprotInfo/genesUniprot.xlsx')
    worksheet = workbook.add_worksheet("Uniprot")
    bold = workbook.add_format({'bold': True})
    worksheet.write("A1", "Acession", bold)
    worksheet.write("B1", "Name", bold)
    worksheet.write("C1", "Protein fullname", bold)
    worksheet.write("D1", "EC_Number" ,bold)
    worksheet.write("E1", "Function" ,bold)
    worksheet.write("F1", "Catalytic Activity", bold)
    worksheet.write("G1", "Pathway", bold)
    worksheet.write("H1", "Location", bold)
    worksheet.write("I1", "GO Terms",bold)
    worksheet.write("J1", "Sequence Length", bold)
    worksheet.write("K1", "Sequence", bold)
    row=1
    col=0
    #End excel file
    filename='Blast/sequences.fasta'
    seqf=open(filename,'w')
    ecf=open('KEGG/ecnums.txt','w')
    for id in uniprotIds:
        url='http://www.uniprot.org/uniprot/'+id+'.xml'
        response=requests.get(url)
        ec=parseUniProtFile(response,worksheet,seqf,row,col)
        print(ec,file=ecf)
        row +=1
    seqf.close()
    workbook.close()

#parse uniprot raw data using beautifulsoup(xml parser) into xml file
def parseUniProtFile(response,worksheet,seqf,row,col):
    soup=BeautifulSoup(response.text,'lxml')
    worksheet.write(row, col,soup.find('accession').text)
    col+=1
    worksheet.write(row, col,soup.find('name').text)
    col+=1
    protein=soup.find('recommendedname')
    worksheet.write(row, col,protein.find('fullname').text)
    col+=1
    worksheet.write(row, col,protein.find('ecnumber').text)
    col+=1
    worksheet.write(row, col,soup.find('comment',{'type':'function'}).text)
    col+=1
    worksheet.write(row, col,soup.find('comment',{'type':'catalytic activity'}).text)
    col+=1
    worksheet.write(row, col,soup.find('comment',{'type':'pathway'}).text)
    col+=1
    worksheet.write(row, col,soup.find('location').text)
    col+=1
    gos=soup.findAll('dbreference',{'type':'GO'})
    goterms=[]
    for go in gos:
        goterms.append(go['id'])
    worksheet.write(row, col,str(goterms))
    col+=1
    seq=soup.findAll('sequence')
    for s in seq:
        if s.text:
            worksheet.write(row, col,s['length'])
            col+=1
            print('>',soup.find('accession').text,'|',soup.find('name',{'type':'ordered locus'}).text,'length=',s['length'],end='',file=seqf)
            worksheet.write(row, col,s.text)
            col+=1
            print(s.text,file=seqf)
    return protein.find('ecnumber').text
    
    

    
#os.remove('GeneGBInfo/genesGenbank.xlsx')
#os.remove('UniprotInfo/genesUniprot.xlsx')
geneAnalysis('NC_002942',['lpg0847','lpg2310','lpg2612','lpg2613','lpg2614','lpg2616','lpg0917','lpg2618','lpg2617','lpg0808'])

