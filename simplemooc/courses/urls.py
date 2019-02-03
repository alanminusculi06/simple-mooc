from django.urls import include, path
from simplemooc.courses import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('inscricao/<slug:slug>/', views.enrollment, name='enrollment'),
]