from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    author = models.ForeignKey(User)
    post_date = models.DateTimeField(max_length=30)
    content = models.CharField(max_length=42)