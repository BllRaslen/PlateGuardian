import cv2
import pytesseract
import psycopg2
import paho.mqtt.client as mqtt
import time


# Set the path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# MQTT Configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_username = "blendable"
mqtt_password = "bll.raslen"

# PostgreSQL Configuration
db_config = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "bll.raslen",
    "database": "biti"
}

# MQTT Topics
mqtt_topic_existing = "mevcud/topic"
mqtt_topic_not_existing = "yok/topic"
mqtt_topic_movement = "may/topic"

# Connect to MQTT Broker
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=mqtt_username, password=mqtt_password)
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Connect to PostgreSQL Database
db_connection = psycopg2.connect(**db_config)
db_cursor = db_connection.cursor()

# Function to publish a message to MQTT
def publish_mqtt_message(topic, message):
    mqtt_client.publish(topic, message)


# Function to process video frames and extract the car number plate
def process_video():
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while True:
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Configure Tesseract OCR
        custom_config = r'--oem 3 --psm 6 outputbase digits'

        # Perform OCR on the grayscale image
        plate_number = pytesseract.image_to_string(gray, config=custom_config)

        # Remove non-alphanumeric characters from the plate number
        plate_number = ''.join(e for e in plate_number if e.isalnum())

        # Check if 3 seconds have elapsed
        if time.time() - start_time >= 3:
            # Print the recognized plate number to the console every 3 seconds
            print("Plate Number:", plate_number)

            # Reset the timer
            start_time = time.time()

        # Check if the plate number exists in the database
        if check_plate_existence(plate_number):
            publish_mqtt_message(mqtt_topic_existing, f"Plate number {plate_number} exists.")
        else:
            publish_mqtt_message(mqtt_topic_not_existing, f"Plate number {plate_number} does not exist.")

        # Publish movement message to MQTT
        publish_mqtt_message(mqtt_topic_movement, "90")

        # Display the frame with license plate recognition
        cv2.imshow('License Plate Recognition', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    # Close the PostgreSQL cursor and connection
    db_cursor.close()
    db_connection.close()

    # Disconnect from MQTT Broker
    mqtt_client.disconnect()

# Function to check if the plate number exists in the database
def check_plate_existence(plate_number):
    query = "SELECT * FROM car_info WHERE plate_number = %s"
    db_cursor.execute(query, (plate_number,))
    result = db_cursor.fetchone()
    return result is not None

if __name__ == "__main__":
    process_video()
