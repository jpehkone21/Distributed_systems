# users/urls.py
from django.urls import path
from .views import UserCreateView, UserRetrieveByIdView, UserRetrieveByNameView, UserListView, UserUpdateView, UserDeleteView, Index

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path('users/', UserListView.as_view(), name='user-list'),  # GET all users
    path('users/create/', UserCreateView.as_view(), name='user-create'),  # POST a new user
    path('users/id/<str:user_id>/', UserRetrieveByIdView.as_view(), name='user-retrieve-by-id'),  # GET a specific user by id
    path('users/name/<str:name>/', UserRetrieveByNameView.as_view(), name='user-retrieve-by-name'),  # GET a specific user by name
    path('users/<str:user_id>/update/', UserUpdateView.as_view(), name='user-update'),  # PUT update user
    path('users/<str:user_id>/delete/', UserDeleteView.as_view(), name='user-delete'),  # DELETE user
]
