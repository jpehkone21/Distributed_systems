import json
import numpy as np
import paho.mqtt.client as paho
from paho import mqtt

# MQTT Configuration
BROKER = "04bae4d7b8034393b71c90e9cacea240.s1.eu.hivemq.cloud"
TOPIC = "smart_factory/motor1"
MQTT_PORT = 8883
MQTT_USERNAME = "sensor"
MQTT_PASSWORD = "Sensor123"

# Acceptable value ranges
RANGES = {
    "temperature": (50, 100),
    "speed": (1000, 5000),
    "torque": (10, 50)
}

def is_anomaly(value: float, min_val: float, max_val: float) -> bool:
    return value < min_val or value > max_val

def detect_anomalies(data: dict):
    anomalies = {key: value for key, value in data.items() if key in RANGES and is_anomaly(value, *RANGES[key])}
    return anomalies

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    anomalies = detect_anomalies(payload)
    if anomalies:
        print(f"Anomaly detected! Data: {payload} - Anomalies: {anomalies}")

# MQTT Client Setup
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)#
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(BROKER, MQTT_PORT)
client.subscribe(TOPIC)
client.on_message = on_message
client.loop_forever()
