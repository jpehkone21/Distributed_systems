# users/urls.py
from django.urls import path
from .views import UserCreateView, UserListView, UserUpdateView, UserDeleteView, Index

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path('users/', UserListView.as_view(), name='user-list'),  # GET all users
    path('users/create/', UserCreateView.as_view(), name='user-create'),  # POST a new user
    #path('users/<str:user_id>/', UserRetrieveView.as_view(), name='user-retrieve'),  # GET a specific user
    path('users/<str:user_id>/update/', UserUpdateView.as_view(), name='user-update'),  # PUT update user
    path('users/<str:user_id>/delete/', UserDeleteView.as_view(), name='user-delete'),  # DELETE user
]
