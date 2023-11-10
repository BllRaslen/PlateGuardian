# License Plate Recognition System

This Python script utilizes computer vision and optical character recognition (OCR) to recognize license plates in real-time from a video feed. The recognized plate number is then checked against a PostgreSQL database, and corresponding messages are published to an MQTT broker based on the results.

## Prerequisites

Before running the script, ensure the following dependencies are installed:

- [OpenCV](https://pypi.org/project/opencv-python/)
- [PyTesseract](https://pypi.org/project/pytesseract/)
- [Psycopg2](https://pypi.org/project/psycopg2/)
- [Paho-MQTT](https://pypi.org/project/paho-mqtt/)

Additionally, you need to have Tesseract OCR installed on your system. You can download it from [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) and set the path to the executable in the script.

## Configuration

### Tesseract OCR

```python
# Set the path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
```

Make sure to update the path based on your Tesseract installation directory.

### MQTT Configuration

```python
# MQTT Configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_username = "blendable"
mqtt_password = "bll.raslen"
```

Update the MQTT broker details, including the broker address, port, username, and password.

### PostgreSQL Configuration

```python
# PostgreSQL Configuration
db_config = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "bll.raslen",
    "database": "biti"
}
```

Provide the necessary details to connect to your PostgreSQL database.

### MQTT Topics

```python
# MQTT Topics
mqtt_topic_existing = "mevcud/topic"
mqtt_topic_not_existing = "yok/topic"
mqtt_topic_movement = "may/topic"
```

Update MQTT topics based on your application needs.

## Usage

Run the script by executing the following command:

```bash
python script_name.py
```

The script will capture video from the default camera (camera index 0). Press 'q' to exit the video feed.

## Notes

- The script uses Tesseract OCR to extract text (license plate number) from the video frames.
- Recognized plate numbers are checked against a PostgreSQL database (`car_info` table) to determine their existence.
- MQTT messages are published based on the results, indicating whether the plate number exists or not.
- The script continuously processes video frames until the 'q' key is pressed.

Feel free to customize the script to suit your specific requirements or integrate it into your existing system.
