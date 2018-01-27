# -*- coding: utf-8 -*-

import requests
import re


def idMapper(gene,bd1,bd2):
    url = 'http://www.uniprot.org/uploadlists/'

    map_params = {
            'from':bd1,
            'to':bd2,
            'format':'tab',
            'query':gene
            }

    response=requests.get(url,params=map_params)
    x=response.text.split('\n')
    data=[]
    for r in range(1,len(x)-1):
        s=re.split('\t+',x[r])
        if len(s)>=1:
            data.append(s[1])

    #print(data)
    return data

