import json
import psycopg2

def lambda_handler(event, context):

    id = "YDbnBtbHN0N0G6GfLhHT"
    conn = psycopg2.connect(
        database="phmax",
        user="pharbers",
        password="Abcde196125",
        host="192.168.49.199",
        port="5442"
    )
    print("Opened database successfully")
    cur = conn.cursor()

    cur.execute(
        'SELECT message FROM "jobLog" WHERE ID= ' + '\'' + id +'\''
    )
    # WHERE id=YDbnBtbHN0N0G6GfLhHT
    message = cur.fetchall()
    print(message)
    conn.close()

