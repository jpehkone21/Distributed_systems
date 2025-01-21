import grpc
import service_pb2
import service_pb2_grpc

def run():
    # Create a channel to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GreeterStub(channel)
        
        # Call the SayHello method
        hello_request = service_pb2.HelloRequest(name="Bob")
        hello_response = stub.SayHello(hello_request)
        print("Server responded to SayHello: " + hello_response.message)
        
        # Call the SayGoodbye method
        goodbye_request = service_pb2.GoodbyeRequest(name="Bob")
        goodbye_response = stub.SayGoodbye(goodbye_request)
        print("Server responded to SayGoodbye: " + goodbye_response.message)

if __name__ == '__main__':
    run()
