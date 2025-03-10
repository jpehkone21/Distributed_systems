from openai import OpenAI
import paho.mqtt.client as paho
from paho import mqtt


# Set your API key
openai_api_key = " "

ai_client = OpenAI(
    api_key=openai_api_key,  # This is the default and can be omitted
)

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc)
    client.subscribe("smart_factory/request")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    ai_response = generate_response(msg.payload.decode())
    publish_mqtt(ai_response)


MQTT_BROKER = "04bae4d7b8034393b71c90e9cacea240.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "sensor"
MQTT_PASSWORD = "Sensor123"

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)#
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT)
#client.loop_forever()  # Keeps the client running

print("Connected to broker!")




def generate_response(user_input):
    """
    Generates a response from OpenAI's GPT model using prompt engineering.
    """
    messages = [
        {"role": "system", "content": "You are a smart factory. Answer only what is the state of the asked component."},
        {"role": "user", "content": user_input}
    ]
    
    response = ai_client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if needed
        messages=messages,
        temperature=0.7,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.3
    )

    # Correct way to extract content
    return response.choices[0].message.content


def publish_mqtt(message):

    #client.connect("ssl://localhost", 8883)

    #client.subscribe("encyclopedia/#", qos=1)
    client.publish("smart_factory/response", payload=message, qos=0)
    print("published: " + message)


# Example Usage
if __name__ == "__main__":
    #user_query = "What is the state of motor 1"
    #ai_response = generate_response(user_query)
    #print(ai_response)
    #publish_mqtt(ai_response)
    client.loop_forever()
    


