# -*- coding: utf-8 -*-
import xlsxwriter

def transcriptionFactorsParse(filename):
    #Start excel FILE
    workbook = xlsxwriter.Workbook('TransriptionFactors/Legpneumo_TranscriptionFactors.xlsx')
    worksheet = workbook.add_worksheet("DBD Results")
    bold = workbook.add_format({'bold': True})
    worksheet.write("A1", "	Hidden Markov Model identifier", bold)
    worksheet.write("B1", "Sequence identifier", bold)
    worksheet.write("C1", "Match region", bold)
    worksheet.write("D1", "Family name", bold)
    row = 1
    col = 0
    #End excel file
    
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    g = open('protids.txt', 'r')
    ids = g.readlines()
    id_list = []
    for id in ids:
        id = id.strip()
        id_list.append(id)
    g.close()


    for i in range(1, len(lines)):
        terms = lines[i].split('\t')
        for id in id_list:
            if id == terms[1][16:len(terms[1])-1]:
                for i in range(len(terms)):
                    print(row, col+1, terms[i])
                    worksheet.write(row, col+i, terms[i])
                row += 1

    workbook.close() 

transcriptionFactorsParse('TransriptionFactors/x7.tf.ass')