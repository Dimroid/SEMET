from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat, Message
from .forms import MessageForm
from django.contrib import messages

@login_required
def reply_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    recipient = original_message.sender

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = recipient
            reply.save()

            chat, created = Chat.objects.get_or_create(
                participants__in=[request.user], 
                defaults={'participants': [request.user, recipient]}
            )
            if not created and not chat.participants.filter(id=recipient.id).exists():
                chat.participants.add(recipient)

            chat.messages.add(reply)
            messages.success(request, 'Reply sent successfully')
            # return redirect('messaging:chat_history', username=recipient.username)
    else:
        form = MessageForm(initial={'recipient': recipient})  # Initialize form with recipient
    return render(request, 'messaging/reply_message.html', {'form': form, 'recipient': recipient, 'original_message': original_message, 'section':'messaging'})


@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'received_messages': received_messages, 'section':'messaging'})

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'sent_messages': sent_messages, 'section':'messaging'})

@login_required
def send_message(request, username):
    recipient = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()

            # Get or create the chat between the sender and recipient
            chat, created = Chat.objects.get_or_create(participants__in=[request.user, recipient])
            if created:
                chat.participants.set([request.user, recipient])  # Use set() to assign participants

            chat.messages.add(message)

            messages.success(request, 'Message sent successfully')
            # return redirect('messaging:chat_history', username=username)
    else:
        form = MessageForm(initial={'recipient': recipient})
    return render(request, 'messaging/send_message.html', {'form': form, 'recipient': recipient, 'section': 'messaging'})

@login_required
def chat_history(request, username):
    recipient = get_object_or_404(User, username=username)
    chat = Chat.objects.filter(participants__in=[request.user]).filter(participants__in=[recipient]).first()
    messages = chat.messages.all() if chat else []
    return render(request, 'messaging/chat_history.html', {'messages': messages, 'recipient': recipient, 'section':'messaging'})