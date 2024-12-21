import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database\students.db')
cursor = conn.cursor()

# Function to fetch student image by ID
def fetch_student_image(student_id):
    cursor.execute('SELECT image FROM students WHERE id=?', (student_id,))
    record = cursor.fetchone()
    if record:
        return record[0]  # Return the image blob
    return None

# Function to save fetched image to a file
def save_image(image_blob, output_filename):
    with open(output_filename, 'wb') as output_file:
        output_file.write(image_blob)

# Example usage
student_id_to_fetch = int(input("Enter the Student ID to fetch the image: "))
image_blob = fetch_student_image(student_id_to_fetch)
if image_blob:
    output_filename = f'output_image_{student_id_to_fetch}.jpg'  # Define output filename
    save_image(image_blob, output_filename)
    print(f"Image for Student ID {student_id_to_fetch} has been saved as {output_filename}.")
else:
    print(f"No image found for Student ID {student_id_to_fetch}.")

# Close the connection
conn.close()