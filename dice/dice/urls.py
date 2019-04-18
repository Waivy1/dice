
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index_page'),
    path('result_for_one', views.ResultForOne.as_view(), name='result_for_one'),
    path('second_page', views.SecondPage.as_view(), name='second_page'),
    path('result_for_two', views.ResultForTwo.as_view(), name='result_for_two'),
    path('sign_up', views.SignUp.as_view(), name='sign_up'),
    path('sign_in', views.SignIn.as_view(), name='sign_in'),
    path('exit', views.Exit.as_view(), name='exit'),
]
