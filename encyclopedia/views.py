import markdown
from django.shortcuts import render

from . import util


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
