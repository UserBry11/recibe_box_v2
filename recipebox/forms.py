from django import forms
from recipebox.models import Author, RecipeItem

class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    time_required = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)

class AuthorAddForm(forms.Form):
    name = forms.CharField(max_length=50)
    byline = forms.CharField(max_length=250)
    name = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25)
    bio = forms.CharField(max_length=300)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25)


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = RecipeItem
        fields = ['title', 'author', 'description', 'time_required', 'instructions']
