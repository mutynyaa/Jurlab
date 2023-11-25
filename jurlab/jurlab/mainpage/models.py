from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title=models.CharField(max_length=200)
    text=models.TextField()
     
    def __str__(self):
        return self.title
    
class Supervisor(models.Model):
    title=models.CharField(max_length=200)
    court_author_vision = models.BooleanField(default=False)
    ex_author_vision = models.BooleanField(default=False)
     
    def __str__(self):
        return self.title




