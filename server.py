import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc
import requests

class Greeter(service_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # Create a new user in MongoDB
        #user_id = create_user(request.name)
        myobj = {'name': request.name}
        response = requests.post("http://127.0.0.1:8000/api/users/create/", json = myobj)
        
        # Respond with a greeting message
        return service_pb2.HelloResponse(message=f"Hello, {request.name}! (User ID: {response.text})")

    def SayGoodbye(self, request, context):
        # Find the user in MongoDB by name
        #user = find_user(request.name)
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
