from django import forms
from recipebox.models import Author

class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    time_required = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)

class AuthorAddForm(forms.Form):
    name = forms.CharField(max_length=50)
    byline = forms.CharField(max_length=250)
