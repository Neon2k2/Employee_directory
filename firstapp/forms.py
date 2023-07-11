from django import forms
from django.forms.widgets import DateInput
from datetime import datetime, timezone
from django.core.validators import MinValueValidator
from firstapp.models import Employee

class CustomDateInput(DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        min_date = kwargs.pop('min_date', None)
        max_date = kwargs.pop('max_date', None)
        super().__init__(*args, **kwargs)
        if min_date:
            self.attrs['min'] = min_date
        if max_date:
            self.attrs['max'] = max_date

class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        exclude = ['created_at', 'updated_at']
        CITY_CHOICES = [
            ('ahmedabad', 'Ahmedabad'),
            ('ahmednagar', 'Ahmednagar'),
            ('ajmer', 'Ajmer'),
            ('akola', 'Akola'),
            ('aligarh', 'Aligarh'),
            ('allahabad', 'Allahabad'),
            ('amravati', 'Amravati'),
            ('amritsar', 'Amritsar'),
            ('ankleshwar', 'Ankleshwar'),
            ('bareilly', 'Bareilly'),
            ('bardoli', 'Bardoli'),
            ('baramati', 'Baramati'),
            ('bengaluru', 'Bengaluru'),
            ('bharuch', 'Bharuch'),
            ('bhavnagar', 'Bhavnagar'),
            ('bhuj', 'Bhuj'),
            ('bhopal', 'Bhopal'),
            ('bhubaneswar', 'Bhubaneswar'),
            ('chandigarh', 'Chandigarh'),
            ('chandrapur', 'Chandrapur'),
            ('chennai', 'Chennai'),
            ('coimbatore', 'Coimbatore'),
            ('colombo', 'Colombo'),
            ('dehradun', 'Dehradun'),
            ('delhi', 'Delhi'),
            ('dhaka', 'Dhaka'),
            ('dhule', 'Dhule'),
            ('faridabad', 'Faridabad'),
            ('gandhidham', 'Gandhidham'),
            ('gandhinagar', 'Gandhinagar'),
            ('ghaziabad', 'Ghaziabad'),
            ('goa', 'Goa'),
            ('gurgaon', 'Gurgaon'),
            ('gurugram', 'Gurugram'),
            ('guwahati', 'Guwahati'),
            ('gwalior', 'Gwalior'),
            ('hyderabad', 'Hyderabad'),
            ('indore', 'Indore'),
            ('jaipur', 'Jaipur'),
            ('jamnagar', 'Jamnagar'),
            ('jamshedpur', 'Jamshedpur'),
            ('jammu', 'Jammu'),
            ('jalandhar', 'Jalandhar'),
            ('jodhpur', 'Jodhpur'),
            ('junagadh', 'Junagadh'),
            ('kalyan', 'Kalyan'),
            ('kanpur', 'Kanpur'),
            ('karachi', 'Karachi'),
            ('kathmandu', 'Kathmandu'),
            ('kolkata', 'Kolkata'),
            ('kochi', 'Kochi'),
            ('kota', 'Kota'),
            ('lahore', 'Lahore'),
            ('lucknow', 'Lucknow'),
            ('madurai', 'Madurai'),
            ('malegaon', 'Malegaon'),
            ('mangalore', 'Mangalore'),
            ('meerut', 'Meerut'),
            ('moradabad', 'Moradabad'),
            ('mumbai', 'Mumbai'),
            ('nagpur', 'Nagpur'),
            ('nanded', 'Nanded'),
            ('nashik', 'Nashik'),
            ('navsari', 'Navsari'),
            ('noida', 'Noida'),
            ('panvel', 'Panvel'),
            ('patna', 'Patna'),
            ('pune', 'Pune'),
            ('raipur', 'Raipur'),
            ('rajasthan', 'Rajasthan'),
            ('rajkot', 'Rajkot'),
            ('ranchi', 'Ranchi'),
            ('ratlam', 'Ratlam'),
            ('sagar', 'Sagar'),
            ('salem', 'Salem'),
            ('satara', 'Satara'),
            ('solapur', 'Solapur'),
            ('srinagar', 'Srinagar'),
            ('sangli', 'Sangli'),
            ('surat', 'Surat'),
            ('thane', 'Thane'),
            ('tiruchirappalli', 'Tiruchirappalli'),
            ('ujjain', 'Ujjain'),
            ('udaipur', 'Udaipur'),
            ('vadodara', 'Vadodara'),
            ('vapi', 'Vapi'),
            ('varanasi', 'Varanasi'),
            ('vasai', 'Vasai'),
            ('vijayawada', 'Vijayawada'),
            ('visakhapatnam', 'Visakhapatnam'),
            ('warangal', 'Warangal'),
        ]
        STATE_CHOICES = [
            ('andaman_nicobar', 'Andaman and Nicobar Islands'),
            ('andhra_pradesh', 'Andhra Pradesh'),
            ('arunachal_pradesh', 'Arunachal Pradesh'),
            ('assam', 'Assam'),
            ('bihar', 'Bihar'),
            ('chandigarh', 'Chandigarh'),
            ('chhattisgarh', 'Chhattisgarh'),
            ('dadra_nagar_haveli', 'Dadra and Nagar Haveli'),
            ('daman_diu', 'Daman and Diu'),
            ('delhi', 'Delhi'),
            ('goa', 'Goa'),
            ('gujarat', 'Gujarat'),
            ('haryana', 'Haryana'),
            ('himachal_pradesh', 'Himachal Pradesh'),
            ('jammu_kashmir', 'Jammu and Kashmir'),
            ('jharkhand', 'Jharkhand'),
            ('karnataka', 'Karnataka'),
            ('kerala', 'Kerala'),
            ('lakshadweep', 'Lakshadweep'),
            ('madhya_pradesh', 'Madhya Pradesh'),
            ('maharashtra', 'Maharashtra'),
            ('manipur', 'Manipur'),
            ('meghalaya', 'Meghalaya'),
            ('mizoram', 'Mizoram'),
            ('nagaland', 'Nagaland'),
            ('odisha', 'Odisha'),
            ('puducherry', 'Puducherry'),
            ('punjab', 'Punjab'),
            ('rajasthan', 'Rajasthan'),
            ('sikkim', 'Sikkim'),
            ('tamil_nadu', 'Tamil Nadu'),
            ('telangana', 'Telangana'),
            ('tripura', 'Tripura'),
            ('uttar_pradesh', 'Uttar Pradesh'),
            ('uttarakhand', 'Uttarakhand'),
            ('west_bengal', 'West Bengal'),
        ]
        GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ]

        Date_ = datetime.now().strftime('%Y-%m-%d')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender' : forms.Select(choices=GENDER_CHOICES, attrs={'class': 'form-control'}),
            'dob': CustomDateInput(attrs={'class': 'form-control'}, min_date='1964-01-31', max_date='2002-12-31'),
            'doj': CustomDateInput(attrs={'class': 'form-control'}, min_date='1990-01-01', max_date = f'{Date_}'),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(choices=CITY_CHOICES, attrs={'class': 'form-control'}),
            'state': forms.Select(choices=STATE_CHOICES, attrs={'class': 'form-control'}),
            'team': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1000'}),
        }


    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob > datetime.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean_doj(self):
        doj = self.cleaned_data.get('doj')
        if doj > datetime.now().date():
            raise forms.ValidationError("Date of joining cannot be in the future.")
        return doj

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary <= 0:
            raise forms.ValidationError("Salary must be a positive value.")
        return salary
    


