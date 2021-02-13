from django.urls import path
from . import views
from django.conf.urls import url

app_name = "main"


urlpatterns = [
	path('register/', views.registerview, name="register"),
	path('', views.loginview, name="login"),
	path('logout/', views.logoutview, name="logout"),
	path('welcome/', views.Dashboardview.as_view(), name="welcome"),
	path('article/', views.CreateArticleview.as_view(), name="article"),
	path('search/', views.SearchResview.as_view(), name="searchresults"),
]