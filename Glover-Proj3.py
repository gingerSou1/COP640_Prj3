"""
__filename__ = "Glover-Proj3.py"
__coursename__ = "COP-650 Secure Software"
__author__ = "Corey Glover"
__copyright__ = "None"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Corey Glover"
__email__ = "cglover35@student.umgc.edu"

Site hosted off URL for http://localhost:8080/)
"""
import csv
import hashlib

from flask import Flask, render_template, request, session
from datetime import datetime
import socket

app = Flask(__name__)
app.secret_key = 'mydogjarvis'
TIME_NOW = datetime.now()
DATE_TIME = TIME_NOW.strftime("%B %d, %Y, %H:%M:%S")


@app.route('/', methods=['GET', 'POST'])
def login():
    login_error= None
    try:
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']

            with open('users.csv', 'r') as db:
                db_read = csv.reader(db, delimiter=":")
                if user == "" or password == "":
                    login_error = 'Cannot be blank!'
                else:
                    for item in db_read:
                        if item[0] == user and item[1] == password:
                            session['username'] = user
                            session['last_login'] = datetime.now()
                            host = socket.gethostname()
                            IP = socket.gethostbyname(host)
                            userlogs(session['username'], session['last_login'], [IP])
                            return render_template('landing.html', user=session['username'], last_login=session['last_login'])
                        elif user == 'admin' and password == 'admin':
                            session['username'] = user
                            session['last_login'] = datetime.now()
                            host = socket.gethostname()
                            IP = socket.gethostbyname(host)
                            userlogs(session['username'], session['last_login'], [IP])
                            return render_template('admin_landing.html', user=session['username'], last_login=session['last_login'])
                        else:
                            raise IndexError
    except IndexError:
            login_error = 'Please check login credentials ' \
                            'and try again. Attempt has been logged!'

            with open('logFail.csv', 'w', newline='') as logfile:
                host = socket.gethostname()
                IP = socket.gethostbyname(host)
                userData = [['User', 'Date', 'IP Address'],[session['username'], DATE_TIME],[IP]]
                writeLog = csv.writer(logfile)
                writeLog.writerows(userData)
    return render_template('login.html', error=login_error)

def userlogs(user, date, IP):
    """ function to log users"""
    with open('logFail.csv', 'w', newline='') as logfile:
        userData = [['User', 'Date', 'IP Address'], [user, date], [IP]]
        writeLog = csv.writer(logfile)
        writeLog.writerows(userData)

@app.route('/landing')
def page_2():
    """ Function to call second page in HTML"""
    return render_template('landing.html', datetime=DATE_TIME)

@app.route('/admin_landing')
def page_3():
    """ Function to call third page in HTML"""
    return render_template('admin_landing.html', datetime=DATE_TIME)

@app.route('/ICS')
def page_4():
    """ Function to call fourth page in HTML"""
    data = []
    with open('temp_readings.csv', mode='r') as tmps:
        csv_read = csv.DictReader(tmps, delimiter=':')
        for row in csv_read:
            data.append(row)

    headers = data[0].keys() if data else []

    return render_template('ICS.html', datetime=DATE_TIME, data=data, headers=headers)

@app.route('/ICS_Admin')
def page_5():
    """ Function to call fifth page in HTML"""
    data = []
    with open('temp_readings.csv', mode='r') as tmps:
        csv_read = csv.DictReader(tmps, delimiter=':')
        for row in csv_read:
            data.append(row)

    headers = data[0].keys() if data else []

    return render_template('ICS_Admin.html', datetime=DATE_TIME, data=data, headers=headers)

@app.route('/add_data')
def page_6():
    """ Function to call sixth page in HTML"""

    return render_template("/add_data.html")

@app.route('/cloud')
def page_7():
    """ Function to call sixth page in HTML"""

    return render_template("/cloud.html")

@app.route('/About')
def page_8():
    """ Function to call sixth page in HTML"""

    return render_template("/About.html")

if __name__ == '__main__':
    app.run(port=8080, debug=True)