from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, BlogPost

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class PostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'