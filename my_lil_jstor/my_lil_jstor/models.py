from django.db import models
from django.forms import ModelForm


class ColoringBook(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)


class Comment(models.Model):
    RATING_CHOICES = [
        ('', 'no rating'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, choices=RATING_CHOICES)
    coloring_book_id = models.PositiveSmallIntegerField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment', 'rating']
