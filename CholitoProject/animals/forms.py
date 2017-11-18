from django import forms

from animals.models import Animal
from complaint.models import AnimalType, Complaint


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
            'adoption_state',
            'is_sterilized',
        )
        widgets = {
            'name' : forms.TextInput(attrs={'id': 'name-input'}),
            'gender' : forms.RadioSelect(attrs={'id': 'gender-input'}),
            'animal_type' : forms.Select(attrs={'id': 'animal_type-input'}),
            'color': forms.TextInput(attrs={'id': 'color-input'}),
            'estimated_age': forms.NumberInput(attrs={'id': 'estimated_age-input'}),
            'description': forms.TextInput(attrs={'id': 'description-input'}),
            'adoption_state': forms.HiddenInput(),
            'is_sterilized': forms.Select(attrs={'id': 'is_sterilized-input'})
        }

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        self.fields['animal_type'] = forms.ModelChoiceField(queryset=AnimalType.objects)

class ImageForm(forms.Form):
    animal_image = forms.ImageField(required=False,
        widget=forms.FileInput(
            attrs={'id': 'image-input', 'class': "form-control", 'placeholder': "Agrega Imagen"}))
