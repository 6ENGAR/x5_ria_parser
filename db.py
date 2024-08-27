import config
import psycopg2
from config import DB_PASSWORD
from notifiers import get_notifier

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


def add_new_car(title, price, mileage, location, fuel_type, transmission, plate, vin_code, link, details):
    if car_exists(title, link):
        print(f"[!] Vehicle '{title}' with link: '{link}' and price ${price} is already in db.")
    else:
        try:
            with connection.cursor() as cursor:
                if "BMW X5" not in title:
                    print(f"[x] {title} is an add post. Not added to db")
                else:
                    cursor.execute("INSERT INTO cars(title, price, mileage, location, fuel_type, transmission, plate, "
                                   "vin_code, link, details) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                   (title, price, mileage, location, fuel_type, transmission, plate, vin_code, link,
                                    details))
                    connection.commit()
                    print(f"[+] {title} {plate} {vin_code} ${price} {link} has been added to db.")
                    telegram = get_notifier('telegram')
                    to_send = f'''
                    🚨 З'явився новий автомобіль — {title} {details} 
                    
🪪 Номер: {plate}
🔖 VIN код: {vin_code}

💰 Ціна: {price}
🤖 Коробка: {transmission}
🚘 Пробіг: {mileage} 
⚙️ Двигун: {fuel_type}
🏡 Знаходиться в: {location}

🔗 {link}
                    '''
                    telegram.notify(token=f'{config.BOT_TOKEN}', chat_id=f'{config.CHAT_ID}', message=to_send)
        except Exception as e:
            print(e)


