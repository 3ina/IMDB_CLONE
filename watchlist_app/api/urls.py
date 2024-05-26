from django.urls import path
from watchlist_app.api.views import \
    WatchList , WatchDetail ,StreamPlatformList ,\
    StreamPlatformDetail , ReviewList

urlpatterns = [
    path('WatchList/',WatchList.as_view(),name='movie-list'),
    path('WatchList/<int:pk>',WatchDetail.as_view(),name='movie-detail'),
    path('stream/',StreamPlatformList.as_view(),name='stream-list'),
    path('stream/<int:pk>', StreamPlatformDetail.as_view(), name='stream-detail'),
    path('review/',ReviewList.as_view(),name='review-list')

]