from django.conf.urls import url
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
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # handling a post like
    path('like/', like_post, name='like_post'),

    # handling a post dislike
    path('dislike/', dislike_post, name='dislike_post'),

    # handling a post deletion
    path('remove_post/', delete_post, name='delete_post'),

    path('login-beta/', login_beta, name='login-beta'),

    # profile page
    url(r'profile/(?P<username>[a-zA-Z0-9]+|)$',  ProfileView.as_view(), name='profile'),

    # notifications
    path('notifications/', NotificationView.as_view(), name='notifications'),

    # friend addition lol -- I wish this was this easy in real life :(
    url(r'add_friend/(?P<username>[a-zA-Z0-9]+)', add_friend, name='add_friend'),

    # friend deletion LOL -- I wish deleting people that USE me like this :(
    url(r'remove_friend/(?P<username>[a-zA-Z0-9]+)', remove_friend, name='remove_friend'),

    # # activation
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
    #         name='activate'),

]
