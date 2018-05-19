from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index' ),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='oglasnik/login.html'),
        name='login' ),
    url(r'^userRegistration/$', views.registerUser, name='userRegistration'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    url(r'^chpass/$', auth_views.PasswordChangeView.as_view(
        template_name="oglasnik/chpass.html",
        success_url='../chpassdone'), name='chpass'),
    url(r'^chpassdone/$', auth_views.PasswordChangeDoneView.as_view(
        template_name="oglasnik/chpassdone.html"), name='chpassdone'),
    url(r'^([0-9]+)/$', views.adDetails, name='adDetails' ),
    url(r'^newAd/$', views.createNewAd, name='newAd' ),
    url(r'^modifyCategories/$', views.modifyCategories, name='modifyCategories' ),
]
