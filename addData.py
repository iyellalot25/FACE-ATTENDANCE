import sqlite3
import os
import re

# Connect to SQLite database
conn = sqlite3.connect('database\students.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        image BLOB
    )
''')
conn.commit()

# Function to convert image to binary
def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

# Function to insert student image with ID
def insert_student_image(student_id, name, image_path):
    image = convert_to_binary_data(image_path)
    cursor.execute('''
        INSERT INTO students (id, name, image) VALUES (?, ?, ?)
    ''', (student_id, name, image))
    conn.commit()

# Function to extract numbers from text
def extract_numbers(text):
    pattern = r'\d+'
    matches = re.findall(pattern, text)
    number_string = ''.join(matches)
    return number_string

# Function to process images in a directory
def process_images_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check for image files
            student_id_str = extract_numbers(filename)  # Extract numbers from filename
            if student_id_str:  # Check if any numbers were found
                student_id = int(student_id_str)  # Convert to integer
                student_name = filename.split('.')[0]  # Use filename (without extension) as name
                image_path = os.path.join(directory, filename)
                insert_student_image(student_id, student_name, image_path)
                print(f"Inserted {student_name} with ID {student_id}")

# Example usage
directory_path = input("Enter the directory path containing images: ")
process_images_in_directory(directory_path)

# Close the connection
conn.close()