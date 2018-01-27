import xlsxwriter

def parse_loctree():

    #cria o ficheiro excel com a informação final
    workbook = xlsxwriter.Workbook('LocTree/output_loctree.xlsx')
    worksheet = workbook.add_worksheet("Localization Prediction")
    bold = workbook.add_format({'bold': True})
    worksheet.write("A1", "ID Proteína", bold)
    worksheet.write("B1", "Score", bold)
    worksheet.write("C1", "Localização", bold)
    worksheet.write("D1", "Gene Ontology Terms", bold)

    #retira os ids das proteinas existentes
    f=open('uniprotids.txt','r')
    ids=[]
    for line in f:
        ids.append(line.strip())

    #verifica se cada id existe no bd loctree e retira a informação pretendida
    row = 1
    col = 0
    with open('LocTree/LocTree.txt', 'r') as f:
        for line in f:
            line = line.strip()
            for id in ids:
                if id in line:
                    terms = line.split('\t')
                    worksheet.write(row, col, id)
                    worksheet.write(row, col + 1, terms[1])
                    worksheet.write(row, col + 2, terms[2])
                    worksheet.write(row, col + 3, terms[3])
                    row += 1
    workbook.close()



parse_loctree()