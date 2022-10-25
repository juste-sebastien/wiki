import json

from django import forms

from django.shortcuts import render

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
    entries_result = []
    for item in util.list_entries():
        if item.casefold() == title:
            return entry(request, item)
        elif title in item.casefold():
            entries_result.append(item)

    return render(request, "encyclopedia/search.html", {
        "entries": entries_result,
    })


def create(request):
    return render(request, "encyclopedia/create_page.html")


def add_new_page(request):
    print("im in add_new_page")
    title = request.POST["pt"]
    match = False
    for item in util.list_entries():
        if item.casefold() == title.casefold():
            match = True
            break
    print(match)
    if not match:
        content = request.POST["pc"]
        util.save_entry(title, content)
        return entry(request, title)
