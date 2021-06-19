from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    # path("wiki/", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title_name>", views.wikititle, name="wikititle"),
    path("randomchoice", views.randomchoice, name="randomchoice"),
    path("newpage", views.newpage, name="newpage"),
    path("saveresult", views.saveresult, name="saveresult"),
    path("editentry",views.editentry,name="editentry"),
    path("processedit",views.processedit,name="processedit")
]
