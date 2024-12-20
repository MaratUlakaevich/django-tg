from django.db import models
from django.contrib.auth.models import User
import uuid

class TelegramToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.token)
