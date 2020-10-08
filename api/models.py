from django.db import models
from django.contrib.auth.models import User



class Chat(models.Model):
    user = models.ManyToManyField(User,related_name="users_chats", verbose_name="Пользователи чата", blank=True)
    name = models.CharField(max_length=150,null=True, blank=True)
    numberOfPeople=models.IntegerField(null=True,blank=True,default=1)

class Message(models.Model):
    chat =models.ForeignKey(Chat,on_delete=models.CASCADE,verbose_name="Сообщения в этом чате")
    text=models.TextField("Текст сообщения", null=True, blank=True)
    data = models.DateTimeField("Время отправки", null=True, blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Сообщения этого пользователя")


class UserState(models.Model):
    user = models.OneToOneField(User,related_name="user_state", on_delete=models.CASCADE)  # Each task is owned by one user
    state = models.IntegerField(null=True, blank=True)


class UserInformation(models.Model):
    user = models.OneToOneField(User,related_name="user_info", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    surname = models.CharField(max_length=100,null=True, blank=True)
    birthdate = models.CharField(max_length=100,null=True, blank=True)

