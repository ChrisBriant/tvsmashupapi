from django.conf.urls import url
from . import views

urlpatterns = [
	#Authenticate to be taken out after testing /autneticate which has the custom claims
	url(r'^authenticate/',views.get_token, name='authenticate'),
	url(r'^register/$', views.register, name='register'),
	url(r'^forgotpassword/$', views.forgot_password, name='forgotpassword'),
	url(r'^addshow/$', views.new_tvshow, name='addshow'),
	url(r'^addsmashup/$', views.add_smashup, name='addsmashup'),
	url(r'^allsmashups/$', views.all_smashups, name='allsmashups'),
	url(r'^mysmashups/$', views.my_smashups, name='mysmashups'),
	url(r'^mytvshows/$', views.my_tvshows, name='mytvshows'),
	url(r'^searchshows/$', views.search_tvshows, name='searchshows'),
	url(r'^search/$', views.search, name='search'),
	url(r'^showsindexed/$', views.shows_index, name='showsindexed'),
	url(r'^getsmashup/$', views.get_smashup, name='getsmashup'),
	url(r'^addrating/$', views.add_rating, name='addrating'),
	url(r'^updatecategories/$', views.update_categories, name='updatecategories'),
]
