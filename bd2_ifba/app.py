import psycopg2


if __name__ == "__main__":
    print("caio")
    conn = psycopg2.connect(
        host="localhost",
        database="caio",
        user="caio",
        password="caio")

    cur = conn.cursor()
    cur.execute('SELECT * FROM compras')
    result = cur.fetchall()
    cur.close()
