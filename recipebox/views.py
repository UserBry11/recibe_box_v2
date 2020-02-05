from django.shortcuts import render, reverse, HttpResponseRedirect

from recipebox.models import Author, RecipeItem
from recipebox.forms import RecipeAddForm, AuthorAddForm


def index(request):
    items = RecipeItem.objects.all()
    return render(request, "index.html", {"data": items})

def recipes(request, recipe):
    return render(request, "recipes.html", {"recipes": RecipeItem.objects.get(title=recipe)})

def authors(request, author):
    return render(request, "authors.html", 
                    {"recipes": RecipeItem.objects.filter(author__name=author),
                    "authors": Author.objects.get(name=author)})

def recipe_add_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            RecipeItem.objects.create(
                author=data['author'],
                title=data['title'],
                time_required=data['time_required'],
                description=data['description'],
                instructions=data['instructions']
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = RecipeAddForm()

    return render(request, html, {'form': form})

def author_add_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                byline=data['byline']
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AuthorAddForm()

    return render(request, html, {'form': form})