from django import forms


class CommentForm(forms.Form):
    CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    name = forms.CharField(label='Your Name', max_length=50)
    comment = forms.CharField(label='Your Comment', max_length=200)
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    coloring_book_id = forms.IntegerField(widget=forms.HiddenInput())
