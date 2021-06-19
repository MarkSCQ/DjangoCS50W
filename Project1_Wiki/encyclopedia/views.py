from django.shortcuts import render
from django.shortcuts import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

import random

from . import util

import markdown2


class formdata(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wikititle(request, title_name):
    EntryNameList = util.list_entries()
    if str(title_name) in EntryNameList:
        cont = markdown2.markdown(util.get_entry(title_name))
        return render(request, "encyclopedia/wikititle.html", {
            "entries": cont,
            "entryname":title_name})
    else:
        return render(request, "encyclopedia/wikititle.html", {
            "entries": "Error, Not existed"})


def search(request):
    cont = util.list_entries()
    returnlist = []
    if request.method == "POST":
        query = request.POST.get("q")
        if query in cont:
            return render(request, "encyclopedia/wikititle.html", {
                "entryname": str(query),
                "entries": str(markdown2.markdown(util.get_entry(query))),
                "type": 1
            })
        else:
            for i in cont:
                if query in str(i):
                    returnlist.append(i)
            if len(returnlist) != 0:
                return render(request, "encyclopedia/search.html", {
                    "entries": returnlist,
                    "type": 2
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "entries": str("Sorry, the item you searched is not in this system.")})
    else:
        # if form is not valid
        return render(request, "encyclopedia/search.html", {
            "entries": "Error"})


def randomchoice(request):
    namelist = util.list_entries()
    title = random.choice(namelist)
    return render(request, "encyclopedia/randompage.html", {
        "entries": str(markdown2.markdown(util.get_entry(title))),
        "entryname":title
    })


def newpage(request):
    return render(request, "encyclopedia/newpage.html")


def writeintxt(txts):
    f = open("logs.txt", "a")
    f.write(txts)
    f.close()


def saveresult(request):
    mf = formdata(request.POST)
    Title = "originTitle"
    Content = "originContent"
    Title = request.POST.get("Title")
    Content = request.POST.get("Content")
    writeintxt(Title)
    writeintxt(Content)
    if Title in util.list_entries():
        return render(request, "encyclopedia/newpageresult.html",
                      {"message": str("File existed"),
                       "existedfile": util.list_entries()})
    else:
        util.save_entry(Title, Content)
        if Title in util.list_entries():
            return render(request, "encyclopedia/newpageresult.html",
                          {"message": str("Creation successfully"),
                           "existedfile": util.list_entries()})
        else:
            return render(request, "encyclopedia/newpageresult.html",
                          {"message": str("Creation fail"),
                           "existedfile": util.list_entries()})
def editentry(request):
    entryname = request.POST.get("entryname")
    return render(request, "encyclopedia/editpage.html",
                          {"entryname": entryname,
                           "content": util.get_entry(entryname)})

def processedit(request):
    entryname = request.POST.get("entryname")
    content = request.POST.get("Content")
    # cont = markdown2.markdown(util.get_entry(title_name))

    util.save_entry(entryname,content)
    return render(request, "encyclopedia/wikititle.html",
                          {"entryname": entryname,
                           "entries": str(markdown2.markdown(util.get_entry(entryname)))})
