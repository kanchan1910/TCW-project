from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
   url(r'^admin/', admin.site.urls),
   url('userprofile/', views.profile, name='userprofile'),
   url('signup/', views.signup, name='signup'),
   url('login/', views.login, name='login'),
   url('', views.index, name='index')
]
