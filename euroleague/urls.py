from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# Define URL patterns for the app
urlpatterns = [
    path('', views.index, name='index'),
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('teams/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('predict/', views.predict_view, name='predict'),
    path('prediction-result/', views.prediction_result_view, name='prediction_result'),
]
# Include default authentication views provided by Django
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
