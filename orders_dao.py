from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
             "(order_id,customer_name, total, datetime)"
             "VALUES (%s, %s, %s)")
    order_data = (order['order_id'],order['customer_name'], order['total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details "
                           "(product_id,order_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s,%s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            
            int(order_detail_record['product_id']),
            order_id,
           float(order_detail_record['quantity']),
           float(order_detail_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)
    order_id=cursor.lastrowid

    connection.commit()

    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from order_details where order_id = %s"

    query ='SELECT order_details.order_id, order_details.quantity, order_details.total_price, products.name, products.price_per_unit FROM order_details LEFT JOIN products on order_details.product_id = products.product_id where order_details.order_id=1'

    data = (order_id,connection)

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_order(connection, {
         'order_id':12,
         'customer_name': 'Taimoor',
         'total': '500',
         'datetime': datetime.now(),
         'order_details': [
             {
                 'product_id': 1,
                 'order_id':12,
                 'quantity': 2,
                 'total_price': 50
             },
             {
                 'product_id': 3,
                 'order_id':12,
                 'quantity': 1,
                 'total_price': 30
             }
         ]
     }))