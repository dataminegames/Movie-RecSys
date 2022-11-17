from django.urls import path
from . import views

app_name = 'recsys'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/vote/', views.vote, name='vote'),
    path('<int:user_id>/result/', views.result, name='result'),
]
