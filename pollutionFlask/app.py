from flask import Flask
from flask import request
import pymysql.cursors
import json

app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='34.69.173.235',
                             user='root',
                             password='CS411-89',
                             database='CS411_Group89_PT1',
                             cursorclass=pymysql.cursors.DictCursor)

def make_where_clause(param_map):
    params = []
    filter = []
    for key, value in param_map.items():
        if value is not None:
            if isinstance(value, int):
                params.append(f"{key} = {value}")
            else:
                if key == 'compound_id':
                    first = 0
                    value_bitshift = int(value)
                    if value_bitshift & 1:
                        filter.append(f"( {key} = 1")
                        first = 1
                    value_bitshift = value_bitshift >> 1
                    if value_bitshift & 1:
                        if first == 0:
                            filter.append(f"( {key} = 2")
                        else:
                            filter.append(f" OR {key} = 2")
                        first = 1
                    value_bitshift = value_bitshift >> 1
                    if value_bitshift & 1:
                        if first == 0:
                            filter.append(f"( {key} = 3")
                        else:
                            filter.append(f" OR {key} = 3")
                        first = 1
                    value_bitshift = value_bitshift >> 1
                    if value_bitshift & 1:
                        if first == 0:
                            filter.append(f"( {key} = 3")
                        else:
                            filter.append(f" OR {key} = 3")
                        first = 1
                    if first:
                        filter.append(f")")
                    filter_where = ' '.join(filter)
                    params.append(filter_where)
                elif key == 'start_date':
                    params.append(f"date >= '{value}'")
                elif key == 'end_date':
                    params.append(f"date <= '{value}'")
                else:
                    params.append(f"{key} = '{value}'")

    query_where = ' AND '.join(params)
    if len(query_where) > 0:
        return f"WHERE {query_where}"
    return ''

@app.route('/')
def backend_entry():
    return "This is one of the backends ever made."


@app.route('/api/state') #@app.route(GET/api/states)
def get_states():  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM State"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result

@app.route('/api/state/<int:state_id>') #@app.route(GET/api/states)
def get_state(state_id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM State WHERE id={state_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result

@app.route('/api/county/') #@app.route(GET/api/states)
def get_counties():  # put application's code here
    state_id = request.args.get('state_id', None)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM County WHERE state_id = {state_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result

@app.route('/api/getdata/')
def get_data():  # put application's code here
    param_map = {
        'compound_id': request.args.get('compound_id', None), # take peramiter strings for one or more pollutants to compare
        'site_id': request.args.get('site_id', None), # return measurements taken at a given site
        'city_id': request.args.get('city_id', None),  # return measurements taken at sites within a city
        'county_id': request.args.get('county_id', None),  # return measurements taken at sites within a county
        'state_id': request.args.get('state_id', None),  # return measurements taken at sites within a state
        'region_id': request.args.get('region_id', None),  # return measurements taken at sites within a region

        'date': request.args.get('date', None), # return measurements taken on a singular date
        'start_date': request.args.get('start_date', None), # return all or only measurements starting from a given date
        'end_date': request.args.get('end_date', None), # return all or only measurements before this given date

    }
    query_where = make_where_clause(param_map)
    #print(query_where)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Measurement {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result

@app.route('/api/state', methods=['POST'])
def add_state():
    temp = request.form
    #request reutrns a dictionary, similar logic to above to parce an insert statement
    return

if __name__ == '__main__':
    app.run(host="0.0.0.0")
