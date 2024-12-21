import sqlite3
import os
import re
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('database\students.db')
cursor = conn.cursor()

# Create table with additional fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        major TEXT,
        starting_year INTEGER,
        total_attendance INTEGER,
        standing TEXT,
        year INTEGER,
        last_attendance_time DATETIME,
        image BLOB
    )
''')
conn.commit()

# Function to convert image to binary
def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

# Function to insert student image with additional details
def insert_student_image(student_id, name, major, starting_year, total_attendance, standing, year, last_attendance_time, image_path):
    image = convert_to_binary_data(image_path)
    cursor.execute('''
        INSERT INTO students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, name, major, starting_year, total_attendance, standing, year, last_attendance_time, image))
    conn.commit()

# Function to extract numbers from text
def extract_numbers(text):
    pattern = r'\d+'
    matches = re.findall(pattern, text)
    number_string = ''.join(matches)
    return number_string

# Function to validate date-time format
def validate_datetime(date_time_str):
    try:
        # Attempt to parse the date-time string
        return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None  # Return None if the format is incorrect

# Function to process images in a directory
def process_images_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check for image files
            student_id_str = extract_numbers(filename)  # Extract numbers from filename
            if student_id_str:  # Check if any numbers were found
                student_id = int(student_id_str)  # Convert to integer
                student_name = filename.split('.')[0]  # Use filename (without extension) as name
                
                # Prompt for additional student details
                major = input(f"Enter major for {student_name}: ")
                starting_year = int(input(f"Enter starting year for {student_name}: "))
                total_attendance = int(input(f"Enter total attendance for {student_name}: "))
                standing = input(f"Enter standing for {student_name}: ")
                year = int(input(f"Enter year for {student_name}: "))
                
                # Prompt for last attendance time and validate
                last_attendance_time_str = input(f"Enter last attendance time for {student_name} (YYYY-MM-DD HH:MM:SS): ")
                last_attendance_time = validate_datetime(last_attendance_time_str)
                
                if last_attendance_time is None:
                    print("Invalid date-time format. Please use YYYY-MM-DD HH:MM:SS.")
                    continue  # Skip this entry if the format is incorrect
                
                image_path = os.path.join(directory, filename)
                insert_student_image(student_id, student_name, major, starting_year, total_attendance, standing, year, last_attendance_time, image_path)
                print(f"Inserted {student_name} with ID {student_id}")

# Example usage
directory_path = input("Enter the directory path containing images: ")
process_images_in_directory(directory_path)

# Close the connection
conn.close()