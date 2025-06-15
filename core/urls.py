from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('ai/', views.ai, name='ai'),
    path('about/', views.about, name='about'),
    path('ai/details/<str:topic>/', views.ai_details, name='ai_details'),
    path('content/', views.content_list, name='content_list'),
    path('content/<slug:slug>/', views.playlist_detail_view, name='playlist_detail'), 
    path('echofortruth/', views.echo_for_truth, name='echo_for_truth'),
]