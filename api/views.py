import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
# More rest imports as needed
from django.contrib.auth import authenticate
from datetime import date, timedelta, datetime
from .decorators import define_usage
from .models import  Chat, UserState, Message,UserInformation
from .serializers import *


#URL /
@define_usage(returns={'url_usage': 'Dict'})
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_index(requet):
    details = {}
    for item in list(globals().items()):
        if item[0][0:4] == 'api_':
            if hasattr(item[1], 'usage'):
                details[reverse(item[1].__name__)] = item[1].usage
    return Response(details)


#URL /registration/
@define_usage(params={'name':'String','surname':'String','username': 'String', 'password': 'String','birthdate':'String'},
              returns={'Registration': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_registration(request):
    try:
        username = request.data['username']
        password = request.data['password']
        name = request.data['name']
        surname = request.data['surname']
        birthdate= request.data['birthdate']
    except:
        return Response({'error': 'Пожалуйста введите все поля'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(username=username,password=password)
        user.save()
        info = UserInformation.objects.create(user=user,surname=surname,name=name,birthdate=birthdate)
        info.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'Registration': True, 'token': "Token " + token.key},status=HTTP_201_CREATED)
    except:
       return Response({'error': 'Это имя пользователя уже занято'})


#URL /signin/
#Note that in a real Django project, signin and signup would most likely be
#handled by a seperate app. For signup on this example, use the admin panel.
@define_usage(params={'username': 'String', 'password': 'String'},
              returns={'authenticated': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signin(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except:
        return Response({'error': 'Пожалуйста введите логин и пароль'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response({'authenticated': False, 'token': None})


#URL /getAllChatByUser/
@define_usage(
    returns={'сhats': 'Dict'})
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_getAllChatByUser(request):
    try:
        user=request.user
    except:
        return Response({'error': 'Таких пользователей не существует'},
                        status=HTTP_400_BAD_REQUEST)
    chat = Chat.objects.all().filter(user=user)
    chat = chatSerializer(chat, many=True)
    return Response({'chats': chat.data})



#URL /createChat/
@define_usage(params={'name': 'String'},
              returns={'chatId': 'Int'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_createChat(request):
    try:
        chat=Chat.objects.create(name=request.data['name'],numberOfPeople=1)
        chat.user.add(request.user)
        chat.save()
    except:
        return Response({'error': 'Введите имя чата'},
                        status=HTTP_400_BAD_REQUEST)
    return Response({'chatId': chat.id})


#URL /users/
@define_usage(returns={'users': 'Dict'})
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_users(request):
    users = userSerializer(User.objects.all(), many=True)
    return Response({'users': users.data})


#URL /getMessagesByChatId/
@define_usage(params={'chatId': 'Int'},returns={'messages': 'Dict'})
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_getMessagesByChatId(request):
    messages=Message.objects.all().filter(chat=Chat.objects.get(id=request.data['chatId']))[:100]
    messages = messageSerializer(messages, many=True)
    return Response({'messages': messages.data})



#URL /createMessage/
@define_usage(params={'chatId':'Int','text': 'String'},
              returns={'done': 'Bool'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_createMessage(request):
    try:
        message=Message.objects.create(user=request.user,chat=Chat.objects.get(id=request.data['chatId']),text=request.data['text'],data=datetime.now())
        message.save()
    except:
        return Response({'error': 'Такого чата нет'},
                        status=HTTP_400_BAD_REQUEST)
    return Response({'done': True})



#URL /addUserToChatByUsername/
@define_usage(params={'chatId':'Int','username': 'String'},
              returns={'done': 'Bool'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_addUserToChatByUsername(request):
    try:
        chat = Chat.objects.get(id=request.data['chatId'])

    except:
        return Response({'error': 'Такого чата нет'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user=User.objects.get(username=request.data['username'])
        chat.user.add(user)
        chat.numberOfPeople+=1
        chat.save()
    except:
        return Response({'error': 'Пользователь уже в чате'},
                        status=HTTP_400_BAD_REQUEST)
    return Response({'done': True})


#URL /changeUsername/
@define_usage(params={'name': 'String'},
              returns={'done': 'Bool'})
@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_changeUsername(request):
    user=request.user
    user.username=request.data['name']
    user.save()
    return Response({'done': True})