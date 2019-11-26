from django.contrib import admin
from .models import UserContact, AddressBook, ContactAddressBook, Message, Chat

# Register your models here.

admin.site.register(UserContact)
admin.site.register(AddressBook)
admin.site.register(ContactAddressBook)
admin.site.register(Message)
admin.site.register(Chat)
