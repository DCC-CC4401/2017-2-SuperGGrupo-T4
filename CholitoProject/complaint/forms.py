from django import forms

from .models import Complaint, AnimalType


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            'case',
            'animal_type',
            'gender',
            'color',
            'wounded',
            'directions',
            'lat',
            'lng',
            'description',
            'municipality',
        )
        widgets = {
            'case': forms.Select(attrs={'id': 'case-input'}),
            'animal_type': forms.Select(attrs={'id': 'animal_type-input'}),
            'color': forms.TextInput(attrs={'id': 'color-input'}),
            'gender': forms.RadioSelect(attrs={'id': "gender-input"}),
            'wounded': forms.RadioSelect(attrs={'id': "wounded-input"}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'directions': forms.HiddenInput(),
            'description': forms.TextInput(attrs={'id': 'description-input'}),
            'municipality': forms.Select(attrs={'id': 'municipality-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['animal_type'] = forms.ModelChoiceField(queryset=AnimalType.objects)


class ImageForm(forms.Form):
    complaint_image = forms.ImageField(required=False,
        widget=forms.FileInput(
            attrs={'id': 'image-input', 'class': "form-control", 'placeholder': "Agrega una imagen de tu denuncia"}))
