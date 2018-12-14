#!/usr/bin/env python3
from flask import Flask,render_template,redirect,session,abort,request,flash
import os,pickle,sqlite3
import json
app = Flask(__name__)
app.secret_key = os.urandom(12)
formkeys = ['max_speed','min_alt','max_angle_attack','max_rate_ascend',
        'max_distance_home','low_battery_level','tot_time_flight',
        'drone_category']

datafile = "file.txt"

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template("index.html")
    else:
        return render_template("input.html")

@app.route("/input")
def sinput():
    if not session.get('logged_in'):
        return render_template("index.html")
    else:
        return render_template("input.html")

@app.route("/update")
def go_home():
    return sinput()


@app.route("/dump")
def val_dump():
    conn = sqlite3.connect("dronefield.db")
    cur = conn.cursor()
    cur.execute("select * from dronefield")
    res = cur.fetchall()
    conn.close()
    return json.dumps(res)
# view page actions
@app.route("/view")
def see_view():
    # initiate connection to local db
    if not os.path.isfile("dronefield.db"):
        return "Database does not exist"
    conn = sqlite3.connect("dronefield.db")
    cursor = conn.cursor()

    # check if table exists
    cursor.execute("select name from sqlite_master where type='table' and name='dronefield'")
    results = cursor.fetchall()

    # if not exists
    if len(results) == 0:
        return "Database is empty"
    else:
        # get all fields from dronefield
        cursor.execute('select * from dronefield')
        results = cursor.fetchall()
        conn.close()

        # show results in view template(cpushop.html)
        return render_template("cpushop.html",data=results)


@app.route("/update",methods=['POST'])
def update_data():
    if request.method != "POST":
        flash("ERROR!")
    else:
        # store form entered values in dit
        data = request.form.to_dict()

        # connecto to sqlite3 db
        conn = sqlite3.connect("dronefield.db")
        cursor = conn.cursor()

        # check if table exists or not(if not this is first run)
        cursor.execute("select name from sqlite_master where type='table' and name='dronefield'")
        result = cursor.fetchall()

        # if table doesn't exist,create dronefield table
        if len(result) == 0:
            cquery = ''
            cquery += "create table dronefield ("
            for i in formkeys:
                cquery += i + " integer,"
            cquery = cquery[:-1]
            cquery += ")"
            conn.execute(cquery)
            conn.commit()

        # generate insertion query.

        # check for partial input in form
        query_prestr = "("
        query_postr = "("
        for key,value in data.items():
            if value != '':
                query_prestr += str(key)
                query_prestr += ','

                query_postr += str(request.form[key])
                query_postr += ','

        # trim trailing characters(',update,' and ',submit)
        # (button field event from both query strings)
        query_prestr = query_prestr[:-8]
        query_postr = query_postr[:-8]

        # append trailing ) to both query strings
        query_prestr += ")"
        query_postr += ")"

        # create final query
        query_str = "insert into dronefield"
        query_str += query_prestr + " values" + query_postr

        # execute insertion query.
        conn.execute(query_str)
        conn.commit()
        conn.close()

    # redirect to view page once done
    return see_view()

@app.route("/login",methods=['POST'])
def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash("Wrong password")
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
