from django import forms

from animals.models import Animal
from complaint.models import AnimalType, Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = (
            'name',
            'gender',
            'animal_type',
            'color',
            'estimated_age',
            'description',
            'from_complaint',
            'admission_date',
        )

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['animal_type'] = forms.ModelChoiceField(queryset=AnimalType.objects)
        self.fields['from_complaint'] = forms.ModelChoiceField(queryset=Complaint.objects)
