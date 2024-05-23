from django.urls import path
from watchlist_app.api.views import WatchList , WatchDetail

urlpatterns = [
    path('list/',WatchList.as_view(),name='movie-list'),
    path('<int:pk>',WatchDetail.as_view(),name='movie-detail'),
]