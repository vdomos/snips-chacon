#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                                    

'''
14/6/2018
https://snips.gitbook.io/tutorials/t/technical-guides/listening-to-intents-over-mqtt-using-python
Voir shéma du protocole Hermes pour voir les différents messages MQTT.

You will most likely be interested in the following messages:
    hermes/hotword/<hotword_id>detected: 
        when a wakeword is detected, this message will be sent, and Snips will listening to your voice command. 
        You can for instance use this message to play a little tone, or start a led animation, indicating the start of a listening session
    hermes/asr/textCaptured: when listening, 
        Snips will transcribe your query into text, and after a small period of silence, it will stop listening, and send this message. 
        You may use this to play another tone, or stop a led animation, indicating end of listening
    hermes/intent/<intent_name>: after text has been captured, 
        the NLU module will process the text and transform it into an intent, which is the final representation of your query that you can use as an actionable item. 
        This is where you want to put your intent handler code
    
https://github.com/respeaker/4mics_hat/pixels_demo.py
'''

import json
import paho.mqtt.client as mqtt
from pixels import Pixels, pixels
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern

HOST = 'localhost'
PORT = 1883
SUBTOPIC = [('hermes/hotword/#', 0), ('hermes/intent/#', 0), ('hermes/asr/#', 0), ('hermes/tts/#', 0), ('hermes/nlu/#', 0)]

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    client.subscribe(SUBTOPIC) 
    
def on_message(client, userdata, msg):
    #print("Message received on topic {0}: {1}".format(msg.topic, msg.payload))
    if "hotword" in msg.topic:
        print("==> hotword message {0}: {1}".format(msg.topic, msg.payload))
        if "detected" in msg.topic:
            pixels.wakeup()
        if msg.topic == "hermes/hotword/toggleOn":
            pixels.off()
    if "asr" in msg.topic:
        print("==> asr message {0}: {1}".format(msg.topic, msg.payload))
        if "textCaptured" in msg.topic:
            pixels.think()
    if "nlu" in msg.topic:
        print("==> nlu message {0}: {1}".format(msg.topic, msg.payload))
    if "tts" in msg.topic:
        print("==> tts message {0}: {1}".format(msg.topic, msg.payload))
        if msg.topic == "hermes/tts/say":
            pixels.speak()
    elif "intent" in msg.topic:
        print("==> intent message {0}: {1}".format(msg.topic, msg.payload))
        #intent_topic = msg.topic.split("/") 
        payload = json.loads(msg.payload)
        if "intent" in payload:
            name = payload["intent"]["intentName"]
            slots = payload["slots"]
            print("====> intent {0} detected with slots {1}".format(name, slots))   


pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
#pixels.pattern = AlexaLedPattern(show=pixels.show)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)
client.loop_forever()
pixels.off()

