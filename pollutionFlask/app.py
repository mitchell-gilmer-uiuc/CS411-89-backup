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
    parce = []
    for key, value in param_map.items():
        if value is not None:
            csv = value.split(",")
            if key == 'start_date':
                params.append(f"date >= '{value}'")
            elif key == 'end_date':
                params.append(f"date <= '{value}'")
            else:
                if len(csv) == 1:
                    params.append(f"{key} <= '{value}'")
                else:
                    for i in range(len(csv)):
                        if i == 0:
                            parce.append(f"({key} = '{csv[i]}'")
                        elif i == (len(csv)-1):
                            parce.append(f" OR {key} = '{csv[i]}')")
                        else:
                            parce.append(f" OR {key} = '{csv[i]}'")
                    condition = ' '.join(parce)
                    params.append(condition)
    query_where = ' AND '.join(params)
    if len(query_where) > 0:
        return f"WHERE {query_where}"
    return ''


@app.route('/')
def backend_entry():
    return "This is one of the backends ever made."


# get all of everything

@app.route('/api/site')  # @app.route(GET/api/states)
def get_sites():  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM Site"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/city')  # @app.route(GET/api/states)
def get_cities():  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM City"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/county')  # @app.route(GET/api/states)
def get_counties():  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM County"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/state')  # @app.route(GET/api/states)
def get_states():  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM State"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result

# get single entries by ID


@app.route('/api/state/<int:id>')
def get_state(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM State WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/state/<int:id>')
def get_county(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM County WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/state/<int:id>')
def get_city(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM City WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/state/<int:id>')
def get_site(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Site WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/getdata/')
def get_data():  # put application's code here
    param_map = {
        'compound_id': request.args.get('compound_id', None),
        'site_id': request.args.get('site_id', None),  # return measurements taken at a given site
        'date': request.args.get('date', None),  # return measurements taken on a singular date
        'start_date': request.args.get('start_date', None),
        'end_date': request.args.get('end_date', None),  # return all or only measurements before this given date
    }
    query_where = make_where_clause(param_map)
    # print(query_where)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Measurement {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


# add an entry

@app.route('/api/site/', methods=['POST'])
def add_site():
    address = request.form.get("address", None)
    city_id = request.form.get("city_id", None)
    if address is None or city_id is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        # verify site does not already exist
        sql = f"SELECT * FROM Site WHERE city_id = {city_id} and address = '{address}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            # return site_id
            return "A site in that city with that address already exists with ID ___", 200
        else:
            # verify the target city exists
            sql = f"SELECT * FROM City WHERE id = {city_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return "Bad request, invalid city_id"
            else:
                sql = f"INSERT INTO Site(city_id, address) VALUES({city_id}, '{address}')"
                cursor.execute(sql)
                sql = f"SELECT * FROM Site WHERE city_id = city_id and address = '{address}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result, 201


@app.route('/api/city/', methods=['POST'])
def add_city():
    name = request.form.get("name", None)
    county_id = request.form.get("county_id", None)
    if name is None or county_id is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        # verify the city does not exist already
        sql = f"SELECT * FROM City WHERE county_id = {county_id} and name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            # return site_id
            return "A city in that county with that address already exists with ID ___", 200
        else:
            # verify the county is valid
            sql = f"SELECT * FROM County WHERE id = {county_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return "Bad request, invalid county_id"
            else:
                # preform the add
                sql = f"INSERT INTO City(county_id, name) VALUES({county_id}, '{name}')"
                cursor.execute(sql)
                sql = f"SELECT * FROM City WHERE county_id = county_id and name = '{name}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result, 201


@app.route('/api/county/', methods=['POST'])
def add_county():
    name = request.form.get("name", None)
    state_id = request.form.get("state_id", None)
    if name is None or state_id is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM County WHERE state_id = {state_id} and name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            # return site_id
            "A county in that state with that name already exists with ID ___", 200
        else:
            sql = f"SELECT * FROM State WHERE id = {state_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return "Bad request, invalid state_id"
            else:
                sql = f"INSERT INTO County(state_id, name) VALUES({state_id}, '{name}')"
                cursor.execute(sql)
                sql = f"SELECT * FROM County WHERE state_id = state_id and name = '{name}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result, 201


@app.route('/api/state', methods=['POST'])
def add_state():
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM State WHERE name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = f"INSERT INTO State(name) VALUES ('{name}')"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            sql = f"SELECT * FROM State WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return result, 201
        else:
            return "State already exists", 400


@app.route('/api/getdata/', methods=['POST'])
def add_measurement():
    site_id = request.form.get("site_id", None)
    compound_id = request.form.get("compound_id", None)
    date = request.form.get("date", None)
    parts_per = request.form.get("parts_per", None)
    mean = request.form.get("mean", None)
    max_value = request.form.get("max_value", None)
    max_hour = request.form.get("max_hour", None)
    aqi = request.form.get("aqi", None)

    if site_id is None or compound_id is None or date is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Site WHERE id = {site_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Invalid site", 400
        sql = f"SELECT * FROM Compound WHERE id = {compound_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Invalid compound", 400
        sql = (f"INSERT INTO Measurement(site_id, compound_id, date, parts_per, mean, max_value, max_hour, aqi) "
               f"VALUES ('{site_id}, {compound_id}, '{date}', {parts_per}, {mean}, {max_value}, {max_hour}, {aqi} ')")
        cursor.execute(sql)
        # sql = f"SELECT * FROM Measurement WHERE name = '{name}'"
        # cursor.execute(sql)
        # result = cursor.fetchall()
        # print(result)
        connection.commit()
        return "Entry added", 201


# delete an entry

@app.route('/api/site/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Site WHERE id = {site_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM Site WHERE id = {site_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/city/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM City WHERE id = {city_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM City WHERE id = {city_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/county/<int:county_id>', methods=['DELETE'])
def delete_county(county_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM County WHERE id = {county_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM County WHERE id = {county_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/state/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM State WHERE id = {state_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM State WHERE id = {state_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/measurement/<int:measurement_id>', methods=['DELETE'])
def delete_measurement(measurement_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Measurement WHERE id = {measurement_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM Measurement WHERE id = {measurement_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200

# patch everything

@app.route('/api/state/<int:state_id>', methods=['PATCH'])
def patch_state(state_id):
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM State WHERE id = {state_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE State SET name = '{name}' WHERE id = {state_id}"
            cursor.execute(sql)
            sql = f"SELECT * FROM State WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result, 201


if __name__ == '__main__':
    app.run(host="0.0.0.0")
