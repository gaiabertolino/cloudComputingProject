from cgi import FieldStorage
import shutil
from flask import Flask, render_template, redirect, request
import sqlite3
import sqlite3
import init_db
#import main
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)
init_db.init()

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':

        # Saving the file
        path = str(os.getcwd() + "\\" + request.files['file'].filename)
        request.files['file'].save(path)

        # Verification of data
        if request.files['file'].filename.endswith('.csv'):

            # Saving in the database
            connection = sqlite3.connect('database.db')
            connection.row_factory = sqlite3.Row
            connection.execute('INSERT INTO requests (FileName, Mail, Algorithm) VALUES (?,?,?)', 
                    (request.files['file'].filename, request.form['mail'], request.form['algorithm']))
            connection.commit()
            connection.close()

            url = r'http://request:5000'
            with open(path, 'rb') as f:
                r = requests.post(url, files={'file': f}, data = {'algorithm': request.form['algorithm'], 'mail': request.form['mail']})

            return redirect('/history')
    return render_template('index.html')


@app.route('/history')
def history():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    requests = connection.execute('SELECT * FROM requests').fetchall()
    connection.close()
    return render_template('history.html', requests=requests)

@app.route('/<int:idx>/delete', methods=('POST',))
def delete(idx):
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    requests = connection.execute('DELETE FROM requests WHERE id=?', (idx,))
    connection.commit()
    connection.close()
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
