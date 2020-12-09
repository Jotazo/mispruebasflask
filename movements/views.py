from movements import app
from flask import render_template, request, redirect
import csv


@app.route('/')
def listaIngresos():
    
    with open("movements/data/basededatos.csv", "r") as fichero:
        csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
        ingresos = list(csvReader)
        fichero.close()
        
        total = 0
        for ingreso in ingresos:
            total += float(ingreso[2])
            total = round(total,2)
    
    return render_template("movementsList.html",datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET','POST'])
def nuevoIngreso():
    if request.method == 'POST':
        fecha = request.form.get('date')
        concepto = request.form.get('concept')
        dinero = request.form.get('money')
        
        with open('movements/data/basededatos.csv', mode='a', newline='') as fichero:
            fIngresos = csv.writer(fichero, delimiter=',', quotechar="'")
            fIngresos.writerow([fecha, concepto, dinero])
            fichero.close()
            
        return redirect('/')

    return render_template('creaalta.html')

@app.route('/buscaregistro/<tipo_busqueda>', methods=['GET', 'POST'])
def buscar(tipo_busqueda):
    if request.method == 'POST':
        fecha = ''
        concepto = request.form.get('concept')
        dinero = ''
        with open('movements/data/basededatos.csv', mode='r') as fichero:
            csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
            registros = list(csvReader)
            fichero.close()
            registroEncontrado = False
            
            for registro in registros:
                if registro[1] == concepto:
                    fecha = registro[0]
                    dinero = registro[2]
                    registroEncontrado = True

            if not registroEncontrado:       
                return render_template('buscaregistro.html', encontrado=registroEncontrado, concepto=concepto, tipo_busqueda=tipo_busqueda)
            else:
                if tipo_busqueda == 'Actualizar':
                    return render_template('actualizaregistro.html', fecha=fecha, concepto=concepto, dinero=dinero)
                elif tipo_busqueda == 'Borrar':
                    return render_template('borraregistro.html', fecha=fecha, concepto=concepto, dinero=dinero)

    registroEncontrado = True
    return render_template('buscaregistro.html', tipo_busqueda=tipo_busqueda, encontrado = registroEncontrado)

@app.route('/actualizaregistro', methods=['POST'])
def actualizar():

    with open('movements/data/basededatos.csv', 'r') as fichero:
        csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
        registros = list(csvReader)
        fichero.close()

    nuevaFecha = request.form.get('date')
    concepto = request.form.get('concept')
    nuevoDinero = request.form.get('money')
    registroActualizado = []
    for registro in registros:
        if registro[1] == concepto:
            registroActualizado.append([nuevaFecha, concepto, nuevoDinero])
        else:
            registroActualizado.append(registro)

    with open('movements/data/basededatos.csv', 'w', newline='') as fichero:
        csvWriter = csv.writer(fichero, delimiter=',', quotechar='"')
        print(registroActualizado)
        csvWriter.writerows(registroActualizado)
        
        fichero.close()

    return redirect('/')

@app.route('/borraregistro', methods=['POST'])
def borrar():

    with open('movements/data/basededatos.csv', 'r') as fichero:
        csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
        registros = list(csvReader)
        fichero.close()

    nuevaFecha = request.form.get('date')
    concepto = request.form.get('concept')
    nuevoDinero = request.form.get('money')
    registroActualizado = []

    for registro in registros:
        if registro[1] != concepto:
            registroActualizado.append(registro)
            
    with open('movements/data/basededatos.csv', 'w', newline='') as fichero:
        csvWriter = csv.writer(fichero, delimiter=',', quotechar='"')
        print(registroActualizado)
        csvWriter.writerows(registroActualizado)
        
        fichero.close()

    return redirect('/')

        

            


            
            
                    
