import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django import forms
from . import util


class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Qwikipedia"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    html = markdown.Markdown()
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/404.html", {"e_title": entry})
    else:
        return render(request, "encyclopedia/user_page.html", {"entry": html.convert(entry_page),
                                                               "e_title": entry})


def convert(title):
    content = util.get_entry(title)
    html = markdown.Markdown()
    if content is None:
        return None
    else:
        return html.convert(content)


def search(request):
    if request.method == "POST":
        to_search = request.POST['q']
        if convert(to_search) is not None:
            return render(request, "encyclopedia/user_page.html", {"entry": convert(to_search),
                                                                   "e_title": to_search})
        else:
            similar_entries = []
            for similar in util.list_entries():
                if to_search.upper() in similar.upper():
                    similar_entries.append(similar)
            return render(request, "encyclopedia/index.html", {"entries": similar_entries,
                                                               "search": True,
                                                               "value": to_search})
