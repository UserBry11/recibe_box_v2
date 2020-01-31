from django.db import models

#Author
# Name (CharField)
# Bio (TextField)

#RecipeItem
# Title (CharField)
# Author (ForeignKey)
# Description (TextField)
# Time Required (Charfield) (for example, "One hour")
# Instructions (TextField)

class Author(models.Model):
    name = models.CharField(max_length=50)
    byline = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class RecipeItem(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length=20)
    instructions = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.title, self.author)