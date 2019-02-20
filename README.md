# Build a Physical Authentication System for your Home

## You will need:
- A Raspberry Pi 2B – with a Wi-Fi module and an SD card (at least 8GB)
- Adafruit VL53L0X Time of Flight Distance Sensor
- A USB Webcam
- An Amazon AWS account
- A phone capable of running Android
- A monitor, HDMI cable, a USB keyboard and mouse (optional)

## Introduction:
We equip the Raspberry Pi with a USB camera and a distance sensor. We maintain a database of whitelisted people.  The entry fields in the database are the person’s face and a unique distance as measured by the distance sensor. When the distance measured by the sensor matches the entry in the database, the camera captures a picture of the person standing before it and verifies it with the corresponding database entry using a Face Recognition API. If there is a match, the administrator is notified on his Android phone via an app. The administrator can then either grant access to the person or deny it using a simple Yes-or-No GUI on the app. The result is then relayed back to the person requesting access. All communication between the Raspberry Pi and the administrator’s Android phone is done using a sever hosted in Amazon AWS cloud.

## What You Will Learn:
- Configuring your Raspberry Pi to capture images from a USB webcam connected to it.
- Working with Adafruit VL53L0X Time of Flight Distance Sensor.
- Working with Amazon AWS services like Amazon S3, Amazon Rekognition, Amazon EC2 and Amazon Polly.
- Basic server-side scripting and Android Studio programming.
- System and Network related issues to decrease latency and get the best out of your setup.

### For full report, refer: [Project Report](https://github.com/csaiprashant/smart_security_cam_rpi2b/blob/master/projectreport.pdf)

--------------------------------------------

## Files in this repository:
- /Android/... - Contains all Android app related code for both Polling and Long-Polling versions. Code includes Android Manifext.xml, layouts and strings XML files and the Java code.
- /Database/... - Python code for creating an SQLite database, creating a table in it, adding rows and querying data from it.
- /Audio message/<XYZ.mp3> - Status messages to be played by the Raspberry Pi.
- add.py - Adds a new user into the system.
- bytes.py - Gives a summary of the size of each image frame. The data from this program can be compared against that obtained from Wireshark to measure network overhead incurred.
- data.txt - Quasi-database of users in the system. Offers an easier route when adding a new user to the system.
- datarate.py - Measures downstream throughput from the server to the Raspberry Pi periodically and makes decisions about the quality of images to be uploaded.
- details.txt - Raspberry Pi writes the name of the user to it. Android app reads this file to know which name to display.
- log.txt - Maintains a log of all the interactions of the system with its user(s).
- longpollserver.py - Server code for non-polling implementation.
- nonpolling.py - Non-polling implementation of the system.
- polling.py - Polling implementation of the system.
- projectreport.pdf - A report of the project.
- README.md
