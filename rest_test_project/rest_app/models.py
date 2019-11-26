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

    def __str__(self):
        return 'Address: ' + self.user.first_name + " - " + self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'user'], name="unique_address_book")]


class ContactAddressBook(models.Model):
    """
    A model that represents a contact in an address book. Must be one of the users.
    """
    address_book = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    contact_user = models.ForeignKey(UserContact, on_delete=models.CASCADE)

    def __str__(self):
        return self.address_book.__str__() + " -- " + self.contact_user.first_name

    class Meta:
        constraints = [models.UniqueConstraint(fields=['address_book', 'contact_user'], name="unique_contact")]


class Chat(models.Model):
    name = models.CharField(max_length=100)
    recipients = models.ManyToManyField(UserContact)


class Message(models.Model):
    """
    A model that represents a message.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    date = models.DateTimeField()
    sender = models.ForeignKey(UserContact, on_delete=models.CASCADE)

    def __str__(self):
        return self.message.__str__() + " -- " + self.contact.address_book.name
