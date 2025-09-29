from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget

from .models import Profile, Post, Comment


# ----------------------------
# User Registration Form
# ----------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ----------------------------
# User Update Form
# ----------------------------
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")


# ----------------------------
# Profile Update Form
# ----------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")


# ----------------------------
# Post Form (Create/Update) with Tags
# ----------------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'class': 'tag-input', 'placeholder': 'Add tags'}),  # nicer tag input
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your post content here...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
        }


# ----------------------------
# Comment Form
# ----------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'tags': TagWidget()
        }
