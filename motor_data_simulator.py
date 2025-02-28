import json
import random
import time
import requests
import paho.mqtt.client as paho
from paho import mqtt


# MQTT Configuration
BROKER = "04bae4d7b8034393b71c90e9cacea240.s1.eu.hivemq.cloud"
TOPIC = "smart_factory/motor1"
MQTT_PORT = 8883
MQTT_USERNAME = "sensor"
MQTT_PASSWORD = "Sensor123"

# MQTT Client Setup
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)#
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(BROKER, MQTT_PORT)
client.loop_start()

def generate_motor_data():
    anomaly_chance = random.randint(1, 20)  # 5% chance of anomaly
    if anomaly_chance == 1:
        return {
            "temperature": round(random.uniform(150.0, 200.0), 2),  # Anomalous high temperature
            "speed": random.randint(6000, 8000),  # Anomalous high speed
            "torque": round(random.uniform(60.0, 100.0), 2)  # Anomalous high torque
        }
    else:
        return {
            "temperature": round(random.uniform(50.0, 100.0), 2),  # Celsius
            "speed": random.randint(1000, 5000),  # RPM
            "torque": round(random.uniform(10.0, 50.0), 2)  # Nm
        }

while True:
    data = generate_motor_data()
    
    # Save to JSON file
    #with open("motor_data.json", "w") as file:
        #json.dump(data, file, indent=4)
    
    # Publish to MQTT broker
    client.publish(TOPIC, json.dumps(data))
    print(f"Published: {data}")

    #Adding generated data to mongodb, django server needs to be running, not tested
    #response = requests.post("http://86.50.231.25:8000/api/users/create/", json = data)
    #print(f"got a response from crud api: {response.text}")
    
    time.sleep(5)  # Adjust the interval as needed
