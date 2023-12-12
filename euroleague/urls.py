from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('teams/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('profilis/', views.profilis, name='profilis'),
    path('predict/', views.predict_view, name='predict'),
    path('prediction-result/', views.prediction_result_view, name='prediction_result'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
