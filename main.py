import os
from flask import Flask, render_template, request, session, url_for, redirect, session, send_from_directory
import pymysql.cursors
import requests, json
from functools import wraps

# Initialize the app from flask
app = Flask(__name__)
app.secret_key = "super secret key"

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='',
                       db='travel',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/<error>')
def login_err(error):
    return render_template('login.html', error=error)


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    role = request.form['role']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cursor = conn.cursor()

    if role == 'customer':
        query = 'SELECT email FROM customer WHERE email = %s and password = %s'
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        cursor.close()
        error = None

        if result is None:
            error = 'Invalid email or password'
            return redirect(url_for('login_err', error=error))
        else:
            cursor = conn.cursor()
            query = 'SELECT email, name, building_num, street, city, state,' \
                    'phone_num, passport_num, passport_exp, passport_country FROM customer WHERE email = %s'
            cursor.execute(query, email)
            result = cursor.fetchone()
            cursor.close()
            session['email'] = result['email']
            session['name'] = result['name']
            session['building_num'] = result['building_num']
            session['street'] = result['street']
            session['city'] = result['city']
            session['state'] = result['state']
            session['phone_num'] = result['phone_num']
            session['passport_num'] = result['passport_num']
            session['passport_exp'] = result['passport_exp']
            session['passport_country'] = result['passport_country']
            session['role'] = role

            return redirect(url_for('home'))

    elif role == 'agent':
        query = 'SELECT email FROM agent WHERE email = %s and password = %s'
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        cursor.close()
        error = None

        if result is None:
            error = 'Invalid email or password'
            return redirect(url_for('login_err', error=error))
        else:
            cursor = conn.cursor()
            query = 'SELECT email, agent_ID, commission, commission_amount FROM agent WHERE email = %s'
            cursor.execute(query, email)
            result = cursor.fetchone()
            cursor.close()
            session['email'] = result['email']
            session['agent_ID'] = result['agent_ID']
            session['commission'] = result['commission']
            session['commission_amount'] = result['commission_amount']
            session['role'] = role

            return redirect(url_for('home'))

    elif role == 'staff':
        query = 'SELECT username FROM staff WHERE username = %s and password = %s'
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        error = None

        if result is None:
            error = 'Invalid username or password'
            return redirect(url_for('login_err', error=error))
        else:
            cursor = conn.cursor()
            query = 'SELECT username, name FROM staff WHERE username = %s'
            cursor.execute(query, username)
            result = cursor.fetchone()
            cursor.close()
            session['username'] = result['username']
            session['role'] = role
            session['name'] = result['name']

            return redirect(url_for('home'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register/<error>')
def register_err(error):
    return render_template('register.html', error=error)


@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    role = request.form['role']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    agent_ID = request.form['agent_ID']
    building_num = request.form['building_num']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_num = request.form['phone_num']
    passport_num = request.form['passport_num']
    passport_exp = request.form['passport_exp']
    passport_country = request.form['passport_country']
    commission = 0
    commission_amount = request.form['commission_amount']
    airline_name = request.form['airline_name']

    if role == 'customer':
        cursor = conn.cursor()
        query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(query, email)
        data = cursor.fetchone()
        cursor.close()
        error = None

        if data:
            error = "This user already exists"
            return redirect(url_for('register_err', error=error))
        else:
            cursor = conn.cursor()
            ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (email, name, password, building_num, street, city, state, phone_num,
                                 passport_num, passport_exp, passport_country))
            conn.commit()
            cursor.close()
            return redirect('/')

    elif role == 'agent':
        cursor = conn.cursor()
        query = 'SELECT * FROM agent WHERE email = %s'
        cursor.execute(query, email)
        data = cursor.fetchone()
        cursor.close()
        error = None

        if data:
            error = "This user already exists"
            return redirect(url_for('register_err', error=error))
        else:
            cursor = conn.cursor()
            ins = 'INSERT INTO agent VALUES(%s, %s, %s, %s, %s)'
            cursor.execute(ins, (email, password, agent_ID, commission, commission_amount))
            conn.commit()
            cursor.close()
            return redirect('/')

    elif role == 'staff':
        cursor = conn.cursor()
        query = 'SELECT * FROM staff WHERE username = %s'
        cursor.execute(query, username)
        data = cursor.fetchone()
        cursor.close()
        error = None

        if data:
            error = "This user already exists"
            return redirect(url_for('register_err', error=error))
        else:
            cursor = conn.cursor()
            ins = 'INSERT INTO staff VALUES(%s, %s, %s)'
            cursor.execute(ins, (username, password, airline_name))
            conn.commit()
            cursor.close()
            return redirect('/')


@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')


@app.route('/logoutStaff')
def logoutStaff():
    session.pop('username')
    return redirect('/')


@app.route('/viewMyFlights')
def viewMyFlights():
    email = session['email']
    role = session['role']

    if role == 'customer':
        cursor = conn.cursor()
        query = 'SELECT ticket_ID, flight_num, depart_date, depart_time FROM customer_purchase NATURAL JOIN ticket ' \
                'WHERE email = %s '
        cursor.execute(query, email)
        results = cursor.fetchall()
        cursor.close()
        return render_template('view_my_flights.html', results=results)

    elif role == 'agent':
        cursor = conn.cursor()
        query = 'SELECT customer, ticket_ID, flight_num, depart_date, depart_time FROM agent_purchase ' \
                'NATURAL JOIN ticket WHERE email = %s'
        cursor.execute(query, email)
        results = cursor.fetchall()
        cursor.close()
        return render_template('view_my_flights_agent.html', results=results)


@app.route('/searchForFlights')
def searchForFlights():
    return render_template('search_for_flights.html')


@app.route('/searchForFlights/<error>')
def searchForFlights_err(error):
    return render_template('search_for_flights.html', error=error)


@app.route('/searchForFlightsAuth', methods=['GET', 'POST'])
def searchForFlightsAuth():
    depart_airport = request.form['depart_airport']
    arrival_airport = request.form['arrival_airport']
    depart_date = request.form['depart_date']

    cursor = conn.cursor()
    query = 'SELECT name, flight_num, depart_date, depart_time FROM flight WHERE depart_airport = %s AND ' \
            'arrival_airport = %s AND depart_date = %s'
    cursor.execute(query, (depart_airport, arrival_airport, depart_date))
    results = cursor.fetchall()
    cursor.close()
    return render_template('view_flights.html', results=results)


@app.route('/searchForFlightsHome')
def searchForFlightsHome():
    return render_template('search_for_flights_home.html')


@app.route('/searchForFlightsHome/<error>')
def searchForFlightsHome_err(error):
    return render_template('search_for_flights_home.html', error=error)


@app.route('/searchForFlightsHomeAuth', methods=['GET', 'POST'])
def searchForFlightsHomeAuth():
    depart_airport = request.form['depart_airport']
    arrival_airport = request.form['arrival_airport']
    depart_date = request.form['depart_date']

    cursor = conn.cursor()
    query = 'SELECT name, flight_num, depart_date, depart_time FROM flight WHERE depart_airport = %s AND ' \
            'arrival_airport = %s AND depart_date = %s'
    cursor.execute(query, (depart_airport, arrival_airport, depart_date))
    results = cursor.fetchall()
    cursor.close()
    return render_template('view_flights_home.html', results=results)


@app.route('/searchForStatus')
def searchForStatus():
    return render_template('search_for_status.html')


@app.route('/searchForStatus/<error>')
def searchForStatus_err(error):
    return render_template('search_for_status.html', error=error)


@app.route('/searchForStatusAuth', methods=['GET', 'POST'])
def searchForStatusAuth():
    name = request.form['name']
    flight_num = request.form['flight_num']
    depart_date = request.form['depart_date']
    arrival_date = request.form['arrival_date']

    cursor = conn.cursor()
    query = 'SELECT status FROM flight WHERE name = %s AND flight_num = %s AND depart_date = %s AND arrival_date = %s'
    cursor.execute(query, (name, flight_num, depart_date, arrival_date))
    results = cursor.fetchall()
    cursor.close()
    return render_template('view_status.html', results=results)


@app.route('/searchForStatusHome')
def searchForStatusHome():
    return render_template('search_for_status_home.html')


@app.route('/searchForStatusHome/<error>')
def searchForStatusHome_err(error):
    return render_template('search_for_status_home.html', error=error)


@app.route('/searchForStatusHomeAuth', methods=['GET', 'POST'])
def searchForStatusHomeAuth():
    name = request.form['name']
    flight_num = request.form['flight_num']
    depart_date = request.form['depart_date']
    arrival_date = request.form['arrival_date']

    cursor = conn.cursor()
    query = 'SELECT status FROM flight WHERE name = %s AND flight_num = %s AND depart_date = %s AND arrival_date = %s'
    cursor.execute(query, (name, flight_num, depart_date, arrival_date))
    results = cursor.fetchall()
    cursor.close()
    return render_template('view_status_home.html', results=results)


@app.route('/purchaseTickets')
def purchaseTickets():
    return render_template('purchase_tickets.html')


@app.route('/purchaseTickets/<error>')
def purchaseTickets_err(error):
    return render_template('purchase_tickets.html', error=error)


@app.route('/purchaseTicketsAuth', methods=['GET', 'POST'])
def purchaseTicketsAuth():
    email = session['email']
    name = request.form['name']
    flight_num = request.form['flight_num']
    depart_date = request.form['depart_date']
    depart_time = request.form['depart_time']
    date_purchased = request.form['date_purchased']

    cursor = conn.cursor()
    query = 'SELECT ticket_ID FROM ticket WHERE name = %s AND flight_num = %s AND depart_date = %s AND depart_time = %s'
    cursor.execute(query, (name, flight_num, depart_date, depart_time))
    results = cursor.fetchall()
    cursor.close()

    if results:
        for i in results:
            ticket_ID = i['ticket_ID']
    else:
        error = "There is an error, check the name, flight_num, depart_date, and depart_time"
        return redirect(url_for('purchaseTickets_err', error=error))

    cursor = conn.cursor()
    ins = 'INSERT INTO customer_purchase VALUES (%s, %s, %s)'
    cursor.execute(ins, (ticket_ID, email, date_purchased))
    conn.commit()
    cursor.close()

    return redirect(url_for('home'))


@app.route('/purchaseTicketsAgent')
def purchaseTicketsAgent():
    return render_template('purchase_tickets_agent.html')


@app.route('/purchaseTicketsAgent/<error>')
def purchaseTicketsAgent_err(error):
    return render_template('purchase_tickets_agent.html', error=error)


@app.route('/purchaseTicketsAgentAuth', methods=['GET', 'POST'])
def purchaseTicketsAgentAuth():
    email = session['email']
    customer = request.form['customer']
    name = request.form['name']
    flight_num = request.form['flight_num']
    depart_date = request.form['depart_date']
    depart_time = request.form['depart_time']
    date_purchased = request.form['date_purchased']
    commission_amount = request.form['commission_amount']

    cursor = conn.cursor()
    query = 'SELECT ticket_ID FROM ticket WHERE name = %s AND flight_num = %s AND depart_date = %s AND depart_time = %s'
    cursor.execute(query, (name, flight_num, depart_date, depart_time))
    results = cursor.fetchall()
    cursor.close()

    if results:
        for i in results:
            ticket_ID = i['ticket_ID']
    else:
        error = "There is an error, check the name, flight_num, depart_date, and depart_time"
        return redirect(url_for('purchaseTicketsAgentAuth_err', error=error))

    cursor = conn.cursor()
    ins = 'INSERT INTO agent_purchase VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(ins, (ticket_ID, email, customer, date_purchased, commission_amount))
    conn.commit()
    cursor.close()

    return redirect(url_for('home'))


@app.route('/giveRatings')
def giveRatings():
    return render_template('give_ratings.html')


@app.route('/giveRatings/<error>')
def giveRatings_err(error):
    return render_template('give_ratings.html', error=error)


@app.route('/giveRatingsAuth', methods=['GET', 'POST'])
def giveRatingsAuth():
    email = session['email']
    ticket_ID = request.form['ticket_ID']
    comments = request.form['comments']
    rating = request.form['rating']

    cursor = conn.cursor()
    query = 'SELECT name, flight_num FROM customer_purchase NATURAL JOIN ticket WHERE email = %s AND ticket_ID = %s'
    cursor.execute(query, (email, ticket_ID))
    results = cursor.fetchall()
    cursor.close()

    if results:
        for i in results:
            name = i['name']
            flight_num = i['flight_num']

    cursor = conn.cursor()
    ins = 'INSERT INTO comment_rate VALUES (%s, %s, %s, %s)'
    cursor.execute(ins, (name, flight_num, comments, rating))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/trackSpending')
def trackSpending():
    return render_template('track_spending.html')


@app.route('/trackSpending/<error>')
def trackSpending_err(error):
    return render_template('track_spending.html', error=error)


@app.route('/trackSpendingAuth', methods=['GET', 'POST'])
def trackSpendingAuth():
    email = session['email']
    within = int(request.form['within'])
    labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    values = []
    values2 = []

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 1 month) AND (now() - interval 0 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 2 month) AND (now() - interval 1 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 3 month) AND (now() - interval 2 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 4 month) AND (now() - interval 3 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 5 month) AND (now() - interval 4 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 6 month) AND (now() - interval 5 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 7 month) AND (now() - interval 6 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 8 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 8 month) AND (now() - interval 7 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 9 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 9 month) AND (now() - interval 8 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 10 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 10 month) AND (now() - interval 9 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 11 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 11 month) AND (now() - interval 10 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 12 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 12 month) AND (now() - interval 11 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 13 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased BETWEEN (now() - interval 13 month) AND (now() - interval 12 month)'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0

    values.append(temp)

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 1 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 2 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 3 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 4 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 5 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 6 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 7 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 8 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 8 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 9 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 9 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 10 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 10 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 11 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 11 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 12 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 12 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    # 13 month
    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE email = %s AND date_purchased >= now() - interval 13 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['price'] != 'NULL':
                temp = k['price']
            else:
                temp = 0
    values2.append(temp)

    f_labels = []
    f_values = []

    for i in range(0, within):
        f_labels.append(labels[i])
        f_values.append(values[i])

    f_values2 = values2[within]

    return render_template('view_spending.html', title="Money spent", max=17000,
                           within=within, f_labels=f_labels, f_values=f_values, f_values2=f_values2)


@app.route('/viewMyCommission')
def viewMyCommission():
    return render_template('view_my_commission.html')


@app.route('/viewMyCommission/<error>')
def viewMyCommission_err(error):
    return render_template('view_my_commission.html', error=error)


@app.route('/viewMyCommissionAuth', methods=['GET', 'POST'])
def viewMyCommissionAuth():
    email = session['email']
    within = int(request.form['within'])
    values1 = []
    values2 = []
    values3 = []

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 1 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 2 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 3 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 4 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 5 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 6 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 7 month'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values1.append(temp)

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 1 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 2 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 3 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 4 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 5 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 6 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT AVG(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 7 month'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values2.append(temp)

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 1 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 2 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 3 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 4 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 5 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 6 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 7 month'
    cursor.execute(query, email)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['amount'] != 'NULL':
                temp = k['amount']
            else:
                temp = 0
    values3.append(temp)

    f_values1 = values1[within]
    f_values2 = values2[within]
    f_values3 = values3[within]

    return render_template('view_my_commission_res.html', f_values1=f_values1, f_values2=f_values2,
                           f_values3=f_values3, within=within)


@app.route('/viewTopCustomers')
def viewTopCustomers():
    email = session['email']
    label1 = []
    label2 = []
    value1 = []
    value2 = []

    cursor = conn.cursor()
    query = 'SELECT customer, count(*) AS number FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 6 month GROUP BY customer ORDER BY number DESC LIMIT 5'
    cursor.execute(query, email)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for i in result1:
            label1.append(i['customer'])
            value1.append(i['number'])

    cursor = conn.cursor()
    query = 'SELECT customer, SUM(commission_amount) AS amount FROM agent_purchase WHERE email = %s AND ' \
            'date_purchased >= now() - interval 12 month GROUP BY customer ORDER BY amount DESC LIMIT 5'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for i in result2:
            label2.append(i['customer'])
            value2.append(i['amount'])

    return render_template('view_top_customers.html', label1=label1, label2=label2, value1=value1, value2=value2)


@app.route('/viewFlights')
def viewFlights():
    return render_template('view_flights_staff.html')


@app.route('/viewFlights/<error>')
def viewFlights_err(error):
    return render_template('view_flights_staff.html', error=error)


@app.route('/viewFlightsAuth', methods=['GET', 'POST'])
def viewFlightsAuth():
    name = session['name']
    depart_airport = request.form['depart_airport']
    depart_date = request.form['depart_date']

    cursor = conn.cursor()
    query = 'SELECT flight_num, depart_date, depart_time FROM flight WHERE depart_airport = %s AND ' \
            'depart_date = %s AND name = %s'
    cursor.execute(query, (depart_airport, depart_date, name))
    results = cursor.fetchall()
    cursor.close()

    return render_template('view_flights_staff_res.html', results=results)


@app.route('/viewCustomersFlight')
def viewCustomersFlight():
    return render_template('view_customers_flight.html')


@app.route('/viewCustomersFlight/<error>')
def viewCustomersFlight_err(error):
    return render_template('view_customers_flight.html', error=error)


@app.route('/viewCustomersFlightAuth', methods=['GET', 'POST'])
def viewCustomersFlightAuth():
    flight_num = request.form['flight_num']
    name = session['name']

    cursor = conn.cursor()
    query = 'SELECT email FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE ' \
            'flight_num = %s AND name = %s'
    cursor.execute(query, (flight_num, name))
    result1 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT customer from agent_purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE ' \
            'flight_num = %s AND name = %s'
    cursor.execute(query, (flight_num, name))
    result2 = cursor.fetchall()
    cursor.close()

    return render_template('view_customers_flight_res.html', result1=result1, result2=result2)


@app.route('/createNewFlights')
def createNewFlights():
    return render_template('create_new_flights.html')


@app.route('/createNewFlights/<error>')
def createNewFlights_err(error):
    return render_template('create_new_flights.html', error=error)


@app.route('/createNewFlightsAuth', methods=['GET', 'POST'])
def createNewFlightsAuth():
    name = session['name']
    flight_num = request.form['flight_num']
    depart_date = request.form['depart_date']
    depart_time = request.form['depart_time']
    arrival_date = request.form['arrival_date']
    arrival_time = request.form['arrival_time']
    base_price = request.form['base_price']
    status = request.form['status']
    depart_airport = request.form['depart_airport']
    arrival_airport = request.form['arrival_airport']
    ticket_ID = request.form['ticket_ID']

    cursor = conn.cursor()
    ins = 'INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (name, flight_num, depart_date, depart_time, arrival_date, arrival_time, base_price, status,
                         depart_airport, arrival_airport))
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    ins = 'INSERT INTO ticket VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(ins, (ticket_ID, name, flight_num, depart_date, depart_time))
    conn.commit()
    cursor.close()

    return redirect(url_for('home'))


@app.route('/changeStatus')
def changeStatus():
    return render_template('change_status.html')


@app.route('/changeStatus/<error>')
def changeStatus_err(error):
    return render_template('change_status.html', error=error)


@app.route('/changeStatusAuth', methods=['GET', 'POST'])
def changeStatusAuth():
    flight_num = request.form['flight_num']
    status = request.form['status']

    cursor = conn.cursor()
    update = 'UPDATE flight SET status = %s WHERE flight_num = %s'
    cursor.execute(update, (status, flight_num))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/addAirplane')
def addAirplane():
    return render_template('add_airplane.html')


@app.route('/addAirplane/<error>')
def addAirplane_err(error):
    return render_template('add_airplane.html', error=error)


@app.route('/addAirplaneAuth', methods=['GET', 'POST'])
def addAirplaneAuth():
    name = session['name']
    ID = request.form['ID']
    seats = request.form['seats']

    cursor = conn.cursor()
    ins = 'INSERT INTO airplane VALUES (%s, %s, %s)'
    cursor.execute(ins, (name, ID, seats))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/addAirport')
def addAirport():
    return render_template('add_airport.html')


@app.route('/addAirport/<error>')
def addAirport_err(error):
    return render_template('add_airport.html', error=error)


@app.route('/addAirportAuth', methods=['GET', 'POST'])
def addAirportAuth():
    airport_name = request.form['airport_name']
    city = request.form['city']

    cursor = conn.cursor()
    ins = 'INSERT INTO airport VALUES (%s, %s)'
    cursor.execute(ins, (airport_name, city))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/viewFlightRatings')
def viewFlightRatings():
    return render_template('view_flight_ratings.html')


@app.route('/viewFlightRatings/<error>')
def viewFlightRatings_err(error):
    return render_template('view_flight_ratings.html', error=error)


@app.route('/viewFlightRatingsAuth', methods=['GET', 'POST'])
def viewFlightRatingsAuth():
    flight_num = request.form['flight_num']

    cursor = conn.cursor()
    query = 'SELECT rating, comments FROM comment_rate WHERE flight_num = %s'
    cursor.execute(query, flight_num)
    results = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT AVG(rating) as avg_rating FROM comment_rate WHERE flight_num = %s'
    cursor.execute(query, flight_num)
    results2 = cursor.fetchall()
    cursor.close()

    return render_template('view_ratings.html', results=results, results2=results2)


@app.route('/viewBookingAgents')
def viewBookingAgents():
    cursor = conn.cursor()
    query = 'SELECT email, count(*) FROM agent_purchase WHERE date_purchased >= now() - interval 1 month ' \
            'GROUP BY email ORDER BY `count(*)` DESC LIMIT 5'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT email, count(*) FROM agent_purchase WHERE date_purchased >= now() - interval 12 month ' \
            'GROUP BY email ORDER BY `count(*)` DESC LIMIT 5'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT email, sum(commission_amount) AS amount FROM agent_purchase GROUP BY email ' \
            'ORDER BY amount DESC LIMIT 5'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    return render_template('view_booking_agents.html', result1=result1, result2=result2, result3=result3)


@app.route('/viewFrequentCustomers')
def viewFrequentCustomers():
    return render_template('view_frequent_customers.html')


@app.route('/viewFrequentCustomers/<error>')
def viewFrequentCustomers_err(error):
    return render_template('view_frequent_customers.html', error=error)


@app.route('/viewFrequentCustomersAuth', methods=['GET', 'POST'])
def viewFrequentCustomersAuth():
    email = request.form['email']

    cursor = conn.cursor()
    query = 'SELECT email, count(email) FROM customer_purchase NATURAL JOIN ticket ' \
            'WHERE depart_date >= now() - interval 12 month GROUP BY email ORDER BY count(email) DESC LIMIT 1'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT ticket_ID, flight_num, depart_date, depart_time FROM customer_purchase NATURAL JOIN ticket ' \
            'NATURAL JOIN staff WHERE email = %s'
    cursor.execute(query, email)
    result2 = cursor.fetchall()
    cursor.close()

    return render_template('view_frequent_customers_res.html', result1=result1, result2=result2)


@app.route('/viewReports')
def viewReports():
    return render_template('view_reports.html')


@app.route('/viewReports/<error>')
def viewReports_err(error):
    return render_template('view_reports.html', error=error)


@app.route('/viewReportsAuth', methods=['GET', 'POST'])
def viewReportsAuth():
    within = int(request.form['within'])
    labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    values1 = []  # month by month sold customer_purchase
    values2 = []  # month by month sold agent_purchase
    values3 = []  # up to sold customer_purchase
    values4 = []  # up to sold agent_purchase

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 1 month) ' \
            'AND (now() - interval 0 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 2 month) ' \
            'AND (now() - interval 1 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 3 month) ' \
            'AND (now() - interval 2 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 4 month) ' \
            'AND (now() - interval 3 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 5 month) ' \
            'AND (now() - interval 4 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 6 month) ' \
            'AND (now() - interval 5 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 7 month) ' \
            'AND (now() - interval 6 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 8 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 8 month) ' \
            'AND (now() - interval 7 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 9 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased BETWEEN (now() - interval 9 month) ' \
            'AND (now() - interval 8 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 10 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 10 month) AND (now() - interval 9 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 11 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 11 month) AND (now() - interval 10 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 12 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 12 month) AND (now() - interval 11 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 13 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 13 month) AND (now() - interval 12 month)'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values1.append(temp)

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 1 month) AND (now() - interval 0 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 2 month) AND (now() - interval 1 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 3 month) AND (now() - interval 2 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 4 month) AND (now() - interval 3 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 5 month) AND (now() - interval 4 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 6 month) AND (now() - interval 5 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 7 month) AND (now() - interval 6 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 8 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 8 month) AND (now() - interval 7 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 9 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 9 month) AND (now() - interval 8 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 10 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 10 month) AND (now() - interval 9 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 11 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 11 month) AND (now() - interval 10 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 12 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 12 month) AND (now() - interval 11 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 13 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased ' \
            'BETWEEN (now() - interval 13 month) AND (now() - interval 12 month)'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values2.append(temp)

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 1 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 2 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 3 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 4 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 5 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 6 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 7 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 8 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 8 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 9 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 9 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 10 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 10 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 11 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 11 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 12 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 12 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 13 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM customer_purchase WHERE date_purchased >= now() - interval 13 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values3.append(temp)

    # 1 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 1 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 2 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 2 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 3 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 3 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 4 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 4 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 5 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 5 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 6 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 6 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 7 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 7 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 8 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 8 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 9 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 9 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 10 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 10 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 11 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 11 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 12 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 12 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    # 13 month
    cursor = conn.cursor()
    query = 'SELECT count(*) AS count FROM agent_purchase WHERE date_purchased >= now() - interval 13 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            if k['count'] != 'NULL':
                temp = k['count']
            else:
                temp = 0

    values4.append(temp)

    f_labels = []
    f_values1 = []
    f_values2 = []

    for i in range(0, within):
        f_labels.append(labels[i])
        f_values1.append(values1[i])
        f_values2.append(values2[i])

    f_values3 = values3[within]
    f_values4 = values4[within]

    return render_template('view_reports_res.html', f_labels=f_labels, f_values1=f_values1, f_values2=f_values2,
                           f_values3=f_values3, f_values4=f_values4)


@app.route('/compareRevenue')
def compareRevenue():
    labels = ['customer', 'agent']
    values1 = []
    values2 = []

    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE date_purchased >= now() - interval 1 month'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    if result1:
        for k in result1:
            temp = k['price']
    values1.append(temp)

    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE date_purchased >= now() - interval 12 month'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    if result2:
        for k in result2:
            temp = k['price']
    values2.append(temp)

    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM agent_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE date_purchased >= now() - interval 1 month'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    if result3:
        for k in result3:
            temp = k['price']
    values1.append(temp)

    cursor = conn.cursor()
    query = 'SELECT SUM(base_price) AS price FROM agent_purchase NATURAL JOIN ticket NATURAL JOIN flight ' \
            'WHERE date_purchased >= now() - interval 12 month'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    if result4:
        for k in result4:
            temp = k['price']
    values2.append(temp)

    return render_template('view_compare_revenue.html', labels=labels, values1=values1, values2=values2)


@app.route('/viewTopDestinations')
def viewTopDestinations():
    cursor = conn.cursor()
    query = 'SELECT arrival_airport, count(*) FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN FLIGHT ' \
            'WHERE arrival_date >= now() - interval 3 month GROUP BY arrival_airport ORDER BY count(*) DESC LIMIT 3'
    cursor.execute(query)
    result1 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT arrival_airport, count(*) FROM agent_purchase NATURAL JOIN ticket NATURAL JOIN FLIGHT ' \
            'WHERE arrival_date >= now() - interval 3 month GROUP BY arrival_airport ORDER BY count(*) DESC LIMIT 3'
    cursor.execute(query)
    result2 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT arrival_airport, count(*) FROM customer_purchase NATURAL JOIN ticket NATURAL JOIN FLIGHT ' \
            'WHERE arrival_date >= now() - interval 12 month GROUP BY arrival_airport ORDER BY count(*) DESC LIMIT 3'
    cursor.execute(query)
    result3 = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT arrival_airport, count(*) FROM agent_purchase NATURAL JOIN ticket NATURAL JOIN FLIGHT ' \
            'WHERE arrival_date >= now() - interval 12 month GROUP BY arrival_airport ORDER BY count(*) DESC LIMIT 3'
    cursor.execute(query)
    result4 = cursor.fetchall()
    cursor.close()

    return render_template('view_top_destinations.html', result1=result1, result2=result2,
                           result3=result3, result4=result4)


# http://127.0.0.1:5000
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
