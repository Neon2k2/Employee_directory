
from datetime import datetime
import json
import pandas as pd
from reportlab.pdfgen import canvas
from django.db import IntegrityError
from django.forms import ValidationError
from django.urls import reverse
import openpyxl
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import EmployeeForm
from .models import Employee, ExcelFile
import io
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class DownloadEmployeesPDFView(View):
    def get(self, request):
        employees = Employee.objects.all().order_by('name')

        # Create a BytesIO object to store the PDF file
        pdf_file = io.BytesIO()
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        # Define custom styles for the resume sections
        styles = getSampleStyleSheet()
        section_title_style = styles['Heading1']
        section_content_style = ParagraphStyle(
            'section_content',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            spaceAfter=10
        )

        # Generate the resume sections for each employee
        elements = []
        for employee in employees:
            # Add employee name as section title
            elements.append(Paragraph(employee.name, section_title_style))
            elements.append(Spacer(1, 12))  # Add space after the section title

            # Add employee details as section content
            elements.append(
                Paragraph(f"Phone: {employee.phone}", section_content_style))
            elements.append(
                Paragraph(f"Date of Birth: {employee.dob}", section_content_style))
            elements.append(
                Paragraph(f"Date of Join: {employee.doj}", section_content_style))
            elements.append(
                Paragraph(f"Address: {employee.address}", section_content_style))
            elements.append(
                Paragraph(f"City: {employee.city}", section_content_style))
            elements.append(
                Paragraph(f"State: {employee.state}", section_content_style))
            elements.append(
                Paragraph(f"Team: {employee.team}", section_content_style))
            elements.append(
                Paragraph(f"Salary: {employee.salary}", section_content_style))

            # Add space between employee sections
            elements.append(Spacer(1, 24))

        # Build the PDF file
        doc.build(elements)

        # Create the HTTP response with the PDF file
        date = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=EmployeesRecord_{date}.pdf'
        response.write(pdf_file.getvalue())

        return response


class DownloadEmployeesView(View):
    def get(self, request):
        employees = Employee.objects.all().order_by('name')

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
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=EmployeesRecords{date}.xlsx'
        response.write(excel_file.getvalue())

        return response


class ManualEntry(View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'manualentry.html', {'form': form})

    def post(self, request):  # Fix: lowercase "p" in "post" method name
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.name = employee.name.capitalize()
            employee.phone = employee.phone.capitalize()
            employee.address = employee.address.capitalize()
            employee.city = employee.city.capitalize()
            employee.state = employee.state.capitalize()
            employee.team = employee.team.capitalize()
            form.save()
            messages.success(
                request, 'Employee added successfully to the database.')
            return redirect(reverse('employee_list'))
        else:
            # Form is invalid, display error messages
            return render(request, 'manualentry.html', {'form': form})


class EmployeeListView(View):
    def get(self, request):
        form = EmployeeForm()
        employees = Employee.objects.all().order_by('-created_at')
        sort = request.GET.get('sort')
        order = request.GET.get('order')
        if sort == 'name':
            employees = employees.order_by('name')
        elif sort == 'doj':
            employees = employees.order_by('doj')
        elif sort == 'city':
            employees = employees.order_by('city')
        elif sort == 'state':
            employees = employees.order_by('state')
        elif sort == 'team':
            employees = employees.order_by('team')
        elif sort == 'salary':
            employees = employees.order_by('salary')

        if sort and order == 'desc':
            employees = employees.reverse()
        else:
            order = 'asc'

        paginator = Paginator(employees, per_page=settings.PAGINATION_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        CurrentDate = datetime.now().date()
        return render(request, 'employees.html', {'form': form, 'page_obj': page_obj, 'date': CurrentDate, 'sort': sort, 'order': order})

    def post(self, request):

        if 'excel_form_submit' in request.POST:
            # Handle file upload and Excel processing here...
            try:
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
                    try:
                        Employee.objects.create(**employee_data)
                    except IntegrityError as e:
                        error_message = f"Error creating employee: This employee already exists."
                        messages.error(request, error_message)
                        # Redirect to employee list page with the error message
                        return redirect(reverse('employee_list'))
                    except Exception as e:
                        error_message = f"Error creating employee: {str(e)}"
                        messages.error(request, error_message)
                        # Redirect to employee list page with the error message
                        return redirect(reverse('employee_list'))

                messages.success(request, 'Excel File uploaded successfully')
                return redirect(reverse('employee_list'))

            except KeyError:
                messages.error(request, "Missing file during Upload.")
                return redirect(reverse('employee_list'))

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect(reverse('employee_list'))

            except Exception as e:
                messages.error(
                    request, f"Error processing the Excel file: {str(e)}")
                return redirect(reverse('employee_list'))
        return redirect(reverse('employee_list'))


class EmployeeUpdateView(View):
    def patch(self, request):
        try:
            data = json.loads(request.body)
            for change in data:
                employee_id = change.get('employee_id')
                field_name = change.get('field_name')
                field_value = change.get('field_value')

                if employee_id and field_name and field_value:
                    employee = Employee.objects.get(id=employee_id)
                    setattr(employee, field_name, field_value)
                    employee.save()
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'})
        except Exception:
            return JsonResponse({'success': False, 'error': 'Error saving changes'})

        return JsonResponse({'success': True})
