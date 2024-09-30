from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_number', 'roll_number', 'first_name', 'last_name', 'attendance', 'cie_marks', 'batch', 'division', 'subjects']
        
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'attendance': forms.NumberInput(attrs={'class': 'form-control'}),
            'cie_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'subjects': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }