from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from recipebox.models import Author, RecipeItem
from recipebox.forms import RecipeAddForm, AuthorAddForm, LoginForm


def index(request):
    items = RecipeItem.objects.all()
    return render(request, "index.html", {"data": items})

def recipes(request, recipe):
    return render(request, "recipes.html", {"recipes": RecipeItem.objects.get(title=recipe)})

def authors(request, author):
    recipes = RecipeItem.objects.filter(author__name=author)
    authors = Author.objects.get(name=author)
    return render(request, "authors.html", 
                    {"recipes": recipes,
                    "authors": authors})

@login_required()
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

@staff_member_required()
def author_add_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['name'],
                data['password'],
                data['bio']
            )
            Author.objects.create(
                name=data['name'],
                byline=data['byline'],
                user=user
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AuthorAddForm()

    return render(request, html, {'form': form})

def login_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)
            if user is not None:
                login(request, user)
                # Where we want to go next after logging in correctly
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))