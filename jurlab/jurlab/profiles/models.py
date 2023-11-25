from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from courts.models import Courts
from django.conf import settings
from django.contrib.sessions.models import Session

class Position(models.Model):
    position = models.CharField(max_length=70, blank=True, null = True)
    
    def __str__(self):
        return self.position
    
class Department(models.Model):
    department = models.CharField(max_length=70, blank=True)
    
    def __str__(self):
        return self.department

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True, default = "Новый пользователь, добавьте информацию в профиль")
    fathers_name = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(blank=True, null = True)
    icq = models.CharField(max_length=30, blank=True)
    skype = models.CharField(max_length=30, blank=True)
    phone_number_job = models.CharField(max_length=30, blank=True, null = True)
    phone_number_home = models.CharField(max_length=30, blank=True, null = True)
    position = models.ForeignKey(Position, on_delete = models.CASCADE, null = True)
    position_date = models.DateField(blank=True, null = True)
    work_is_date = models.DateField(blank=True, null = True)
    department = models.ForeignKey(Department, on_delete = models.CASCADE, null = True)
    avatar = models.ImageField(upload_to='avatars', default = None)
    is_online = models.BooleanField(default=False)
    only_their_courts = models.BooleanField(default=False)
    courts_common_jurisdiction = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            this_record = Profiles.objects.get(id=self.id)
            if this_record.avatar != self.avatar:
                this_record.avatar.delete(save=False)
        except:
            pass
        super(Profiles, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.avatar.delete(save=False)
        super(Profiles, self).delete(*args, **kwargs)

    def __str__(self):
       return "%s  %s" % (self.name, self.surname)
    


class MySession(models.Model):
    session_key = models.CharField(max_length=100)
    user = models.IntegerField()

    def __str__(self):
       return "%s ///////  %s" % (self.session_key, self.user)


