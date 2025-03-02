import grpc
import service_pb2 as service_pb2
import service_pb2_grpc as service_pb2_grpc
import auth_pb2 as auth_pb2
import auth_pb2_grpc as auth_pb2_grpc

AUTH_SERVER_IP = "127.0.0.1"    #86.50.231.25
SENSOR_SERVER_IP = "127.0.0.1"  #86.50.231.25

def authenticate(username, password):
    """ Get a JWT token from the authentication service. """
    try:
        auth_channel = grpc.insecure_channel(f"{AUTH_SERVER_IP}:50052")
        auth_stub = auth_pb2_grpc.AuthServiceStub(auth_channel)
        
        auth_request = auth_pb2.LoginRequest(username=username, password=password)
        auth_response = auth_stub.Login(auth_request)
        print(auth_response)

        if auth_response.access_token:
            print(f"✅ Authentication successful!✍️(◔◡◔) Received Token: {auth_response.access_token[:10]}...")  # Hide full token
            return auth_response.access_token
        else:
            print("❌ Authentication failed (´。＿。｀): Invalid credentials.")
            return None
    except Exception as e:
        print(f"⚠️ Error connecting to Auth Service ╚(•⌂•)╝: {e}")
        return None


def run(user_query, token):
    # Create a channel to the server
    with grpc.insecure_channel(f"{AUTH_SERVER_IP}:50051") as channel:#127.0.0.1 #
        stub = service_pb2_grpc.SmartFactoryStub(channel)

        response = stub.Factory(service_pb2.FactoryRequest(user_query=user_query, token=token))
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
    username = input("Enter username: ")
    password = input("Enter password: ")

    token = authenticate(username, password)
    if token:
        print("authentication ok")
        user_query = input("Enter user query: ")
        run(user_query=user_query, token=token)
        next = input("\nDo you want to ask another question? (y/n): ")
        while (next == "y"):
            user_query2 = input("\nEnter user query: ")
            run(user_query=user_query2, token=token)
            next = input("\nDo you want to ask another question? (y/n): ")
                  
