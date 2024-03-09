from django.db import models
from django.contrib.auth.models import User



class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    label = models.TextField(max_length=200)
    last_message = models.TextField(default="No Last Message Found.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,)
    query = models.TextField(default="No Query Passed")
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


