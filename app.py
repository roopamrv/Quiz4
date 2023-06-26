import pyodbc
import json
from flask import Flask, render_template, request
import os

app = Flask(__name__)


app.secret_key = 'your secret key'

server = 'mysqlserver-rv.database.windows.net'
username = 'azureuser'
password = 'Mavbgl@656'
database = 'demodb'
driver= '{ODBC Driver 18 for SQL Server}'

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/tmp'
print(dir_path)
UPLOAD_FOLDER = dir_path
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for generating the chart
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Get the user-selected interval or attributes from the form
    time1 = request.form.get('time1')
    time2 = request.form.get('time2')
    selected_attributes = request.form.getlist('attributes')

    # Connect to the database
    conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password+ ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cur = conn.cursor()

    # Execute the SQL query
    query = "SELECT time, latitude, mag, place FROM tableName WHERE time >=  "+time1+" AND time < " +time2
    print(query)
    cur.execute(query)

    # Fetch all rows
    rows = cur.fetchall()

    # Close the cursor and the connection
    cur.close()
    conn.close()

    # Prepare data for the selected attributes
    chart_data = []
    for row in rows:
        data_point = {}
        data_point['time'] = row[0]
        for i, attribute in enumerate(['latitude', 'mag', 'place']):
            if attribute in selected_attributes:
                data_point[attribute] = str(row[i+1])
        print("DATA: ",data_point)
        chart_data.append(data_point)
    print("CHART DATA",chart_data)
    # Render the template with the chart data and selected attributes
    return render_template('piechart.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)

if __name__ == '__main__':
    app.run()
