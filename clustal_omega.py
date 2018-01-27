# -*- coding: utf-8 -*-

import requests
import time
from Bio import Phylo
import os

# performs clustal omega and creates the multiple alignment and phylogenetic tree
def clustalo(file,malign,treef):
    f=open('MultipleAlign/'+file, 'rb')
    payload = {'email':'aa@gmail.com','sequence':f.read()}

    r = requests.post("http://www.ebi.ac.uk/Tools/services/rest/clustalo/run/", data=payload,)
    f.close()
    print(r.text)
    time.sleep(20)

    f=open(malign,'w')
    url='http://www.ebi.ac.uk/Tools/services/rest/clustalo/result/'+r.text+'/aln-clustal'
    re=requests.get(url)
    print(re.text,file=f)
    f.close()

    
    f=open('Phylotree.txt','w')
    url='http://www.ebi.ac.uk/Tools/services/rest/clustalo/result/'+r.text+'/phylotree'
    re=requests.get(url)
    print(re.text,file=f)
    f.close()
    

    f=open(treef,'w')
    tree=Phylo.read('Phylotree.txt',"newick")
    Phylo.draw_ascii(tree,file=f)
    f.close()

#performs clustal omega for each file 
def clustaloWrapper():
    filelist=os.listdir('MultipleAlign')
    for file in filelist:
       if 'sequences' in file:
            filename=''.join(file).split('.')
            id=filename[0].split('_')
            id=id[1]
            malign='MultipleAlign/Align_Outputs/malign_'+id+'.txt'
            treef='MultipleAlign/Tree_Outputs/tree_'+id+'.txt'
            clustalo(file,malign,treef)
            os.remove('Phylotree.txt')
            
clustaloWrapper()