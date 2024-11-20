from pymongo import MongoClient
from datetime import datetime, timedelta
import time

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['Lab2Flights']

# Очистити колекцію перед вставкою нових даних
db.Flights.delete_many({})

# Функція для тестування швидкодії вставки даних
def test_mongo_insert():
    # Генерація даних для вставки
    flights = []
    for i in range(10000):  # Створюємо 10,000 рейсів
        flight = {
            "_id": f"flight_{i}",
            "date_time": (datetime.now() + timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration": 120 + i % 60,  # Тривалість (120-180 хв)
            "airplane_id": i % 50,  # 50 унікальних літаків
            "route_id": i % 100,  # 100 маршрутів
            "crew": [
                {
                    "employee_id": 1000 + i,
                    "name": f"John_{i}",
                    "surname": f"Doe_{i}",
                    "role": "Pilot",
                    "position": "Captain",
                    "license_number_pilots": f"ABC12345_{i}",
                    "contact_details": f"john.doe{i}@example.com"
                },
                {
                    "employee_id": 2000 + i,
                    "name": f"Jane_{i}",
                    "surname": f"Smith_{i}",
                    "role": "Co-Pilot",
                    "position": "First Officer",
                    "license_number_pilots": f"DEF67890_{i}",
                    "contact_details": f"jane.smith{i}@example.com"
                }
            ]
        }
        flights.append(flight)

    # Вставка даних
    start_time = time.time()
    db.Flights.insert_many(flights)
    end_time = time.time()

    print(f"MongoDB Insert Time: {end_time - start_time} seconds")

# Функція для тестування швидкодії вибірки даних
def test_mongo_query():
    start_time = time.time()
    # Вибірка всіх рейсів із маршрутом route_id = 5
    flights = db.Flights.find({"route_id": 5})
    for flight in flights:
        pass  # Перебір результатів
    end_time = time.time()

    print(f"MongoDB Query Time: {end_time - start_time} seconds")

# Виконання тестів
test_mongo_insert()
test_mongo_query()
