import grpc
from concurrent import futures

import service_pb2
import service_pb2_grpc
import requests
from kafka import KafkaProducer
#import prometheus_client
from prometheus_client import Counter, Histogram, start_http_server
import paho.mqtt.client as paho
from paho import mqtt
import asyncio

import auth_pb2 as auth_pb2
import auth_pb2_grpc  as auth_pb2_grpc# Import the authentication service
#from authentication import auth_pb2 as auth_pb2
#from authentication import auth_pb2_grpc as auth_pb2_grpc

AUTH_SERVER_IP = "127.0.0.1"
# Connect to Auth Microservice
auth_channel = grpc.insecure_channel(f"{AUTH_SERVER_IP}:50052")
auth_stub = auth_pb2_grpc.AuthServiceStub(auth_channel)

mqtt_response_future = None

REQUEST_COUNT = Counter('grpc_requests_total', 'Total gRPC Requests', ['method', 'status'])
RESPONSE_TIME = Histogram('grpc_response_time_seconds', 'gRPC Response Time', ['method'])

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc)
    client.subscribe("smart_factory/response")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    global mqtt_response_future

    response_data = msg.payload.decode()

    # If there's a pending gRPC request, resolve it
    if mqtt_response_future and not mqtt_response_future.done():
        mqtt_response_future.set_result(response_data)


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
client.loop_start()

print("Connected to broker!")

'''
# Initialize the producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka broker address
    value_serializer=lambda v: v.encode('utf-8')  # Serialize string data to bytes
)
'''
# Store pending requests
pending_requests = {}


class SmartFactory(service_pb2_grpc.SmartFactoryServicer):
    def SayHello(self, request, context):
        with RESPONSE_TIME.labels(method="SayHello").time():
            REQUEST_COUNT.labels(method="SayHello", status="success").inc()
            print(f"received sayHello request from {request.name}")
            # Use REST api to add new user to mongodb
            myobj = {'name': request.name}
            response = requests.post("http://127.0.0.1:8000/api/users/create/", json = myobj)
            print(f"got a response from crud api: {response.text}")
            
            #  HERE send(publish) message to kafka broker that new user is added
            #  Kafka consumer(subscriber) can then do something with that information
            # Send a message to the topic
            print("sending message to kafka broker")
            message_to_kafka = f"Received request from client named {request.name}"
            #producer.send('test-topic', value=message_to_kafka)
            #producer.flush()  # Ensure all messages are sent before closing
            #producer.close()

            # Respond with a greeting message
            return service_pb2.HelloResponse(message=f"Hello, {request.name}! (User ID: {response.text})")

    async def Factory(self, request, context):
        # Validate token with the Auth Microservice
        auth_response = auth_stub.ValidateToken(auth_pb2.ValidateRequest(token=request.token))
        if not auth_response.valid:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid token")
            return service_pb2.FactoryResponse(data="")

        global mqtt_response_future

        # Create a new future to wait for the MQTT response
        mqtt_response_future = asyncio.Future()

        # Publish the received string to the MQTT request topic
        client.publish("smart_factory/request", payload=request.user_query, qos=0)
        print("published: " + request.user_query)

        # Wait for the MQTT response (with timeout)
        try:
            response_message = await asyncio.wait_for(mqtt_response_future, timeout=10)
        except asyncio.TimeoutError:
            return service_pb2.FactoryResponse(response_message="Timeout waiting for MQTT response")

        return service_pb2.FactoryResponse(response_message=response_message)


async def serve():
    server = grpc.aio.server()
    service_pb2_grpc.add_SmartFactoryServicer_to_server(SmartFactory(), server)
    #prometheus_client.start_http_server(8001)  # Metrics exposed at http://localhost:8001/metrics
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC Server Started")
    await server.wait_for_termination()
    '''
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)
    '''
if __name__ == '__main__':
    #serve()
    asyncio.run(serve())
