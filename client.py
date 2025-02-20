import grpc
import service_pb2
import service_pb2_grpc

def run():
    # Create a channel to the server
    with grpc.insecure_channel('127.0.0.1:50051') as channel:# #86.50.231.25
        stub = service_pb2_grpc.SmartFactoryStub(channel)

        response = stub.Factory(service_pb2.FactoryRequest(user_query="what is humidity in factory"))
        print(f"Response: {response.response_message}")
        
        # Call the SayHello method
        # This request adds a new user to the database
        #hello_request = service_pb2.HelloRequest(name="martti2")
        #hello_response = stub.SayHello(hello_request)
        #print("Server responded to SayHello: " + hello_response.message)
        '''
        # Call the SayGoodbye method
        # This request finds the user from the database
        goodbye_request = service_pb2.GoodbyeRequest(name="kissa")
        goodbye_response = stub.SayGoodbye(goodbye_request)
        print("Server responded to SayGoodbye: " + goodbye_response.message)
        '''
if __name__ == '__main__':
    run()
