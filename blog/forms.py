from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *

class AdminApplForm(forms.ModelForm):
    
    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'age', 'email', 'phone_number', 'address', 'qualification', 'bio']

class LoginForm(forms.Form):
    
    email = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'post', 'image', 'category']

class CommentForm(forms.ModelForm):
    
    class Meta:
        
        model = Comment
        fields = ['content', 'parent']

class ReaderSignUpForm(UserCreationForm):
    
    phone_number = forms.CharField(label = 'Phone Number')
    gender = forms.ChoiceField(choices=GENDER, required=True)
    state = forms.ChoiceField(choices=STATE, required=True)
    picture = forms.FileField(label='Profile Picture', required=True)

#readermodel
    bio = forms.CharField(max_length=199, label='Short Description',
            widget=forms.Textarea(attrs={'rows':5,'cols':50}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'age', 'state', 'address', 'picture']
        
    def save(self):
        user = super().save(commit=False)
        user.is_reader = True
        user.save()
        reader = Reader.objects.create(user=user, id=user.id)
        reader.bio = self.cleaned_data.get('bio')
        reader.save()
        return user

class WriterSignUpForm(UserCreationForm):
    
    phone_number = forms.CharField(label = 'Phone Number')
    gender = forms.ChoiceField(choices=GENDER, required=True)
    state = forms.ChoiceField(choices=STATE, required=True)
    picture = forms.FileField(label='Profile Picture', required=True)
    
#writermodel
    year_of_graduation = forms.CharField(max_length=4, min_length=4, initial = 2023, label='Year Of Graduation')
    school = forms.CharField(max_length=99)
    qualification = forms.ChoiceField(choices=QUAL, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'age', 'state', 'address', 'picture']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_writer = True
        user.save()
        writer = Writer.objects.create(user=user, id=user.id)
        writer.school = self.cleaned_data.get('school')
        writer.year_of_graduation = self.cleaned_data.get('year_of_graduation')
        writer.qualification = self.cleaned_data.get('qualification')
        writer.save()
        return user

class UserForm(forms.ModelForm):
    
    phone_number = forms.CharField(label = 'Phone Number')
    gender = forms.ChoiceField(choices=GENDER, required=True)
    state = forms.ChoiceField(choices=STATE, required=True)
    picture = forms.FileField(label='Profile Picture', required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'age', 'state', 'address', 'picture']

class WriterForm(forms.ModelForm):
    
    year_of_graduation = forms.CharField(max_length=4, min_length=4, initial = 2023, label='Year Of Graduation')
    school = forms.CharField(max_length=99)
    qualification = forms.ChoiceField(choices=QUAL, required=True)

    class Meta:
        model = Writer
        fields = ['year_of_graduation', 'school', 'qualification']

class ReaderForm(forms.ModelForm):
    
    bio = forms.CharField(max_length=199, label='Short Description',
            widget=forms.Textarea(attrs={'rows':5,'cols':50}))

    class Meta:
        model = Reader
        fields = ['bio',]