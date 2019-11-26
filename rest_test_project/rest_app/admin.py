from django.contrib import admin
from .models import UserContact, AddressBook, ContactAddressBook, Message

# Register your models here.

admin.site.register(UserContact)
admin.site.register(AddressBook)
admin.site.register(ContactAddressBook)
admin.site.register(Message)
