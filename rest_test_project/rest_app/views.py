from django.views.generic.edit import FormView, View
from rest_test_project.rest_app.forms.GoogleForms import GoogleForm
from django.http import JsonResponse, HttpResponse
from datetime import datetime

# Create your views here.


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
        response = [
            {'userId': "bot",
             'name': "Bot",
             'status': True,
             'info': "Blip Blop",
             'picture': 'bot.png'
             },
            {'userId': "asdhakdh",
                   'name': "Marco",
                   'status': True,
                   'info': "I'm a magic pro",
                   'picture': 'avatar.jpg'
                   }]
        return JsonResponse(response)

    def post(self, request, user_id):
        return HttpResponse(status=200)
