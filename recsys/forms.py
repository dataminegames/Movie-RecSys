from django import forms
from recsys.models import *


class MovieChoiceForm(forms.ModelForm):
    movie = forms.ModelChoiceField(
        queryset=MovieChoice.objects.order_by('order'),
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = MovieChoice
        fields = ['movie']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'address', 'mbti']


class UserLikeForm(forms.ModelForm):
    class Meta:
        model = UserLike
        fields = ['user', 'movie']
