import psycopg2
from config import DB_PASSWORD

connection = psycopg2.connect(
    database="bmwx5",
    user="postgres",
    password=f"{DB_PASSWORD}",
    host="127.0.0.1",
    port="5432"
)


def add_new_car(title, price, mileage, location, fuel_type, transmission, plate, vin_code, link):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO cars(title, price, mileage, location, fuel_type, transmission, plate, "
                           "vin_code, link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                           (title, price, mileage, location, fuel_type, transmission, plate, vin_code, link))
            connection.commit()
            print(f"[+] {title} {plate} {vin_code} has been added to db")
    except Exception as e:
        print(e)


def get_last_row():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cars ORDER BY id DESC LIMIT 1;")
            return  cursor.fetchone()
    except Exception as e:
        print(e)