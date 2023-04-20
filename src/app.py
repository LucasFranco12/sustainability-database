#! /usr/bin/python3
import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('my-form.html')

# handle venue POST and serve result web page
@app.route('/county-handler', methods=['POST'])
def venue_handler():
    rows = connect('SELECT venue_id, title FROM events WHERE venue_id = ' + request.form['venue_id'] + ';')
    heads = ['venue_id', 'title']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/municipality-handler', methods=['POST'])
def municipality_handler():
	installations = connect('SELECT COUNT (*) AS num_installations FROM installation WHERE Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\';')
	emission = connect('SELECT TOTAL_MTCO2e AS Total_CO2_2015 FROM emission WHERE Year = 2015 AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\';')
	heads = ['Number of Installations', 'Total MTCO2 Emission']
	row = [installations,emission]
	return render_template('my-result.html', row=row, heads=heads)

if __name__ == '__main__':
    app.run(debug = True)
