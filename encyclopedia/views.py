import random
import markdown
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util


class CreateForm(forms.Form):
    title_of_the_page = forms.CharField(label="Entry title", widget=forms.TextInput)
    user_text = forms.CharField(widget=forms.Textarea)
    edit_button = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search wikipedia"}))


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


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data["title_of_the_page"]
            user_input = form.cleaned_data["user_text"]
            if util.get_entry(page_title) is None or form.cleaned_data["edit_button"] is True:
                util.save_entry(page_title, user_input)
                # return render(request, "encyclopedia/user_page.html", {"entry": util.get_entry(page_title),
                #                                                        "e_title": page_title})
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": page_title}))
            else:
                return render(request, "encyclopedia/create.html", {"form": form,
                                                                    "does_exist": True,
                                                                    "entry": page_title})
        else:
            return render(request, "encyclopedia/create.html", {"form": form,
                                                                "does_exist": True})
    return render(request, "encyclopedia/create.html", {"form": CreateForm(),
                                                        "does_exist": False})


def random_web_page(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": random_page}))
