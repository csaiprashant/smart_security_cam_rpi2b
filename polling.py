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
    
def face_api(name):
#Use Amazon Rekognition to verify the face of person in captured image with a standard reference
    key = name +'.jpg'

    bucket='iotprojectcloud'
    sourceFile = 'image.jpg'
    targetFile = key

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
                continue           
        if (a == 999):
            text_to_speech("timeout.mp3")
            remove_all()
            quit()
##############################################################################################################
        
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
     print("Polling server.....,")    
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
                    
def send_details(name):
#Send details of person standing before camera to Amazon EC2 Server
    file = open('details.txt', 'w')
    file.write(name)
    file.close()
    command = "scp -i key.pem details.txt ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
    os.system(command)
    
        
######################  Main  ################################################################################

print("Populating Database....")
file = open("data.txt", "r")
i = 0
lines = file.readlines()
dist=[0 for x in range(5)]
name=[0 for x in range(5)]
for lineb in lines:
    line = lineb.rstrip('\n')
    if (i % 2 == 0):
        dist[i] = line
        i = i + 1
    else:
        name[i- 1] = line
        i = i + 1
print dist
print name
# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

for count in range(1,100):
    distance = tof.get_distance()
    print ("%d mm, %d" % (distance, count))
    if (distance == int(dist[0]) or distance == int(dist[1]) or distance == int(dist[2] or distance == int(dist[4]))):
       tof.stop_ranging()
       text_to_speech("Audio messages//face_the_camera.mp3")
       capture_picture()
       post_image()
       if (distance == int(dist[0])):
           i = 0
       if (distance == int(dist[1])):
           i = 1
       if (distance == int(dist[2])):
           i = 2
       if (distance == int(dist[3])):
           i = 3
       if (distance == int(dist[4])):
           i = 4 
       confidence = face_api(str(name[i]))
       if (confidence > 85):
           text_to_speech("Audio messages//wait_for_admin.mp3")
           send_details(str(name[i]))
           timestamp = '{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
           file = open("log.txt", "a")
           line = name[i] + " SUCCESS " + timestamp + "\n"
           file.write(line)
           file.close()
           command = "scp -i key.pem log.txt ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
           os.system(command)
           gif()
       else:
           text_to_speech("Audio messages//sorry.mp3")
           timestamp = '{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
           filename = timestamp + '.jpg'
           file = open("log.txt", "a")
           line = "N/A FAIL " + timestamp + "\n"
           file.write(line)
           file.close()
           command = "scp -i key.pem log.txt ubuntu@ec2-"+ipaddr+".compute-1.amazonaws.com:/home/ubuntu/"
           os.system(command)
       break
