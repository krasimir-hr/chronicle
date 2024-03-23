from django.core.exceptions import ValidationError


def validate_file_size(image):
    if image.size > 10485760:
        raise ValidationError('The maximum file size that can be uploaded is 10 MB')