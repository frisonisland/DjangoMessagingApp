from django.contrib import admin
from .models import UserContact, AddressBook, ContactAddressBook

# Register your models here.

admin.site.register(UserContact)
admin.site.register(AddressBook)
admin.site.register(ContactAddressBook)
