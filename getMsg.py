import paho.mqtt.client as mqtt
import json, random, dotenv, os, requests
from pymongo import MongoClient

dotenv.load_dotenv()

DISCORD  = os.getenv('DISCORD')

MQTT_USER  = os.getenv('MQTT_USER')
MQTT_PASSWORD  = os.getenv('MQTT_PASSWORD')
MQTT_HOST  = os.getenv('MQTT_HOST')

MONGO_URI  = os.getenv('MONGO_URI')

mongoc = MongoClient(MONGO_URI)
database = mongoc["projIoT"]
collection = database["mesures"]

# Callback appelé lorsque le client se connecte au broker
def on_connect(client, userdata, flags, reason_code, properties): #(client, userdata, flags, rc):
    print("Connected with result code "+str(reason_code))
    # Abonnement à un topic
    client.subscribe(os.getenv('MQTT_TOPIC'))

# Callback appelé quand un message est reçu du broker
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    print(msg.topic, data.get('received_at'))
    #print(json.dumps(data, indent=2))
    payload=data.get('uplink_message').get('decoded_payload')
    print(json.dumps(payload, indent=2))

    # Sauve le document dans Mongo
    collection.insert_one(data)

    # Envoi notification à Discord
    data = {
        "content" : f"Message reçu : {data.get('uplink_message').get('decoded_payload')}",
        "username" : msg.topic
    }
    if DISCORD: # payload.get('volt')<4.95:
        requests.post(DISCORD, json = data)



# Création d'un client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Configuration du nom d'utilisateur et du mot de passe
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Attribution des fonctions de callback
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect(MQTT_HOST, 1883, 60)

# Boucle pour maintenir le client en écoute des messages
#client.loop_forever()
client.loop_start()
#while True:
#    client.loop()