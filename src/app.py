#! /usr/bin/python3
import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    rows = []
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
    oldinstallations = connect('CREATE VIEW old_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Year_Installed <= \'2015-12-31\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_installation.municipality, old_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_installation ON emission.Municipality=old_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2015;')
    currentinstallations = connect('CREATE VIEW old_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_installation.municipality, old_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_installation ON emission.Municipality=old_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2020;')
    heads = ['Municipality', 'Installations','Total MTCO2 Emission']
    return render_template('my-county-result.html', oldinstallations=oldinstallations, currentinstallations=currentinstallations, heads=heads)

# handle venue POST and serve result web page
@app.route('/municipality-handler', methods=['POST'])
def municipality_handler():
	oldinstallations = connect('CREATE VIEW old_mun_installation AS SELECT Municipality, County, COUNT(*) AS Installations FROM installation WHERE Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT old_mun_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_mun_installation ON emission.Municipality=old_mun_installation.Municipality AND emission.County=old_mun_installation.County AND Year = 2015;')
	currentinstallations = connect('CREATE VIEW old_mun_installation AS SELECT Municipality, County, COUNT(*) AS Installations FROM installation WHERE Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT old_mun_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_mun_installation ON emission.Municipality=old_mun_installation.Municipality AND emission.County=old_mun_installation.County AND Year = 2020;')

	oldresinstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type = \'Residential\' AND Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.Residential_Electricity, emission.Residential_Natural_Gas FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2015;')
	curresinstall = connect('CREATE VIEW curr_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type = \'Residential\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT curr_res_installation.num_residential_installations, emission.Residential_Electricity, emission.Residential_Natural_Gas FROM emission JOIN curr_res_installation ON emission.Municipality=curr_res_installation.Municipality AND emission.County=curr_res_installation.County AND Year = 2020;')

	oldcomminstall = connect('CREATE VIEW old_comm_installation AS SELECT Municipality, County, COUNT(*) AS num_commercial_installations FROM installation WHERE Customer_Type = \'Commercial\' AND Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT old_comm_installation.num_commercial_installations, emission.Commercial_Electricity, emission.Commercial_Natural_Gas FROM emission JOIN old_comm_installation ON emission.Municipality=old_comm_installation.Municipality AND emission.County=old_comm_installation.County AND Year = 2015;')
	currcomminstall = connect('CREATE VIEW curr_comm_installation AS SELECT Municipality, County, COUNT(*) AS num_commercial_installations FROM installation WHERE Customer_Type = \'Commercial\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT curr_comm_installation.num_commercial_installations, emission.Commercial_Electricity, emission.Commercial_Natural_Gas FROM emission JOIN curr_comm_installation ON emission.Municipality=curr_comm_installation.Municipality AND emission.County=curr_comm_installation.County AND Year = 2020;')

	oldotherinstall = connect('CREATE VIEW old_other_installation AS SELECT Municipality, County, COUNT(*) AS num_other_installations FROM installation WHERE Customer_Type != \'Residential\' AND Customer_Type != \'Commercial\' AND Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT old_other_installation.num_other_installations, emission.Other_Electricity, emission.Other_Gas FROM emission JOIN old_other_installation ON emission.Municipality=old_other_installation.Municipality AND emission.County=old_other_installation.County AND Year = 2015;')
	currotherinstall = connect('CREATE VIEW curr_other_installation AS SELECT Municipality, County, COUNT(*) AS num_other_installations FROM installation WHERE Customer_Type != \'Residential\' AND Customer_Type != \'Commercial\' AND Municipality = \'' + request.form['municipality'] + '\' AND County = \'' + request.form['mun_county'] + '\'GROUP BY Municipality, County; SELECT curr_other_installation.num_other_installations, emission.Other_Electricity, emission.Other_Gas FROM emission JOIN curr_other_installation ON emission.Municipality=curr_other_installation.Municipality AND emission.County=curr_other_installation.County AND Year = 2020;')

	heads = ['Number of Installations', 'Total MTCO2 Emission']
	headres = ['Number of Residential Installations', 'Residential Electricity', 'Residential Natural Gas']
	headcomm = ['Number of Commercial Installations', 'Commercial Electricity', 'Commercial Natural Gas']
	headother = ['Number of Other Installations', 'Other Electricity', 'Other Natural Gas']
	return render_template('my-municipality-result.html', oldinstallations=oldinstallations, currentinstallations=currentinstallations, oldresinstall=oldresinstall, curresinstall=curresinstall, heads=heads, headres=headres, headcomm=headcomm, oldcomminstall=oldcomminstall, currcomminstall=currcomminstall, headother=headother, oldotherinstall=oldotherinstall, currotherinstall=currotherinstall)

if __name__ == '__main__':
    app.run(debug = True)
