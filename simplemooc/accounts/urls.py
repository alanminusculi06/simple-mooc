from django.urls import include, path
from django.contrib.auth import views as auth_views
from simplemooc.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('editar/', views.edit, name='edit'),
    path('senha/', views.edit_password, name='edit_password'),
    path('redefinir/', views.password_reset, name='password_reset'),
    path('novasenha/<str:key>/', views.password_reset_confirm, name='password_reset_confirm'),
]
