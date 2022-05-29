from django.urls import path

from . import views

app_name = 'ml_api'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/predictions', views.upload_file_view, name='upload-predictions')
]
