import json

from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, View
from rest_test_project.rest_app.forms.GoogleForms import GoogleForm
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from .models import ContactAddressBook, UserContact
from django.contrib.auth import authenticate, login
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
            return JsonResponse({"status": "Authenticated"})
        return JsonResponse({"status": "Invalid login"})


class GoogleSearchView(FormView):

    template_name = 'google_search_template_form.html'
    form_class = GoogleForm
    success_url = ''

    '''def get(self, request):
        return HttpResponse("Hello!")

    def post(self, request):
        query = request.POST.get("question")
        search_result_list = list(search(query, tld="co.in", num=10, stop=3, pause=1))
        return JsonResponse(search_result_list, safe=False)
    '''


class UserMessagesView(View):

    def get(self, request, user_id):
        message = {'body': "Hey, how's it going?",
                   'date': datetime.now().strftime("%d/%m/%Y %HH:%mm:%ss")}
        return JsonResponse(message)

    def post(self, request, user_id):
        return HttpResponse(status=200)


class ContactsView(View):

    def get(self, request):
        """

        :param request:
        :return: JSON object of contacts. Contacts is a list of objects
                with following keys: userId, name, status, info, picture
        """
        contact_keys = ["id", "first_name", "status", "info", "picture"]
        response = {"contacts":[
            {'id': "bot",
             'first_name': "Bot",
             'status': True,
             'info': "Blip Blop",
             'picture': 'bot.jpg'
             }]}
        query1 = ContactAddressBook.objects.filter(address_book__user=request.user)
        users = UserContact.objects.filter(contactaddressbook__in=query1).values(*contact_keys)
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

    def post(self, request, user_id):
        return HttpResponse(status=200)
