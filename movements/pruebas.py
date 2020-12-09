import csv

with open('movements/data/pruebas.csv', 'r') as fichero:

    csvReader= csv.reader(fichero, delimiter=',', quotechar='"')
    registros = list(csvReader)

    for registro in registros:
        print(registro)
    
