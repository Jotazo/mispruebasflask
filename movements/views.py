from movements import app
from flask import render_template, request, redirect
import csv


@app.route('/')
def listaIngresos():
    
    with open("movements/data/basededatos.csv", "r") as fichero:
        csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
        ingresos = list(csvReader)
        fichero.close()
        
        if not ingresos:
            return render_template('movementsListNull.html')

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

@app.route('/buscaregistro', methods=['GET', 'POST'])
def buscar():
    if request.method == 'GET':
        return render_template('buscaregistro.html')
    else:
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
                return render_template('actualizaregistro-noencontrado.html', concepto=concepto)
            else:
                return render_template('actualizaregistro-encontrado.html', fecha=fecha, concepto=concepto, dinero=dinero)

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
        

            


            
            
                    
