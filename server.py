import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc
import requests
from kafka import KafkaProducer

# Initialize the producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka broker address
    value_serializer=lambda v: v.encode('utf-8')  # Serialize string data to bytes
)

class Greeter(service_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
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
        producer.send('test-topic', value=message_to_kafka)
        producer.flush()  # Ensure all messages are sent before closing
        #producer.close()

        # Respond with a greeting message
        return service_pb2.HelloResponse(message=f"Hello, {request.name}! (User ID: {response.text})")

    def SayGoodbye(self, request, context):

        # use REST api to find the user in MongoDB by name
        response = requests.get("http://127.0.0.1:8000/api/users/name/" + request.name + "/")
        
        if response.ok:
            return service_pb2.GoodbyeResponse(message=f"Goodbye, {response.text}!")
        else:
            return service_pb2.GoodbyeResponse(message="User not found!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    
    # Start the server on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
