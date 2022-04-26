from itertools import product
from flask import (
    Flask, request, render_template, session, flash, redirect, url_for, jsonify
)

from db import db_connection


app = Flask(__name__)
app.secret_key = 'THISISMYSECRETKEY'  # create the unique one for yourself

@app.route('/registration', methods = ['GET','POST'])
#function for registration
def registration():
    if request.method == 'POST':
     name = request.form ['name']   
     username = request.form['username']
     password = request.form['password']
     email = request.form['email']
     address = request.form['address']
     phone = request.form['phone']
     
     conn = db_connection() #connecting to the database
     cur = conn.cursor() 
     register = (""" INSERT INTO users (username,name,password,email,address,phone) VALUES ('%s','%s','%s','%s','%s','%s')""" % (username,name,password,email,address,phone))
     cur.execute("SELECT * FROM users WHERE username = %(username)s", {'username':username})
     check = cur.fetchone()
     error = ""
     #check if username already exists
     if check :
       error = "You can't use this username because this username is taken"
     else:
         cur.execute(registration)
     flash(error)
     conn.commit()
     cur.close()
     conn.close()

    return render_template ('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ function to show and process login page """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = db_connection()
        cur = conn.cursor()
        sql = """
            SELECT userId, username
            FROM users
            WHERE username = '%s' AND password = '%s'
        """ % (username, password)
        cur.execute(sql)
        user = cur.fetchone()

        error = ''
        if user is None:
            error = 'Wrong credentials. No user found'
        else:
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))

        flash(error)
        cur.close()
        conn.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    """ function to do logout """
    session.clear()  # clear all sessions
    return redirect(url_for('login'))


@app.route('/home')
def index():
    conn = db_connection()
    cur = conn.cursor()
    sql = """
        SELECT products.productId, products.productName, products.description
        FROM products
        ORDER BY products.productId
    """
    cur.execute(sql)
    # [(1, "Article Title 1", "Art 1 content"), (2, "Title2", "Content 2"), ...]
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=products)


@app.route('/product/create', methods=['GET', 'POST'])
def create():
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json() or {}
        # check existence of name and description
        if data.get('productName') and data.get('price'):
            productName = data.get('productName', '')
            price = data.get('price', '')
            description = data.get('description', '')
            image = data.get('image', '')
            stock = data.get('stock', '')
            categoryId = data.get('categoryId', '')
            userId = session.get('userId')

            # strip() is to remove excessive whitespaces before saving
            productName = productName.strip()
            description = description.strip()
            price = price.strip()
            image = image.strip()
            stock = stock.strip()
            categoryId = categoryId.strip()

            conn = db_connection()
            cur = conn.cursor()
            # insert with the userId

            sql = """
                INSERT INTO product (productName, price, description, userId, image, stock, categoryId) VALUES ('%s', %d', '%s', '%d', '%s', '%d', '%d')
            """ % (productName, price, description, userId, image, stock, categoryId)
            cur.execute(sql)
            conn.commit()  # commit to make sure changes are saved
            cur.close()
            conn.close()
            # an example with redirect
            return jsonify({'status': 200, 'message': 'Success', 'redirect': '/'})



        # else will be error
        return jsonify({'status': 500, 'message': 'No Data submitted'})

    return render_template('create.html')


@app.route('/product/<int:productId>', methods=['GET'])
def read(productId):
    # find the products with id = productId, return not found page if error
    conn = db_connection()
    cur = conn.cursor()
    sql = """
        SELECT products.productName, products.productId, users.name
        FROM products 
        JOIN users ON users.userId = products.userId
        WHERE products.userId = %d
    """ % productId
    cur.execute(sql)
    product = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('detail.html', product=product)


@app.route('/product/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(productId):
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = db_connection()
        cur = conn.cursor()
        productName = request.form['productName']
        description = request.form['description']
        productName = productName.strip()
        description = description.strip()

        sql_params = (productName, description, productId)

        sql = "UPDATE products SET productName = '%s', description = '%s' WHERE id = %d" % sql_params
        print(sql)
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
        # use redirect to go to certain url. url_for function accepts the
        # function name of the URL which is function index() in this case
        return redirect(url_for('index'))

    # find the record first
    conn = db_connection()
    cur = conn.cursor()
    sql = 'SELECT productId, productName, body FROM articles WHERE id = %s' % productId
    cur.execute(sql)
    article = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('edit.html', product=product)


@app.route('/product/delete/<int:productId>', methods=['GET', 'POST'])
def delete(productId):
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    conn = db_connection()
    cur = conn.cursor()
    sql = 'DELETE FROM articles WHERE id = %s' % productId
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return jsonify({'status': 200, 'redirect': '/'})