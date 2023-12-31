from django.db.models import Q
from datetime import datetime
import json
import os
import pandas as pd
from django.db import IntegrityError
from django.forms import ValidationError
from django.urls import reverse
import openpyxl
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .forms import EmployeeForm
from .models import Employee, ExcelFile
import io
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView



class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class CustomLogoutView(LogoutView):
    next_page = '/login/'


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your login template path here

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(self.request, user)
            return redirect('employee_list')
        else:
            error_message = "Invalid admin credentials."
            return render(self.request, self.template_name, {'error_message': error_message})


class EmployeeRecordTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.addPageTemplates([
            PageTemplate(
                id='EmployeeRecord',
                frames=[
                    Frame(
                        40,
                        40,
                        self.pagesize[0] - 80,
                        self.pagesize[1] - 80,
                        leftPadding=0,
                        bottomPadding=0,
                        rightPadding=0,
                        topPadding=40,
                    ),
                    Frame(
                        40,
                        0,
                        self.pagesize[0] - 80,
                        40,
                        leftPadding=0,
                        bottomPadding=0,
                        rightPadding=0,
                        topPadding=0,
                        id='header_frame',
                    ),
                ],
                onPage=self.header_footer,
            ),
        ])

    def header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawRightString(
            doc.pagesize[0] - 40,
            doc.pagesize[1] - 20,
            "EMPLOYEES DIRECTORY"
        )
        canvas.setFont("Helvetica", 10)
        canvas.drawString(
            40,
            doc.pagesize[1] - 20,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        canvas.restoreState()


class DownloadEmployeesPDFView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        employees = Employee.objects.all().order_by('name')

        pdf_file = io.BytesIO()

        doc = EmployeeRecordTemplate(pdf_file, pagesize=letter)

        styles = getSampleStyleSheet()
        section_title_style = styles['Heading1']
        section_content_style = ParagraphStyle(
            'section_content',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            spaceAfter=7
        )

        elements = []
        for employee in employees:
            elements.append(Paragraph(employee.name, section_title_style))
            elements.append(Spacer(1, 12))

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


            elements.append(Spacer(1, 24))


        doc.build(elements)

        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'EmployeesRecord_{date}.pdf'
        file_path = os.path.join(settings.MEDIA_ROOT, 'pdf', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(pdf_file.getvalue())

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response.write(pdf_file.getvalue())

        return response


class DownloadEmployeesView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        employees = Employee.objects.all().order_by('id')

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

        excel_file = io.BytesIO()
        excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(excel_writer, index=False, sheet_name='Employees')
        excel_writer.close()
        excel_file.seek(0)


        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'EmployeesRecords_{date}.xlsx'
        file_path = os.path.join(settings.MEDIA_ROOT, 'excel', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(excel_file.getvalue())

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response.write(excel_file.getvalue())

        return response


class ManualEntry(LoginRequiredMixin, View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'manualentry.html', {'form': form})

    def post(self, request): 
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

            return render(request, 'manualentry.html', {'form': form})


class EmployeeListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        form = EmployeeForm()
        employees = Employee.objects.all().order_by('-id')
        count = Employee.objects.count()
        sort = request.GET.get('sort')
        order = request.GET.get('order')
        search_query = request.GET.get('search')

        if search_query:
            employees = employees.filter(
                Q(name__icontains=search_query) | 
                Q(id__icontains=search_query) |   
                Q(city__icontains=search_query) |   
                Q(state__icontains=search_query) |  
                Q(team__icontains=search_query) 
            )

        if sort == 'id':
            employees = employees.order_by('id')
        elif sort == 'name':
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
        return render(request, 'employees.html', {'form': form, 'page_obj': page_obj, 'count': count, 'sort': sort, 'order': order})

    def post(self, request):

        if 'excel_form_submit' in request.POST:
            max_file_size = 1024 * 1024
            try:
                file = request.FILES['files']
                if file.size > max_file_size:
                    error_message = "Error: The file size exceeds the maximum allowed limit (1 MB)."
                    messages.error(request, error_message)
                    return redirect(reverse('employee_list'))
                obj = ExcelFile.objects.create(file_upload=file)
                path = obj.file_upload.path
                workbook = openpyxl.load_workbook(path)
                worksheet = workbook.active
                data = []
                for idx, row in enumerate(worksheet.iter_rows(values_only=True), start=1):
                    if idx == 1:
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

                for employee_data in data:
                    try:
                        Employee.objects.create(**employee_data)
                    except IntegrityError as e:
                        error_message = f"Error creating employee: This employee already exists."
                        messages.error(request, error_message)

                        return redirect(reverse('employee_list'))
                    except Exception as e:
                        error_message = f"Error creating employee: {str(e)}"
                        messages.error(request, error_message)
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


class EmployeeUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'
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
