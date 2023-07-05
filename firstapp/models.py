from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Employee(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed."
    )

    def validate_dob(value):
        # Custom validation logic for DOB
        if value.year < 1950:
            raise ValidationError("Invalid date of birth. Year must be greater than or equal to 1950.")
        if value.year > 2005:
            raise ValidationError("Invalid date of birth. Year must be less than 2005")

    name = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    dob = models.DateField(validators=[validate_dob])
    doj = models.DateField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    team = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'phone']


class ExcelFile(models.Model):
    file_upload = models.FileField(upload_to="excel")