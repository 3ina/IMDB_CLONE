from django.urls import path, include
from watchlist_app.api.views import \
    WatchListV, WatchDetail, StreamPlatformList, \
    StreamPlatformDetail, ReviewList, ReviewDetail ,\
    ReviewCreate ,StreamPlatformVS

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')

urlpatterns = [
    path('WatchList/', WatchListV.as_view(), name='movie-list'),
    path('WatchList/<int:pk>', WatchDetail.as_view(), name='movie-detail'),

    path('',include(router.urls)),
    # path('stream/', StreamPlatformList.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetail.as_view(), name='stream-detail'),

    path('stream/<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review', ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),

]
