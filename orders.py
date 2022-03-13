
from sql_connection import get_sql_connection

def insert_orders(connection,order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
             "(order_id,customer_name, total, datetime)"
             "VALUES (%s, %s, %s,%s)")
    order_data = (order['order_id'],order['customer_name'], order['total'],order['datetime'])
    cursor.execute(order_query, order_data)
    connection.commit()
    order_id = cursor.lastrowid
if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_orders(connection, {
         'order_id':156,
         'customer_name': 'Taimoor',
         'total': '500',
         'datetime':'2001-12-11'}))


