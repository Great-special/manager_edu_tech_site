from django import forms
from django.forms import formset_factory


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
