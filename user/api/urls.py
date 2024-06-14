from django.urls import path
from user.api import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
urlpatterns = [
    path('register/',views.registration_view,name="register"),
    path('logout/',views.logout_view,name="logout"),
    path('token/',TokenObtainPairView.as_view(),name="token_obtain_view"),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh_view'),

]
