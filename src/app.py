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
    oldcresinstall = connect('CREATE VIEW old_cres_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Customer_Type = \'Residential\' AND Year_Installed <= \'2015-12-31\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_cres_installation.municipality, old_cres_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_cres_installation ON emission.Municipality=old_cres_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2015;')
    currcresinstall = connect('CREATE VIEW old_cres_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Customer_Type = \'Residential\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_cres_installation.municipality, old_cres_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_cres_installation ON emission.Municipality=old_cres_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2020;')
    oldccominstall = connect('CREATE VIEW old_cres_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Customer_Type = \'Commercial\' AND Year_Installed <= \'2015-12-31\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_cres_installation.municipality, old_cres_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_cres_installation ON emission.Municipality=old_cres_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2015;')
    currccominstall = connect('CREATE VIEW old_cres_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Customer_Type = \'Commercial\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_cres_installation.municipality, old_cres_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_cres_installation ON emission.Municipality=old_cres_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2020;')
    oldcotherinstall = connect('CREATE VIEW old_cres_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Customer_Type != \'Commercial\' AND Customer_Type != \'Residential\' AND Year_Installed <= \'2015-12-31\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_cres_installation.municipality, old_cres_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_cres_installation ON emission.Municipality=old_cres_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2015;')
    currcotherinstall = connect('CREATE VIEW old_cres_installation AS SELECT Municipality, COUNT(*) AS Installations FROM installation WHERE Customer_Type != \'Commercial\' AND Customer_Type != \'Residential\' AND County = \'' + request.form['county'] + '\'GROUP BY Municipality; SELECT old_cres_installation.municipality, old_cres_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_cres_installation ON emission.Municipality=old_cres_installation.Municipality AND emission.County=\'' + request.form['county'] + '\' AND Year = 2020;')
    heads = ['Municipality', 'Installations','Total MTCO2 Emission']
    headres = ['Municipality', 'Number of Residential Installations']
    headcom = ['Municipality', 'Number of Commercial Installations']
    headother = ['Municipality', 'Number of Other Installations']
    return render_template('my-county-result.html', oldcotherinstall=oldcotherinstall, currcotherinstall=currcotherinstall, oldccominstall=oldccominstall, currccominstall=currccominstall, oldinstallations=oldinstallations, currentinstallations=currentinstallations, oldcresinstall=oldcresinstall, currcresinstall=currcresinstall, heads=heads, headres=headres, headcom=headcom, headother=headother)

# handle venue POST and serve result web page
@app.route('/municipality-handler', methods=['POST'])
def municipality_handler():
    oldinstallations = connect('CREATE VIEW old_mun_installation AS SELECT Municipality, County, COUNT(*) AS Installations FROM installation WHERE Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_mun_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_mun_installation ON emission.Municipality=old_mun_installation.Municipality AND emission.County=old_mun_installation.County AND Year = 2015;')
    currentinstallations = connect('CREATE VIEW old_mun_installation AS SELECT Municipality, County, COUNT(*) AS Installations FROM installation WHERE Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_mun_installation.Installations, emission.TOTAL_MTCO2e FROM emission JOIN old_mun_installation ON emission.Municipality=old_mun_installation.Municipality AND emission.County=old_mun_installation.County AND Year = 2020;')
    oldresinstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type = \'Residential\' AND Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.TOTAL_MTCO2e FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2015;')
    curresinstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type = \'Residential\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.TOTAL_MTCO2e FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2020;')
    oldcominstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type = \'Commercial\'  AND Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.TOTAL_MTCO2e FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2015;')
    curcominstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type = \'Commercial\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.TOTAL_MTCO2e FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2020;')
    oldotherinstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type != \'Residential\' AND Customer_Type != \'Commercial\' AND Year_Installed <= \'2015-12-31\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.TOTAL_MTCO2e FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2015;')
    curotherinstall = connect('CREATE VIEW old_res_installation AS SELECT Municipality, County, COUNT(*) AS num_residential_installations FROM installation WHERE Customer_Type != \'Residential\' AND Customer_Type != \'Commercial\' AND Municipality = \'' + request.form['municipality'] + '\'GROUP BY Municipality, County; SELECT old_res_installation.num_residential_installations, emission.TOTAL_MTCO2e FROM emission JOIN old_res_installation ON emission.Municipality=old_res_installation.Municipality AND emission.County=old_res_installation.County AND Year = 2020;')
    heads = ['Number of Installations', 'Total MTCO2 Emission']
    headres = ['Number of Residential Installations', 'Total MTCO2 Emission']
    headcom = ['Number of Commercial Installations', 'Total MTCO2 Emission']
    headother = ['Number of Other Installations', 'Total MTCO2 Emission']
    return render_template('my-municipality-result.html', curcominstall=curcominstall, oldcominstall=oldcominstall, curotherinstall=curotherinstall, oldotherinstall=oldotherinstall, oldinstallations=oldinstallations, currentinstallations=currentinstallations, oldresinstall=oldresinstall, curresinstall=curresinstall, heads=heads, headres=headres, headcom=headcom, headother=headother)

if __name__ == '__main__':
    app.run(debug = True)
