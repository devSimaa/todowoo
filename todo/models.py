from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=600)
    created = models.DateTimeField(auto_now_add=True)
    datacompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title