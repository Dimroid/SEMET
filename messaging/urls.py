from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('chat_history/<str:username>/', views.chat_history, name='chat_history'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent_messages/', views.sent_messages, name='sent_messages'),
    path('reply_message/<int:message_id>/', views.reply_message, name='reply_message'),
]