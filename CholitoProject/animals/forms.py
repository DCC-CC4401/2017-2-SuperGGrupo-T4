from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from animals.models import Animal
from complaint.models import AnimalType


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = (
            'name',
            'gender',
            'animal_type',
            'color',
            'estimated_age',
            'description',
            'admission_date',
            'is_sterilized',
            'avatar',
        )
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name-input'}),
            'gender': forms.RadioSelect(attrs={'id': 'gender-input'}),
            'animal_type': forms.Select(attrs={'id': 'animal_type-input'}),
            'color': forms.TextInput(attrs={'id': 'color-input'}),
            'estimated_age': forms.NumberInput(
                attrs={'id': 'estimated_age-input'}),
            'description': forms.TextInput(attrs={'id': 'description-input'}),
            'is_sterilized': forms.Select(attrs={'id': 'is_sterilized-input'}),
            'admission_date': forms.widgets.DateInput(attrs={'id': 'admission_date_input', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'id': 'avatar-input'})
        }

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        self.fields['animal_type'] = forms.ModelChoiceField(
            queryset=AnimalType.objects)


class ImageForm(forms.Form):
    animal_image = forms.ImageField(required=False,
                                    widget=forms.FileInput(
                                        attrs={'id': 'image-input',
                                               'placeholder': "Agrega Imagen"}))
