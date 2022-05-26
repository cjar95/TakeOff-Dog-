// Includes the necessary MQTT library
#include <MQTT.h>

 //the IP of the MQTT broker (raspberry pi)
 byte server[] = { 192,168,0,92 };
 
 //Defines the client 
 MQTT client(server, 1883, callback);
 
 //Recieves the messages 
void callback(char* topic, byte* payload, unsigned int length) {
     char p[length + 1];
     memcpy(p, payload, length);
     p[length] = NULL;
     String message(p);
     
    if (message.equals("Movement"))
        //Triggers the IFTTT to send an SMS
        //Publishes data "Movement" to the topic "Dog"
        Particle.publish("Dog", "Movement", PRIVATE);
     else if (message.equals("No_Movement"))
        //Publishes to the events stream of particle with NO IFTTT trigger and subsequent SMS
         Particle.publish("No-Go Zone is empty");
     else
        //If neither Movement or No Movement are receieved from the Pi broker publishes a message to particle events stream
         Particle.publish("TakeOff Dog is not detecting");
     delay(1000);
 }
void setup() {
    
     client.connect(System.deviceID());
     //Only subscribe to messages when the client is connected 
     if (client.isConnected()) {
         //Dog is the topic that argon is subscribed to 
         client.subscribe("Dog");
         //Console check to ensure connection
         Particle.publish("Connection is working");
         
     }
 }
void loop() {
    //While the client is connected continue the program loop
     if (client.isConnected())
         client.loop();
         
 } 
