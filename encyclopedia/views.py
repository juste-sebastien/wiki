from django import forms

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from random import randint

from . import util

from markdown2 import Markdown


def index(request):
    """"
    With enter on index.html, render the corresponding webpage with the list of all entries in
    ~/entries/

    Parameters:
    -----------------
    request: WSGIRequest 

    Returns:
    -----------------
    render of the webpage
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """"
    With enter on each entry, render the corresponding webpage with the title and the content of 
    the selected entry

    Parameters:
    -----------------
    request: WSGIRequest 
    title: str

    Returns:
    -----------------
    render of the webpage
    """
    if title in util.list_entries():
        content = convert_to_html(util.get_entry(title))
    else:
        error_title = "Error"
        content = f"Sorry, the page {title} seems not to exist"
        title = error_title
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content,
        })


def search(request):
    """"
    When the user search for a particular entry this function take the content of the request,
    call the function search_for_entry(), compare the type of entries_result. If it's a list, 
    the rendering of the webpage is returned. If not return the rendering by calling entry()

    Parameters:
    -----------------
    request: WSGIRequest 

    Returns:
    -----------------
    render of the webpage
    """
    title = request.GET["q"].casefold()
    entries_result = search_for_entry(title)

    if type(entries_result) != list:
        return entry(request, entries_result)
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": entries_result,
        })


def search_for_entry(title):
    """"
    Compare the title that the user search for. If the title exist, the title in util.list_entries()
    is return. If the research is contained in the item, the return of this function is a list with 
    similar titles. If there is no match, the research is returned

    Parameters:
    -----------------
    title: str

    Returns:
    -----------------
    entries_list: list
    or
    title: str
    or 
    item: str

    """
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
    """"
    Check the type of the request. If it is a GET request, the rendering of create_page.html is returned to create 
    a new entrie. If not, it's the return of add_new_page()

    Parameters:
    -----------------
    request: WSGIRequest 

    Returns:
    -----------------
    render of the webpage
    """
    if request.method == "GET":
        return render(request, "encyclopedia/create_page.html")
    else:
        return add_new_page(request)
    


def add_new_page(request):
    """"
    When this function is called, it checked if the title does not correspond to any each other that currently 
    exist in util.list_entries(). If the entry is already in ~/entries/ the rendering of error.html is returned.
    If not, a new entry is created by calling util.save_entry-) and the user is redirected to this new entry.

    Parameters:
    -----------------
    request: WSGIRequest 

    Returns:
    -----------------
    render of the webpage
    or
    HttpResponseRedirect
    """
    title = search_for_entry(request.POST["pt"])
    if title in util.list_entries():
        return render(request, "encyclopedia/error.html", {"title": title,})
    else:
        title = title.capitalize()
        util.save_entry(title, request.POST["pc"])
        return HttpResponseRedirect(reverse("wiki:entry", args=[title]))


def edit(request, title):
    """"
    When a user want to edit an existing entry, the calling method is a GET method and the rendering of
    this entry is returned in an <textarea> to authorize the user to change the content. When he click on
    save button, the method is POST and the user is redirect to the entry with the new content
    after the call of util.save_entry()

    Parameters:
    -----------------
    request: WSGIRequest 
    title: str

    Returns:
    -----------------
    render of the webpage
    or
    HttpResponseRedirect
    """
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
    """"
    When the user want a random page, this function generate a random integer to choose an index
    in the list returned by util.list_entries(). The user is automatically redirect to this 
    page selected randomly

    Parameters:
    -----------------
    request: WSGIRequest 

    Returns:
    -----------------
    HttpResponseRedirect
    """
    list_entries = util.list_entries()
    title = list_entries[randint(0, len(list_entries)) - 1]
    return HttpResponseRedirect(reverse("wiki:entry", args=[title]))


def convert_to_html(content):
    """"
    Take the content of an entry in MarkDown language, and return the corresponding HTML code

    Parameters:
    -----------------
    content: str
        in markdown language 

    Returns:
    -----------------
    str
    """
    markdowner = Markdown()
    return markdowner.convert(content)
