from django.urls import include, path
from simplemooc.forum import views as v

app_name = 'forum'

urlpatterns = [
    path('', v.index, name='index'),    
    path('tag/<str:tag>/', v.index, name='index_tagged'),
    path('topico/<slug:slug>/', v.thread, name='thread'),
]