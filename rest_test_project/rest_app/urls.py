from django.urls import path
from rest_test_project.rest_app.views import ContactsView, UserMessagesView, LoginView, LogoutView

urlpatterns = [
    path('messages/<slug:user_id>/', UserMessagesView.as_view()),
    path('contacts/', ContactsView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]