#Daniel Oñate Hernandez - 20191020016#

import pandas as pd
from sodapy import Socrata
from dateutil import parser
from flask import Flask, render_template, request, redirect, url_for

cliente = Socrata("www.datos.gov.co", None)
results = cliente.get("gt2j-8ykr", limit=1762)

cdf = pd.DataFrame.from_records(results)

cdf['fecha_de_notificaci_n'] = cdf['fecha_de_notificaci_n'].dropna(axis=0, how='any')
cdf['fecha_reporte_web'] = cdf['fecha_reporte_web'].dropna(axis=0, how='any')
cdf['fecha_diagnostico'] = cdf['fecha_diagnostico'].dropna(axis=0, how='any')

cdf = cdf.fillna(value='No Registra')

cdf['fecha_de_notificaci_n'] = cdf['fecha_de_notificaci_n'].apply(parser.parse)
cdf['fecha_reporte_web'] = cdf['fecha_reporte_web'].apply(parser.parse)
cdf['fecha_diagnostico'] = cdf['fecha_diagnostico'].apply(parser.parse)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', datos=cdf.to_html())

@app.route('/filtrar', methods=['POST'])
def filtrar():
    if request.method == 'POST':

        if request.form['ciudad'] != '' and request.form['fecha'] != '':
            return render_template('index.html', datos=cdf[(cdf['ciudad_municipio_nom'] == request.form['ciudad']) & (cdf['fecha_diagnostico'] == request.form['fecha'])].to_html())

        elif request.form['ciudad'] != '' and request.form['fecha'] == '':
            return render_template('index.html', datos=cdf[cdf['ciudad_municipio_nom'] == request.form['ciudad']].to_html())

        elif request.form['fecha'] != '' and request.form['ciudad'] == '':
            return render_template('index.html', datos=cdf[cdf['fecha_diagnostico'] == request.form['fecha']].to_html())

        else:
            return redirect(url_for('index'))

@app.route('/grupoC', methods=['GET'])
def grupoC():
    return render_template('index.html', datos=pd.DataFrame(cdf['ciudad_municipio_nom'].value_counts()).to_html())

@app.route('/grupoF', methods=['GET'])
def grupoF():
    return render_template('index.html', datos=pd.DataFrame(cdf['fecha_diagnostico'].value_counts()).to_html())

if __name__ == '__main__':
    app.run(port=8080, debug=True)