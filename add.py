from PIL import Image
import select
import v4l2capture

import boto3


file = open("data.txt", "a")
d = raw_input("\nEnter distance\n")
file.write(d + "\n" )
n = raw_input("\nEnter Name\n") 
file.write(n + "\n" )
file.close()

print("Face the camera")

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
photo = n +'.jpg'
image.save(photo)
print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"
        
#post the captured picture to Amazon S3 bucket for face verification
s3 = boto3.resource('s3')

data = open(photo, 'rb')
s3.Bucket('iotprojectcloud').put_object(Key = photo, Body=data)  
