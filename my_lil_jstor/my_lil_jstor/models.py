from django.db import models
from django.forms import ModelForm


class ColoringBook(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)


class Comment(models.Model):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(blank=True)
    coloring_book_id = models.PositiveSmallIntegerField
    add_date = models.DateTimeField(auto_now_add=True)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment', 'rating']
