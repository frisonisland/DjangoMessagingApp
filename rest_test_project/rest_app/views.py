import json

from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, View
from rest_test_project.rest_app.forms.GoogleForms import GoogleForm
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from .models import ContactAddressBook, UserContact, Message, Chat
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
# Create your views here.


class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        authenticated = authenticate(username=username, password=password)
        if authenticated:
            login(request, authenticated)
            return JsonResponse({"token": "Authenticated"})
        return JsonResponse({"token": ""}, status=500)


class LogoutView(View):

    def post(self, request):
        logout(request)
        return JsonResponse({"status": "Logged out"})


class GoogleSearchView(FormView):

    template_name = 'google_search_template_form.html'
    form_class = GoogleForm
    success_url = ''


class ChatView(View):

    def get(self, request):
        response = {"chats": []}
        chats = Chat.objects.filter(recipients__in=[request.user])
        contact_keys = ["id", "first_name", "last_name", "status", "info", "picture"]
        for chat in chats:
            recipients = list(chat.recipients.exclude(pk__in=[request.user.pk]).values(*contact_keys))
            if len(recipients) == 1:
                response["chats"].append({
                    "id": chat.pk,
                    "name": recipients[0]["first_name"],
                    "status": recipients[0]["status"],
                    "info": recipients[0]["info"],
                    "picture": recipients[0]["picture"]
                })
            else:
                response["chats"].append({"id": chat.pk,
                    "name": chat.name,
                    "status": "",
                    "info": "",
                    "picture": ""})

        return JsonResponse(response)


class UserMessagesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserMessagesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, chat_id):
        message_keys=["date","message", "sender__pk"]
        chat = Chat.objects.get(pk=chat_id, recipients__in=[request.user])
        messages = Message.objects.filter(chat=chat).values(*message_keys)
        new_messages = []
        for msg in messages:
            if msg["sender__pk"] == request.user.pk:
                sender = "me"
            else:
                sender = msg["sender__pk"]
            new_messages.append({"body":msg["message"], "date": msg["date"], "sender": sender})
        messages = {"messages": new_messages}
        return JsonResponse(messages)


    def post(self, request, chat_id):
        data = json.loads(request.body)
        message = data.get("message")
        chat = Chat.objects.get(pk=chat_id, recipients__in=[request.user])
        Message.objects.create(chat=chat, sender=request.user, message=message, date=datetime.now())

        return HttpResponse(status=200)


class ContactsView(View):

    def get(self, request):
        """
        :param request:
        :return: JSON object of contacts. Contacts is a list of objects
                with following keys: userId, name, status, info, picture
        """
        contact_keys = ["id", "first_name", "status", "info", "picture"]
        response = {"contacts":[]}
        #get all contacts in user address book
        contacts = ContactAddressBook.objects.filter(address_book__user=request.user)
        #get users in addressbook
        users = UserContact.objects.filter(contactaddressbook__in=contacts).values(*contact_keys)
        response["contacts"] += users
        new_response = []
        # map to correct keys
        for entry in response["contacts"]:
            new_response.append({"userId": entry["id"],
                                 "name": entry["first_name"],
                                 "status": entry["status"],
                                 "info": entry["info"],
                                 "picture": entry["picture"],
                                 })
        response["contacts"] = new_response
        return JsonResponse(response)

