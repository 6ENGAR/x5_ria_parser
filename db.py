import psycopg2
from config import DB_PASSWORD

connection = psycopg2.connect(
    database="bmwx5",
    user="postgres",
    password=f"{DB_PASSWORD}",
    host="127.0.0.1",
    port="5432"
)


def car_exists(title, link):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cars WHERE title = %s AND link = %s;", (title, link))
            return cursor.fetchone() is not None
    except Exception as e:
        print(e)
        return False


def add_new_car(title, price, mileage, location, fuel_type, transmission, plate, vin_code, link):
    if car_exists(title, link):
        print(f"[!] Vehicle '{title}' with link: '{link}' and price ${price} is already in db.")
    else:
        try:
            with connection.cursor() as cursor:
                if "BMW X5" not in title:
                    print(f"[x] {title} is an add post. Not added to db")
                else:
                    cursor.execute("INSERT INTO cars(title, price, mileage, location, fuel_type, transmission, plate, "
                                   "vin_code, link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                   (title, price, mileage, location, fuel_type, transmission, plate, vin_code, link))
                    connection.commit()
                    print(f"[+] {title} {plate} {vin_code} ${price} {link} has been added to db.")
        except Exception as e:
            print(e)


