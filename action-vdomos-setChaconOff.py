#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

ROOMSID = {"salon": "5", "canapé": "6", "séjour": "7", "cuisine": "8"}
DMGCMDURL = "http://hermes:40406/rest/cmd/id/"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def httpSetChacon(room):
    url = DMGCMDURL + ROOMSID[room] + "?state=0"        # "http://hermes:40406/rest/cmd/id/7?state=0"
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as err:
        print("Erreur RequestException: '%s'" % err)
        return False
    if req.status_code != 200:
        print("Erreur RequestHttp: '%s'" % req.status_code)
        return False
    return True


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 
     
    Refer to the documentation for further details. 
    """

    print("intentMessage = " % format(intentMessage))
    if len(intentMessage.slots.house_room) > 0:
        room = intentMessage.slots.house_room.first().value             # We extract the value from the slot "house_room"
        if httpSetChacon(room):
            result_sentence = "Lumière {} allumée".format(str(room))    # The response that will be said out loud by the TTS engine.
        else:
            result_sentence = "Echec commande lumière {}".format(str(room))            
    else:
        pass
    hermes.publish_end_session(intentMessage.session_id, result_sentence)
    

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("vdomos:setChaconOff", subscribe_intent_callback) \
         .start()
