
from datetime import datetime
import openpyxl
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import EmployeeForm
from .models import Employee, ExcelFile
import io
from django.conf import settings

class DownloadEmployeesView(View):
    def get(self, request):
        employees = Employee.objects.all()

        # Create a DataFrame from the employees queryset
        data = {
            'Name': [employee.name for employee in employees],
            'Phone': [employee.phone for employee in employees],
            'Date of Birth': [employee.dob for employee in employees],
            'Date of Join': [employee.doj for employee in employees],
            'Address': [employee.address for employee in employees],
            'City': [employee.city for employee in employees],
            'State': [employee.state for employee in employees],
            'Team': [employee.team for employee in employees],
            'Salary': [employee.salary for employee in employees],
        }
        df = pd.DataFrame(data)

        # Create a BytesIO object to store the Excel file
        excel_file = io.BytesIO()
        excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(excel_writer, index=False, sheet_name='Employees')
        excel_writer.close()
        excel_file.seek(0)

        # Create the HTTP response with the Excel file
        date = datetime.now()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=EmployeesRecords{date}.xlsx'
        response.write(excel_file.getvalue())

        return response
    


class EmployeeListView(View):
    def get(self, request):
        form = EmployeeForm()
        employees = Employee.objects.all()
        return render(request, 'employees.html', {'form': form, 'employees': employees})

    def post(self, request):
        if 'employee_form_submit' in request.POST:
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('employee_list')

        
        if 'excel_form_submit' in request.POST:
            file = request.FILES['files']

            # Save the uploaded Excel file
            obj = ExcelFile.objects.create(file_upload=file)
            path = obj.file_upload.path

            # Read the data from the Excel file
            workbook = openpyxl.load_workbook(path)
            worksheet = workbook.active

            data = []
            for idx, row in enumerate(worksheet.iter_rows(values_only=True), start=1):
                if idx == 1:
                    # Skip the header row
                    continue

                dob_str = datetime.strftime(row[2], '%Y-%m-%d')
                doj_str = datetime.strftime(row[3], '%Y-%m-%d')

                employee_data = {
                    'name': row[0],
                    'phone': row[1],
                    'dob': dob_str,
                    'doj': doj_str,
                    'address': row[4],
                    'city': row[5],
                    'state': row[6],
                    'team': row[7],
                    'salary': row[8],
                }
                data.append(employee_data)

            # Create Employee objects from the data
            for employee_data in data:
                Employee.objects.create(**employee_data)
            return redirect('employee_list')

        employee_form = EmployeeForm()
        return render(request, 'employees.html', {'employee_form': employee_form})

