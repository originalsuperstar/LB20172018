# -*- coding: utf-8 -*-
from Bio.KEGG import REST
from Bio.KEGG import Enzyme
import xlsxwriter

#get kegg raw data
def getKegg(listlocus,output):
    entries = []
    for locus in listlocus:
        print('Searching..')
        search = REST.kegg_find("genes", locus).read()
        entries.append(search)
        print('Done..')
    f = open(output, 'w')
    for entry in entries:
        print(entry,file=f)
    f.close()

def parseKegg(filename):
    f = open('KEGG/kegg_entries.txt', 'r')
    search_terms = []
    for line in f.readlines():
        terms = line.split('\t')
        if terms[0] != '\n': 
            search_terms.append(terms[0])
    f.close()
    for term in search_terms:
        filename = 'KEGG/KEGG_output/kegg_entry' + term + '.txt'
        filename = filename.replace(':', '')
        output = open(filename, 'w') 
        entry = REST.kegg_get(term)
        for line in entry.readlines():
            print(line,file=output)
        output.close()

#create excel file with kegg information for each gene
def parseEnzyme():
    #Start excel FILE
    workbook = xlsxwriter.Workbook('KEGG/LegpneumoEnzymes.xlsx')
    worksheet = workbook.add_worksheet("KEGG Enzymes")
    bold = workbook.add_format({'bold': True})
    worksheet.write("A1", "Locus Tag", bold)
    worksheet.write("B1", "EC Number", bold)
    worksheet.write("C1", "KEGG Orthologs", bold)
    worksheet.write("D1", "KEGG Reactions IDs", bold)
    worksheet.write("E1", "KEGG Pathways", bold)
    row = 1
    col = 0
    #End excel file

    ec = open("KEGG/ecnums.txt", "r")
    ec_nums = []
    for line in ec.readlines():
        line = line.strip()
        ec_nums.append(line)

    for ec_num in ec_nums:
        if "-" in ec_num:
            continue
        print(ec_num)
        res = []
        request = REST.kegg_get("ec:"+ec_num)
        open("KEGG/Enzymes/ec_"+ec_num+".txt", 'w').write(request.read())
        filename="KEGG/Enzymes/ec_"+ec_num+".txt"
        records = Enzyme.parse(open(filename))
        record = list(records)[0]
        # locus_tag
        gene = ""
        for g in record.genes:
            if "LPN" in g:
                gene = g
        if gene != "":
            gene = ''.join(gene[1])
        res.append(gene)
        # EC Number
        ec_number = record.entry
        res.append(ec_number)
        # KEGG Ortholog
        f = open(filename, 'r')
        orthologs = []
        for line in f.readlines():
            if line[:12] != "            ":
                keyword = line[:12]
            data = line[12:].strip()
            if "ORTHOLOGY" in keyword:
                orthologs.append(data)
        f.close()
        orth_str = ""
        for ortholog in orthologs:
            orth_str += ortholog + ", "
        res.append(orth_str)
        # KEGG Reaction
        reactions = record.reaction
        if len(reactions) > 1:
            reac_list = ""
            for reaction in reactions:
                reac_list += reaction + ', '
            res.append(reac_list)
        else:
            res.append(''.join(reactions))
        # Kegg Pathways
        pathways = record.pathway
        path_str = ""
        for pathway in pathways:
            id = pathway[1]
            path = pathway[2]
            path_str += id + ": " + path + ", "
        res.append(path_str)

        for i in range(len(res)):
            worksheet.write(row, col+i, res[i])
        row += 1

    workbook.close() # close the workbook

#getKegg(['lpg0847','lpg2310','lpg2612','lpg2613','lpg2614','lpg2616','lpg0917','lpg2618','lpg2617','lpg0808'],'KEGG/kegg_entries.txt')
#parseKegg('KEGG/kegg_entries.txt')
parseEnzyme()