from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^authenticate/',views.get_token, name='authenticate'),
	url(r'^register/$', views.register, name='register'),
	url(r'^forgotpassword/$', views.forgot_password, name='forgotpassword'),
	url(r'^addshow/$', views.new_tvshow, name='addshow'),
	url(r'^addsmashup/$', views.add_smashup, name='addsmashup'),
	url(r'^allsmashups/$', views.all_smashups, name='allsmashups'),
	url(r'^mysmashups/$', views.my_smashups, name='mysmashups'),
	url(r'^mytvshows/$', views.my_tvshows, name='mytvshows'),
	url(r'^searchshows/$', views.search_tvshows, name='searchshows'),
]
