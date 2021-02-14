from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^authenticate/',views.get_token, name='authenticate'),
	url(r'^register/$', views.register, name='register'),
	url(r'^forgotpassword/$', views.forgot_password, name='forgotpassword'),
	url(r'^addshow/$', views.new_tvshow, name='addshow'),
	url(r'^addsmashup/$', views.add_smashup, name='addsmashup'),
]
