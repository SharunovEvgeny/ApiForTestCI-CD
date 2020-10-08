from django.contrib import admin
from .models import Chat, Message, UserState, UserInformation


@admin.register(Chat,Message,UserState,UserInformation)
class PersonAdmin(admin.ModelAdmin):
    pass
# Register your models here.
