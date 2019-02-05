import time
import VL53L0X

from PIL import Image
import select
import v4l2capture

import requests
import boto3
import pygame
import os

import socket

ipaddr = "52-207-185-193"

##############################################################################################################

def capture_picture():
#use the USB webcam to capture a picture and save it
    video = v4l2capture.Video_device("/dev/video0")
    size_x, size_y = video.set_format(1280, 720)

    video.create_buffers(1)

    video.queue_all_buffers()

    video.start()

    select.select((video,), (), ())

    image_data = video.read()
    video.close()
    image = Image.fromstring("RGB", (size_x, size_y), image_data)
    image.save("image.jpg")
    print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"

##############################################################################################################
    
def post_image():
#post the captured picture to Amazon S3 bucket for face verification
    s3 = boto3.resource('s3')

    data = open('image.jpg', 'rb')
    s3.Bucket('iotprojectcloud').put_object(Key='image.jpg', Body=data)    
    
def face_api():
#Use Amazon Rekognition to verify the face of person in captured image with a standard reference
    bucket='iotprojectcloud'
    sourceFile='image.jpg'
    targetFile='prashant.jpg'

    try:
        client=boto3.client('rekognition')

        response=client.compare_faces(SimilarityThreshold=70,
                                  SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile}},
                                  TargetImage={'S3Object':{'Bucket':bucket,'Name':targetFile}})

        for faceMatch in response['FaceMatches']:
            confidence = float(faceMatch['Face']['Confidence'])
        
        return confidence
    except:
        text_to_speech("error.mp3")

##############################################################################################################        

def text_to_speech(aud):
#Play MP3 file stored in the same directory
    pygame.mixer.init()
    pygame.mixer.music.load(aud)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
    	continue

##############################################################################################################    

def gif():
#capture a stream of images and push it to Amazon EC2 server
    name = "image"
    ext = ".jpg"
    for i in range(30):
        video = v4l2capture.Video_device("/dev/video0")
        size_x, size_y = video.set_format(1280, 720)
    
        video.create_buffers(1)

        video.queue_all_buffers()

        video.start()

        select.select((video,), (), ())

        image_data = video.read()
        video.close()
        image = Image.fromstring("RGB", (size_x, size_y), image_data)

        file = name + str(i) + ext
        image.save(file)
        print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"
        command = "scp -i key.pem "+file+" ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
        os.system(command)

##############################################################################################################
        
def remove_all():
#Delete all files in Amazon EC2 server after the process is complete
    print("Cleaning up........")
    name = "image"
    ext = ".jpg"
    for i in range(30):
        file = name + str(i) + ext
        remove = "rm -f " + file
        command = "ssh -i key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com " + remove
        os.system(command)
        os.system("rm " + file)
    os.system("ssh -i key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com rm -f prashant.jpg")
    os.system("rm image.jpg")
    print ("Wiped clean!!")    

##############################################################################################################
    
def nonpolling():
    print("Waiting for server.........")
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get machine name
    host = '52.90.46.91'                           

    port = 9999

    print("Connected to host...........  waiting for authentication")

    # connection to hostname on the port.
    s.connect((host, port))                               

    # Receive no more than 1024 bytes
    tm = s.recv(1024)                                     

    s.close()

    print("%s" % tm.decode('ascii'))


##############################################################################################################
                    
def send_details():
#Send details of person standing before camera to Amazon EC2 Server
    file = open('details.txt', 'w')
    file.write('Prashant')
    file.close()
    command = "scp -i key.pem details.txt ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
    os.system(command)    
    
######################  Main  ################################################################################
    
# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

for count in range(1,100):
    distance = tof.get_distance()
    print ("%d mm, %d" % (distance, count))
    if (distance > 80 and distance < 90):
       tof.stop_ranging()
       text_to_speech("Audio messages//face_the_camera.mp3")
       capture_picture()
       post_image()
       confidence = face_api()
       if (confidence > 85):
           text_to_speech("Audio messages//wait_for_admin.mp3")
           send_details()
           gif()
           nonpolling()
           text_to_speech("Audios messages//welcome.mp3")
           remove_all()
       else:
           text_to_speech("Audio messages//sorry.mp3")
       break

