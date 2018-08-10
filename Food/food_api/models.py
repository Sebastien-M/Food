from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='ingredients', on_delete='cascade')

    def str(self):
        return self.name