from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from recipebox.models import Author, RecipeItem
from recipebox.forms import RecipeAddForm, AuthorAddForm, LoginForm, EditRecipeForm, SignupForm


def index(request):
    items = RecipeItem.objects.all()
    return render(request, "index.html", {"data": items})

def recipes(request, recipe):
    recipes = RecipeItem.objects.get(title=recipe)
    flag = False

    if str(request.user) == str(recipes.author):
        flag = True

    return render(request, "recipes.html", {"recipes": recipes, "flag": flag})

def authors(request, author):
    recipes = RecipeItem.objects.filter(author__name=author)
    authors = Author.objects.get(name=author)
    favorites = recipes.filter(favorite=True)

    return render(request, "authors.html", 
                    {"recipes": recipes,
                    "authors": authors,
                    "favorites": favorites,
                    })

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
                # data['bio']
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
            # login(request, user)
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


def recipe_edit_view(request, id):
    html = "editrecipe.html"

    recipe = RecipeItem.objects.get(id=id)
    save_data = {
        "title": recipe.title,
        "author": recipe.author,
        "description": recipe.description,
        "time_required": recipe.time_required,
        "instructions": recipe.instructions
    }

    if request.method == "POST":
        form = EditRecipeForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            recipe.title = data['title']
            recipe.author = data['author']
            recipe.description = data['description']
            recipe.time_required = data['time_required']
            recipe.instructions = data['instructions']
            recipe.save()
            
            return HttpResponseRedirect(reverse("homepage"))

    form = EditRecipeForm(save_data)

    return render(request, html, {'form': form})


def favorite_view(request, id):
    recipe = RecipeItem.objects.get(id=id)
    recipe.favorite = True
    recipe.save()

    return HttpResponseRedirect(reverse("homepage"))


def signup_view(request):
    html = "signup.html"

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(
                data['username'],
                data['password'],
            )

            login(request, user)
            Author.objects.create(
                name=data['username'],
                user=user
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, html, {'form': form})
