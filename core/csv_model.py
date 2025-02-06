import csv
from typing import Type
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Model

def import_csv_to_model(csv_file_path: str, model_class: Type[Model], related_fields: dict = {}, field_mapping: dict = {}, skip_header: bool = True) -> tuple[int, list]:
    """
    Import data from a CSV file into a Django model, handling related models.
    
    Args:
        csv_file_path (str): Path to the CSV file.
        model_class (Type[Model]): Django model class to create instances of.
        related_fields (dict, optional): Maps related field names to lookup fields.
            Example: {'department': ('DepartmentModel', 'name')}
        field_mapping (dict, optional): Maps CSV headers to model fields.
        skip_header (bool, optional): Whether to skip the first row. Defaults to True.
    
    Returns:
        tuple[int, list]: Number of records created and list of errors encountered.
    """
    records_created = 0
    errors = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            if skip_header:
                next(csv_reader, None)

            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    # Transform data using field mapping
                    transformed_data = {
                        model_field: row[csv_field]
                        for csv_field, model_field in field_mapping.items()
                        if csv_field in row
                    }

                    # Handle related fields (ForeignKey, OneToOne)
                    for related_field, (related_model, lookup_field) in related_fields.items():
                        related_value = row.get(lookup_field)
                        if related_value:
                            try:
                                related_instance = related_model.objects.get(**{lookup_field: related_value})
                                transformed_data[related_field] = related_instance
                            except related_model.DoesNotExist:
                                errors.append(f"Row {row_number}: Related {related_model.__name__} with {lookup_field}='{related_value}' not found.")
                                continue
                    
                    # Create and validate model instance
                    instance = model_class(**transformed_data)
                    instance.full_clean()
                    with transaction.atomic():
                        instance.save()
                    
                    records_created += 1
                
                except (ValidationError, KeyError) as e:
                    errors.append(f"Error in row {row_number}: {str(e)}")
                except Exception as e:
                    errors.append(f"Unexpected error in row {row_number}: {str(e)}")
    
    except FileNotFoundError:
        errors.append(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        errors.append(f"Error processing CSV file: {str(e)}")
        
    return records_created, errors




def import_csv_to_model(csv_file_path: str, model_class: Type[Model], field_mapping: dict = {}, skip_header: bool = True) -> tuple[int, list]:
    """
    Import data from a CSV file into a Django model, saving records one by one.
    
    Args:
        csv_file_path (str): Path to the CSV file
        model_class (Type[Model]): Django model class to create instances of
        field_mapping (dict, optional): Dictionary mapping CSV headers to model fields.
            If empty, assumes CSV headers match model field names.
        skip_header (bool, optional): Whether to skip the first row. Defaults to True.
    
    Returns:
        tuple[int, list]: Number of records created and list of errors encountered.
    
    Example:
        field_mapping = {
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Email Address': 'email'
        }
        created, errors = import_csv_to_model(
            'users.csv', 
            UserModel, 
            field_mapping
        )
    """
    records_created = 0
    errors = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            # Skip header if required
            if skip_header:
                next(csv_reader, None)

            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    # Transform data according to field mapping
                    if field_mapping:
                        transformed_data = {
                            model_field: row[csv_field]
                            for csv_field, model_field in field_mapping.items()
                            if csv_field in row
                        }
                    else:
                        transformed_data = row
                    
                    # Create and validate model instance
                    instance = model_class(**transformed_data)
                    instance.full_clean()  # Validate data
                    with transaction.atomic():  # Ensure transaction safety
                        instance.save()
                    
                    records_created += 1
                
                except (ValidationError, KeyError) as e:
                    errors.append(f"Error in row {row_number}: {str(e)}")
                except Exception as e:
                    errors.append(f"Unexpected error in row {row_number}: {str(e)}")
    
    except FileNotFoundError:
        errors.append(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        errors.append(f"Error processing CSV file: {str(e)}")
        
    return records_created, errors

def upload_csv_courses(request):
    if request.method == "POST" and request.FILES:
        file_form = CSVFileUploadForm(request.POST, request.FILES)
        mapping_formset = FieldMappingFormset(request.POST, prefix='mappings')

        if file_form.is_valid() and mapping_formset.is_valid():
            try:
                # Get the uploaded file
                csv_file = request.FILES['csv_file']

                # Save file temporarily
                temp_path = default_storage.save(
                    f'temp/{csv_file.name}',
                    ContentFile(csv_file.read())
                )
                file_path = default_storage.path(temp_path)

                # Create field mapping dictionary from formset
                field_mapping = {
                    form.cleaned_data['csv_column']: form.cleaned_data['model_field']
                    for form in mapping_formset
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                }

                try:
                    # Import CSV data using the previous import_csv_to_model function
                    records_created, errors = import_csv_to_model(
                        csv_file_path=file_path,
                        model_class=Category,  # Replace with your model
                        field_mapping=field_mapping
                    )

                    # Handle results
                    if errors:
                        for error in errors:
                            messages.warning(request, error)
                    
                    messages.success(
                        request,
                        f'Successfully created {records_created} records'
                    )

                except Exception as e:
                    messages.error(request, f'Error processing file: {str(e)}')

                finally:
                    # Clean up - delete temporary file
                    default_storage.delete(temp_path)

                return redirect('success_url')  # Replace with your success URL

            except Exception as e:
                messages.error(request, f'Error handling file: {str(e)}')
                return redirect('upload_csv_courses')
    else:
        file_form = CSVFileUploadForm()
        mapping_formset = FieldMappingFormset(prefix='mappings')

    context = {
        'file_form': file_form,
        'mapping_formset': mapping_formset
    }
    return render(request, 'ihrdc_layout/upload_csv.html', context)
            