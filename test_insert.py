import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

def test_insert():
    try:
        # Kết nối đến MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # Tên người dùng MySQL
            password=os.getenv("DB_PASSWORD"),  # Mật khẩu MySQL
            database='weather_data'  # Tên cơ sở dữ liệu
        )

        if connection.is_connected():
            print("Connection to MySQL was successful!")
            
            # Tạo một đối tượng cursor để thực hiện câu lệnh SQL
            cursor = connection.cursor()
            
            # Chuẩn bị câu lệnh SQL để insert dữ liệu
            insert_query = """
            INSERT INTO weather (city, temperature, humidity, weather, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            # Dữ liệu cần thêm vào bảng
            data = (
                'Ho Chi Minh',     # Thành phố
                30.5,              # Nhiệt độ
                80,                # Độ ẩm
                'Clear sky',       # Mô tả thời tiết
                datetime.now()     # Thời gian hiện tại
            )
            
            # Thực hiện câu lệnh insert
            cursor.execute(insert_query, data)
            
            # Commit thay đổi vào cơ sở dữ liệu
            connection.commit()
            
            print("Data inserted successfully!")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        # Đóng kết nối khi xong
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    test_insert()
