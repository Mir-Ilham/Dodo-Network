from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, BlogPost

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio']

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'name', 'username', 'email', 'company_name', 'bio']

class PostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'cover']