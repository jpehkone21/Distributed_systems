# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import create_user, get_user, get_all_users, update_user, delete_user
from .serializers import UserSerializer
from django.http import HttpResponse

class Index(APIView):
    def get(self, request):
        return HttpResponse("Hello, world. here is something...")
    
class UserCreateView(APIView):
    def post(self, request):
        name = request.data.get("name")
        if name:
            user_id = create_user(name)
            return Response({"id": user_id, "name": name}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    def get(self, request):
        users = get_all_users()
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)

'''
class UserRetrieveView(APIView):
    def get(self, request, user_id):
        user = get_user_by_id(user_id)
        if user:
            serialized_user = UserSerializer(user)
            return Response(serialized_user.data)
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
'''

class UserUpdateView(APIView):
    def put(self, request, user_id):
        new_name = request.data.get("name")
        if new_name and update_user(user_id, new_name):
            return Response({"message": "User updated successfully."})
        return Response({"detail": "User not found or invalid data."}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    def delete(self, request, user_id):
        if delete_user(user_id):
            return Response({"message": "User deleted successfully."})
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
