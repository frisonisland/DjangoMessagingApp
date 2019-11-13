from django.urls import path
from rest_test_project.rest_app.views import GoogleSearchView, ContactsView, UserMessagesView

urlpatterns = [
    path('', GoogleSearchView.as_view()),
    path('messages/<slug:user_id>/', UserMessagesView.as_view()),
    path('contacts/', ContactsView.as_view())
]