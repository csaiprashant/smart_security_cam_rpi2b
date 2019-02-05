import time
import VL53L0X

from PIL import Image
import select
import v4l2capture

import requests
import boto3
import pygame
import os

import datetime

ipaddr = "52-207-185-193"

##############################################################################################################

def capture_picture():
#use the USB webcam to capture a picture and save it
    video = v4l2capture.Video_device("/dev/video0")
    size_x, size_y = video.set_format(640, 480)

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

def gif480():
#capture a stream of images and push it to Amazon EC2 server
    print("Capturing 640x480 frames")
    a = 1
    while True:
        video = v4l2capture.Video_device("/dev/video0")
        size_x, size_y = video.set_format(640, 480)
    
        video.create_buffers(1)

        video.queue_all_buffers()

        video.start()

        select.select((video,), (), ())

        image_data = video.read()
        video.close()
        image = Image.fromstring("RGB", (size_x, size_y), image_data)

        image.save("image.jpg")
        command = "scp -i key.pem image.jpg ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
        os.system(command)
        a = a + 1
        if (a % 10 == 0):
            result = polling()
            if (result == True):
                text_to_speech("welcome.mp3")
                remove_all()
                os.system("rm yes.txt")
                quit()
            else:
                downstream = datarate()
                if (downstream > 28):
                    gif480()
                else:
                    gif120()      
        if (a == 999):
            text_to_speech("timeout.mp3")
            remove_all()
            quit()
##############################################################################################################
def gif120():
#capture a stream of images and push it to Amazon EC2 server
    print("Capturing 160x120 frames")
    a = 1
    while True:
        video = v4l2capture.Video_device("/dev/video0")
        size_x, size_y = video.set_format(160, 120)
    
        video.create_buffers(1)

        video.queue_all_buffers()

        video.start()

        select.select((video,), (), ())

        image_data = video.read()
        video.close()
        image = Image.fromstring("RGB", (size_x, size_y), image_data)

        image.save("image.jpg")
        command = "scp -i key.pem image.jpg ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
        os.system(command)
        a = a + 1
        if (a % 10 == 0):
            result = polling()
            if (result == True):
                text_to_speech("welcome.mp3")
                remove_all()
                os.system("rm yes.txt")
                quit()
            else:
                downstream = datarate()
                if (downstream > 28):
                    gif480()
                else:
                    gif120()         
        if (a == 999):
            text_to_speech("timeout.mp3")
            remove_all()
            quit()

#############################################################################################################       
def remove_all():
#Delete all files in Amazon EC2 server after the process is complete
    print("Cleaning up........")
    remove = "rm -f image.jpg"
    command = "ssh -i key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com rm -f image.jpg"
    os.system(command)
    os.system("ssh -i key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com rm -f details.txt")
    os.system("rm image.jpg")
    print ("Wiped clean!!")    

##############################################################################################################
    
def polling():
#Implementation of 'Polling'
     try:
         url = "https://firebasestorage.googleapis.com/v0/b/iotfirebaseproject-55895.appspot.com/o/yes.txt?alt=media&token=67dee95d-fe0e-4be4-86ae-2dbbac0b6b09"
         r = requests.get(url,allow_redirects=True)
         open("yes.txt","wb").write(r.content)
         file = open("yes.txt")
         for line in file:
             if (len(line) == 3):
                file.close()
                print("found file")
                return True
     except Exception:
         return False
     else:
         return False

##############################################################################################################
def datarate():
    print("Measuring average downstream bandwidth")
    command1 ="scp -i  key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/test/test1.jpg ."
    command2 ="scp -i  key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/test/test2.png ."
    command3 ="scp -i  key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/test/test3.jpg ."
    command4 ="scp -i  key.pem ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/test/test4.png ."
    before = datetime.datetime.now()
    os.system(command1)
    os.system(command2)
    os.system(command3)
    os.system(command4)
    after = datetime.datetime.now()
    downloadtime = (after-before).seconds
    speed = 150 / float(downloadtime)
    print(str(speed) + "KB/s")
    return(speed)

#############################################################################################################

def send_details():
#Send details of person standing before camera to Amazon EC2 Server
    file = open('details.txt', 'w')
    file.write("Prashant")
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
       text_to_speech("face_the_camera.mp3")
       capture_picture()
       post_image()
       confidence = face_api()
       if (confidence > 85):
           send_details()
           text_to_speech("wait_for_admin.mp3")
           downstream = datarate()
           if (downstream > 20):
               gif480()
           else:
               gif120()               
       else:
           text_to_speech("sorry.mp3")
       break

