from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = './db/names.db'

def query_db(query, args=(), one=False):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute(query, args)
            r = [dict((cur.description[i][0], value) \
                   for i, value in enumerate(row)) for row in cur.fetchall()]
            return (r[0] if r else None) if one else r
    except sqlite3.DatabaseError:
        return None

@app.route('/name/<string:name>', methods=['GET'])
def get_name(name):
    if not name.isalpha():
        return jsonify({"error": "Invalid name format"}), 400

    result = query_db('SELECT * FROM Nombres_permitidos WHERE name=?', [name])

    if not result:
        return jsonify({"error": "Name not found"}), 404
    return jsonify(result)

@app.route('/names/prefix/<string:prefix>', methods=['GET'])
def get_names_by_prefix(prefix):
    if not prefix.isalpha():
        return jsonify({"error": "Invalid prefix format"}), 400

    result = query_db("SELECT * FROM Nombres_permitidos WHERE name LIKE ? LIMIT 100", [prefix + "%"])

    if not result:
        return jsonify({"error": "No names found with the given prefix"}), 404
    return jsonify(result)

@app.route('/names/count/gender', methods=['GET'])
def get_count_by_gender():
    result = query_db("SELECT gender, COUNT(*) as count FROM Nombres_permitidos GROUP BY gender")
    if not result:
        return jsonify({"error": "No data available"}), 404
    return jsonify(result)

@app.route('/names/top', methods=['GET'])
def get_top_names():
    result = query_db("SELECT name, COUNT(*) as count FROM Dataset_nombres GROUP BY name ORDER BY count DESC LIMIT 10")
    if not result:
        return jsonify({"error": "No data available"}), 404
    return jsonify(result)

@app.route('/name/validate', methods=['GET'])
def validate_name():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name is required as a query parameter"}), 400

    parts = name.split()
    response = []
    for part in parts:
        result = query_db('SELECT * FROM Nombres_permitidos WHERE name=?', [part])
        if result:
            response.append({part: 'approved'})
        else:
            response.append({part: 'not approved'})

    return jsonify(response)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='4000')
