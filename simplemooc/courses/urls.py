from django.urls import include, path
from simplemooc.courses import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('inscricao/<slug:slug>/', views.enrollment, name='enrollment'),
    path('anuncios/<slug:slug>/', views.announcements, name='announcements'),
    path('cancelar-inscricao/<slug:slug>/', views.undo_enrollment, name='undo_enrollment'),
]