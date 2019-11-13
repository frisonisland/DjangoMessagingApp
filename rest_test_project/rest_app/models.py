from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.


class UserContact(AbstractUser):
    info = models.TextField(blank=True)
    picture = models.CharField(max_length=255, default="avatar.png")
    status = models.BooleanField(default=False)


class AddressBook(models.Model):
    """
    A model that represents an address book for a user
    """
    name = models.CharField(max_length=100, default="Main")
    user = models.OneToOneField(UserContact, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'user'], name="unique_address_book")]


class ContactAddressBook(models.Model):
    """
    A model that represents a contact in an address book. Must be one of the users.
    """
    address_book = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    contact_user = models.ForeignKey(UserContact, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['address_book', 'contact_user'], name="unique_contact")]


class Chat(models.Model):
    """
    A model that represents a chat. A chat name must be unique for eacher user. Chats can have multiple contacts (group chat).
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(UserContact, on_delete=models.CASCADE)
    contacts = models.ForeignKey(ContactAddressBook, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'user'], name="unique_user_chat_name")]
