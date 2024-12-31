import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

def test_connection():
    connection = None  # Khai báo kết nối ở ngoài try để tránh lỗi UnboundLocalError
    try:
        # Thay đổi thông tin kết nối theo hệ thống của bạn
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # Tên người dùng MySQL
            password=os.getenv("DB_PASSWORD"),  # Lấy mật khẩu từ biến môi trường
            database='weather_data'  # Tên cơ sở dữ liệu
        )

        if connection.is_connected():
            print("Connection to MySQL was successful!")
            # Kiểm tra thông tin cơ sở dữ liệu
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
        
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        # Đóng kết nối khi xong, kiểm tra biến connection đã được khởi tạo hay chưa
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    test_connection()
