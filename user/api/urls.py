from django.urls import path
from user.api import views
urlpatterns = [
    path('register/',views.registration_view,name="register"),

]
