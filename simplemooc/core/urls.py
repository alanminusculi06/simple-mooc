from django.urls import include, path
from simplemooc.core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
]