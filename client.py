import grpc
import service_pb2
import service_pb2_grpc

def run():
    # Create a channel to the server
    with grpc.insecure_channel('127.0.0.1:50051') as channel:#86.50.231.25
        stub = service_pb2_grpc.GreeterStub(channel)

        # Test GetTemperature method
        response = stub.GetTemperature(service_pb2.TemperatureRequest(location="New York"))
        print(f"Simulated Temperature in New York: {response.temperature}°C")
        
        # Call the SayHello method
        # This request adds a new user to the database
        hello_request = service_pb2.HelloRequest(name="kissa")
        hello_response = stub.SayHello(hello_request)
        print("Server responded to SayHello: " + hello_response.message)
        '''
        # Call the SayGoodbye method
        # This request finds the user from the database
        goodbye_request = service_pb2.GoodbyeRequest(name="kissa")
        goodbye_response = stub.SayGoodbye(goodbye_request)
        print("Server responded to SayGoodbye: " + goodbye_response.message)
        '''
if __name__ == '__main__':
    run()
