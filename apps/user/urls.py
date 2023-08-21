from django.urls import path

from .views import ListCreateProfileView

app_name='user'

urlpatterns =[
    path('profile/', ListCreateProfileView.as_view(), name='list_create_profile')
]
