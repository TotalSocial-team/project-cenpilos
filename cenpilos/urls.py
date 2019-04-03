from django.urls import path, re_path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # register
    path('register/', RegisterView.as_view(), name='register'),

    # login
    path('login/', auth_views.LoginView.as_view(template_name='cenpilos/auth/pages/login.html', extra_context={
            'login': 'active',
            'title': 'Login | Cenpilos Public'

    })
         , name="login"),

    # logout
    # TODO: set the template url
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # notifications
    path('notifications/', NotificationView.as_view(), name='notifications'),

    # activation
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
            name='activate'),

]
