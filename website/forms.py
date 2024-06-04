from django import forms
from .models import *


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Pins
        fields = ['title', 'description', 'collection', 'video', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'collection': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_collections = Collections.objects.filter(author=self.user)
        choices = [(collection.id, collection.title) for collection in user_collections]
        self.fields['collection'].widget.choices = choices


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Pins
        fields = ['title', 'description', 'collection', 'video', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'collection': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)
        self.fields['collection'].queryset = Collections.objects.filter(author=self.author)


class ChangeProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Имя пользователя")
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = Profile
        fields = ['photo', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super(ChangeProfileForm, self).save(commit=False)
        profile.user.username = self.cleaned_data['username']
        if commit:
            profile.user.save()
            profile.save()
        return profile


class AddCollectionForm(forms.ModelForm):
    class Meta:
        model = Collections
        fields = ['title', 'collection_image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название коллекции'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
