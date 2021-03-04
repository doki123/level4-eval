from flask import *
from flask_pymongo import PyMongo

# TODO: Update flight timings, delete flights, publish to Heroku, screenshot update route code and send to teacher
app = Flask('Airport')
app.config['MONGO_URI'] = \
    "mongodb+srv://Shruti:bfy6SeOsMbF02Ffp@cluster0-l0gvf.mongodb.net/Shruti_Dats?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'airport'
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect('/')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        print(request.form)
        doc = {'name': request.form['flight_name'], 'airline': request.form['airline'],
               'date': request.form['flight_date'], 'capacity': request.form['capacity'],
               'price': request.form['price']}
        mongo.db.flight_register.insert_one(doc)
        return redirect('/add')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        print(request.form)
        old = mongo.db.flight_register.find_one({'airline': request.form['airline'], 'name': request.form['flight_name']})
        old_book = mongo.db.booked_flights.find_one({'airline': request.form['airline'], 'name': request.form['flight_name']})
        print('Old Register:', old)
        print('Old Booked:', old_book)
        mongo.db.flight_register.update_one({'_id': old['_id']}, {'$set': {'date': request.form['flight_date']}})
        mongo.db.booked_flights.update_one({'_id': old_book['_id']}, {'$set': {'date': request.form['flight_date']}})
        new = mongo.db.flight_register.find_one({'airline': request.form['airline'], 'name': request.form['flight_name']})
        new_book = mongo.db.booked_flights.find_one({'airline': request.form['airline'], 'name': request.form['flight_name']})
        print('New Register:', new)
        print('New Booked:', new_book)
        return redirect('/update')


@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        flights = mongo.db.flight_register.find()
        return render_template('book.html', flights=flights)
    else:
        print(request.form)
        doc = {'name': request.form['flight_name'], 'airline': request.form['airline'],
               'date': request.form['flight_date'], 'seats': request.form['seats'],
               'price': request.form['price']}
        print(doc)
        mongo.db.booked_flights.insert_one(doc)
        return redirect('/book')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        booked_flights = mongo.db.booked_flights.find()
        return render_template('checkout.html', booked_flights=booked_flights)
    else:
        mongo.db.booked_flights.remove({})
        return redirect('/')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('checkout.html')
    else:
        print(request.form)
        delete_flight = mongo.db.booked_flights.find_one({'name': request.form['name'],
                                                          'airline': request.form['airline'],
                                                          'date': request.form['date'],
                                                          'seats': request.form['seats']})
        mongo.db.booked_flights.remove(delete_flight)
        return redirect('/checkout')


app.run(debug=True)
