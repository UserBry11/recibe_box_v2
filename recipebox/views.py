from django.shortcuts import render

from recipebox.models import Author, RecipeItem


def index(request):
    items = RecipeItem.objects.all()
    return render(request, "index.html", {"data": items})

def recipes(request, recipe):
    return render(request, "recipes.html", {"recipes": RecipeItem.objects.get(title=recipe)})

def authors(request, author):
    return render(request, "authors.html", 
                    {"recipes": RecipeItem.objects.filter(author__name=author),
                    "authors": Author.objects.get(name=author)})
