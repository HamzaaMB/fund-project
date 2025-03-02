from django.urls import path
from .views import FundListAPI, FundDetailAPI

urlpatterns = [
    path('funds/', FundListAPI.as_view(), name='fund-list-api'),
    path('funds/<uuid:pk>/', FundDetailAPI.as_view(), name='fund-detail-api'), 
]
