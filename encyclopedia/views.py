from django import forms

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if title in util.list_entries():
        content = util.get_entry(title)
    else:
        error_title = "Error"
        content = f"Sorry, the page {title} seems not to exist"
        title = error_title
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content,
        })


def search(request):
    title = request.GET["q"].casefold()
    entries_result = search_for_entry(title)

    if type(entries_result) != list:
        return entry(request, entries_result)
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": entries_result,
        })


def search_for_entry(title):
    entries_list = []
    for item in util.list_entries():
        if item.casefold() == title:
            return item
        elif title in item.casefold():
            entries_list.append(item)

    if len(entries_list) != 0:
        return entries_list
    else:
        return title


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_page.html")
    else:
        return add_new_page(request)
    


def add_new_page(request):
    title = search_for_entry(request.POST["pt"])
    if title in util.list_entries():
        return render(request, "encyclopedia/error.html", {"title": title,})
    else:
        title = title.capitalize()
        util.save_entry(title, request.POST["pc"])
        return HttpResponseRedirect(reverse("wiki:entry", args=[title]))


def edit(request, title):
    content = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
        })
    else:
        util.save_entry(request.POST["pt"], request.POST["pc"])
        return HttpResponseRedirect(reverse("wiki:entry", args=[title]))


def random(request):
    list_entries = util.list_entries()
    title = list_entries[randint(0, len(list_entries)) - 1]
    return HttpResponseRedirect(reverse("wiki:entry", args=[title]))
