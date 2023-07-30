from django.urls import path

from firstapp.views import *
urlpatterns = [
    path('login/', CustomLoginView.as_view() , name='login'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('download/', DownloadEmployeesView.as_view(), name='download_employees'),
    path('downloadpdf/', DownloadEmployeesPDFView.as_view(), name='download_pdf'),
    path('manualEntry/', ManualEntry.as_view(), name='manualEntry'),
    path('update/', EmployeeUpdateView.as_view(), name='update_employee'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
