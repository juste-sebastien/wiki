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
    request_dict = request.GET
    title = request_dict["q"]
    for item in util.list_entries():
        title = title.casefold()
        if item.casefold() == title:
            entry(request, item)
    else:
        print("ko")
        pass