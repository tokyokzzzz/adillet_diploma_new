from django.urls import path
from . import views

urlpatterns = [
    path("", views.conversation_list, name="conversation_list"),
    path("<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("<int:pk>/accept/", views.accept_chat, name="accept_chat"),
    path("<int:pk>/decline/", views.decline_chat, name="decline_chat"),
    path("<int:pk>/send/", views.send_message, name="send_message"),
    path("<int:pk>/poll/", views.poll_messages, name="poll_messages"),
    path("start/<int:mentor_pk>/", views.start_chat, name="start_chat"),
]
