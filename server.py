from tkinter import Y
from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)

connection = get_sql_connection()

# Creating my own exception



@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    return response
try:
    get_uom()
except Exception as e:
    print(e)


@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    return response
try:
    get_products()
except Exception as e:
    print(e)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    
    return response
try:
    insert_product()
except Exception as e:
    print('You have to insert product from product', e)

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    
    return response



@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    
    return response

@app.errorhandler(404)
def invalid_route(e):
    return "WELCOME TO T&A GROCERY STORE"




if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)

