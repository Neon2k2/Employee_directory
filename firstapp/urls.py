from django.urls import path

from firstapp.views import DownloadEmployeesView, EmployeeListView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('download/', DownloadEmployeesView.as_view(), name='download_employees'),
]
