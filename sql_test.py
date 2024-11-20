import pyodbc
import time
from datetime import datetime, timedelta

# Підключення до SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-E1L4539\\SQLEXPRESS;'
    'DATABASE=BDFlights;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Очистка таблиць перед тестами
cursor.execute("DELETE FROM Crews;")
cursor.execute("DELETE FROM Flights;")
conn.commit()

# Функція для тестування швидкодії вставки даних
def test_sql_insert():
    start_time = time.time()

    # Генерація та вставка даних
    for i in range(10000):  # Створюємо 10,000 рейсів
        flight_id = f"flight_{i}"
        date_time = (datetime.now() + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
        duration = 120 + i % 60
        airplane_id = i % 50
        route_id = i % 100

        # Вставка в Flights
        cursor.execute("""
            INSERT INTO Flights (FlightID, DateTime, Duration, AirplaneID, RouteID)
            VALUES (?, ?, ?, ?, ?);
        """, flight_id, date_time, duration, airplane_id, route_id)

        # Вставка в Crews
        cursor.execute("""
            INSERT INTO Crews (EmployeeID, FlightID, Name, Surname, Role, Position, LicenseNumber, ContactDetails)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, 1000 + i * 2, flight_id, f"John_{i}", f"Doe_{i}", "Pilot", "Captain", f"ABC12345_{i}", f"john.doe{i}@example.com")

        cursor.execute("""
            INSERT INTO Crews (EmployeeID, FlightID, Name, Surname, Role, Position, LicenseNumber, ContactDetails)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, 1001 + i * 2, flight_id, f"Jane_{i}", f"Smith_{i}", "Co-Pilot", "First Officer", f"DEF67890_{i}", f"jane.smith{i}@example.com")

    conn.commit()
    end_time = time.time()
    print(f"SQL Insert Time: {end_time - start_time} seconds")

# Функція для тестування швидкодії вибірки даних
def test_sql_query():
    start_time = time.time()

    # Вибірка всіх рейсів із маршрутом RouteID = 5
    cursor.execute("SELECT * FROM Flights WHERE RouteID = 5;")
    rows = cursor.fetchall()
    for row in rows:
        pass  # Перебір результатів для вимірювання часу вибірки

    end_time = time.time()
    print(f"SQL Query Time: {end_time - start_time} seconds")

# Виконання тестів
test_sql_insert()
test_sql_query()

# Закриття підключення
cursor.close()
conn.close()
