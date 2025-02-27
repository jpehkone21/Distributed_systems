import grpc
from concurrent import futures
import auth_pb2
import auth_pb2_grpc
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Secret Key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

# Simulated user database
users_db = {
    "kissa": pwd_context.hash("Kissa22") 
}

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Login(self, request, context):

        # Check if the user exists in the database
        if request.username not in users_db:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return auth_pb2.LoginResponse(access_token="")

        # Retrieve the stored hashed password
        stored_hashed_password = users_db[request.username]

        # Verify the provided password against the stored hash
        if not pwd_context.verify(request.password, stored_hashed_password):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return auth_pb2.LoginResponse(access_token="")

        # Generate JWT token with expiration
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": request.username, "exp": expire}
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        print(token)

        return auth_pb2.LoginResponse(access_token=token)

    def ValidateToken(self, request, context):
        try:
            payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            return auth_pb2.ValidateResponse(valid=True, username=username)
        except JWTError:
            return auth_pb2.ValidateResponse(valid=False, username="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50052")  # Auth microservice runs on a different port
    server.start()
    print("Auth gRPC Server is running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
