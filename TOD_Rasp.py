#Imports the necessary libraries        
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from picamera import PiCamera
from gpiozero import MotionSensor
from gpiozero import Buzzer
from time import sleep

#MQTT setup
def messageFunction(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    print(topic + message)

#Creates a MQTT client object 
ourClient = mqtt.Client("makerio_mqtt")
#Connects to the test MQTT broker
ourClient.connect("test.mosquitto.org", 1883)
#Attaches the messageFunction 
ourClient.on_message = messageFunction
#Starts the MQTT client object 
ourClient.loop_start()

#Set warnings to false 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Makes the motion sensor an input
#Reads output from PIR motion sensor
GPIO.setup(4, GPIO.IN)

#Makes the buzzer output so sound can be emitted
GPIO.setup(17, GPIO.OUT)

#Creates variable pir which links to GPIO4  
pir = MotionSensor(4)
#Creates variable buzzer which links tp GPIO17
buzzer = Buzzer(17)
#Creates variable camera from PiCamera library
camera = PiCamera()
#Counter allows multiple photos to be taken under Dog name 
i = 0

while True:
    #Creates a variable to track motion status (1 or 0)
    motion_status = GPIO.input(4)
    #Pauses the script until motion is first detected 
    pir.wait_for_motion(timeout = None)
    #Condition for when motion is detected
    #Starts a chain of events 
    if motion_status == 1:
        print(motion_status)
        print("Motion Detected Potential DOG")
        
        #Dog deterrent alarm goes through a small cycle of on then off
        buzzer.on()
        sleep(4)
        buzzer.off()
        
        #Opens camera preview for demo purposes
        #Sleep is needed to allow the camera to adjust 
        camera.start_preview()
        sleep(5)
        
        #Captures an image saved in documents
        #Increments Dog[i].jpg
        camera.capture("Dog%s.jpg" % i)
        camera.stop_preview()
        
        #MQTT publishing of Movement event from topic Dog
        #This will trigger the particle argon 
        ourClient.publish("Dog", "Movement")
        time.sleep(1)
        
        #increments i with each iteration
        i = i+1
        sleep(10)
        pir.wait_for_no_motion(timeout = 10)
        
    #Condition for when no motion is detected
    if motion_status == 0:
        #MQTT publishing of No_Movement event from topic Dog
        ourClient.publish("Dog", "No_Movement")
        print("No Motion or Dog")
        sleep(120)
