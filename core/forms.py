from django import forms
from django.forms import formset_factory
from .models import CourseRegistration


class CSVFileUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='File must be in CSV format'
    )

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be in CSV format')
        return file

class FieldMappingForm(forms.Form):
    csv_column = forms.CharField(
        label='CSV Column Name',
        help_text='Enter the column name from your CSV file',
        required=True
    )
    model_field = forms.CharField(
        label='Model Field Name',
        help_text='Enter the corresponding model field name',
        required=True
    )

# Create formset for field mappings
FieldMappingFormset = formset_factory(
    FieldMappingForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        exclude = 'course',  # Exclude course field to be set programmatically
        widgets = {
            'session': forms.TextInput(attrs={'placeholder': 'Select a session'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name*'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email*'}),
            'designation': forms.TextInput(attrs={'placeholder': 'Designation/Position'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address*'}),
            'city': forms.TextInput(attrs={'placeholder': 'City*'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country*'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Telephone'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile*'}),
            'fax': forms.TextInput(attrs={'placeholder': 'Fax'}),
        }