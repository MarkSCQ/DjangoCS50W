
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    path('login', views.login, name="login"),

    path('TestList/<str:message>', views.TestList, name="TestList"),

    path('studentonetest/<str:testid>/<str:idcode>',
         views.StudentOneTest, name="StudentOneTest"),

    path('submitans', views.submitans, name="submitans"),

    path('ReviewTestsList/<str:message>',
         views.ReviewTestsList, name="ReviewTestsList"),

    path('ReviewTestDetails/<str:message>/<str:testname>/<str:gradeid>',
         views.ReviewTestDetails, name="ReviewTestDetails"),

    path('GenerateNewTest/<str:message>',
         views.GenerateNewTest, name="GenerateNewTest"),

    path('GenerateNewTestSave/', views.GenerateNewTestSave,
         name="GenerateNewTestSave"),

    path('AnayReco/<str:message>',
         views.AnayReco, name="AnayReco"),

    path("BackToMain/<str:message>", views.BackToMain, name="BackToMain")
    # path("<str:name>",views,greet.name="greet"),
    # html django templating language{{}}
]
