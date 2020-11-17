import pandas as pd
from sodapy import Socrata
from flask import Flask, render_template, request, redirect, url_for

cliente = Socrata("www.datos.gov.co", None)
results = cliente.get("gt2j-8ykr")

cdf = pd.DataFrame.from_records(results).fillna(value='No Registra')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', datos=cdf.to_html())

@app.route('/filtrar', methods=['POST'])
def filtrar():
    if request.method == 'POST':
        if request.form['ciudad'] != '':
            return render_template('index.html', datos=cdf[cdf['ciudad_municipio_nom'] == request.form['ciudad']].to_html())
        else:
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8080, debug=True)