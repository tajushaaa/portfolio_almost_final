from .models import Project, AdditionalImage
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ProjectForm(forms.ModelForm):
    additional_images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'info',
                  'category', 'image', 'additional_images')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            image_extension = image.name.split('.')[-1].lower()
            if image_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                raise ValidationError(
                    _('Only image files (jpg, jpeg, png, gif) are allowed.'))
        return image


class ImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("This field is required.")
        image_extension = image.name.split('.')[-1].lower()
        if image_extension not in ['jpg', 'jpeg', 'png', 'gif']:
            raise forms.ValidationError(
                _('Only image files (jpg, jpeg, png, gif) are allowed.'))
        return image


class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }
