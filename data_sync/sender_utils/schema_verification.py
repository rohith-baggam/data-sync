
from django.db import models
from django.apps import apps


def get_model_properties(model: models.Model) -> dict:
    """
    Retrieve and return all properties of a Django model, including fields, types, and attributes.
    """
    print('get_model_properties', model)
    properties = {}

    # Get all fields of the model
    fields = model._meta.get_fields()
    print('fields', fields)
    for field in fields:
        # Convert field type to a string that is JSON serializable
        field_type = str(type(field).__name__)
        field_info = {
            'type': field_type,
            'max_length': getattr(field, 'max_length', None),
            'null': getattr(field, 'null', None),
            'blank': getattr(field, 'blank', None),
            'default': getattr(field, 'default', None),
            'unique': getattr(field, 'unique', None),
            'db_index': getattr(field, 'db_index', None),
            'related_name': getattr(field, 'related_name', None),
            'related_model': None,
            'choices': getattr(field, 'choices', None),
        }

        # Handle related model
        if hasattr(field, 'remote_field') and field.remote_field:
            related_model = field.remote_field.model
            if related_model:
                field_info['related_model'] = related_model.__name__

        # Ensure the default value is a string if it's not a boolean
        if isinstance(field_info['default'], bool):
            field_info['default'] = str(field_info['default'])
        elif field_info['default'] is not None:
            field_info['default'] = str(field_info['default'])

        # If the field has choices, get the choices and default choice
        if field_info['choices']:
            field_info['choices'] = [str(choice)
                                     for choice in field_info['choices']]
            field_info['default_choice'] = str(field_info['default'])

        properties[field.name] = field_info

    return {
        "model": str(model),
        "fields": properties
    }
# def get_model_properties(model: models.Model) -> dict:
#     """
#     Retrieve and return all properties of a Django model, including fields, types, and attributes.
#     """
#     print('get_model_properties', model)
#     properties = {}

#     # Get all fields of the model
#     fields = model._meta.get_fields()
#     print('fields', fields)
#     for field in fields:
#         field_info = {
#             'type': str(type(field).__name__),
#             'max_length': getattr(field, 'max_length', None),
#             'null': getattr(field, 'null', None),
#             'blank': getattr(field, 'blank', None),
#             'default': getattr(field, 'default', None) if str(getattr(field, 'default', None)) in [True, False] else str(getattr(field, 'default', None)),
#             'unique': getattr(field, 'unique', None),
#             'db_index': getattr(field, 'db_index', None),
#             'related_name': getattr(field, 'related_name', None),
#             'related_model': getattr(field.remote_field, 'model', None) if hasattr(field, 'remote_field') else None,
#             # Get choices if available
#             'choices': getattr(field, 'choices', None),
#         }

#         # If the field has choices, get the choices and default choice
#         if field_info['choices']:
#             field_info['choices'] = list(field_info['choices'])
#             field_info['default_choice'] = field_info['default']
#         properties[field.name] = field_info

#     return {
#         "model": str(model),
#         "fields": properties
#     }
