from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('vendors/', views.dashboard_with_pivot_vendors, name='dashboard_with_pivot_vendors'),
    path('customers/', views.dashboard_with_pivot_customers, name='dashboard_with_pivot_customers'),
    path('data/', views.pivot_data, name='pivot_data'),
    path('data_vendor/', views.pivot_data_vendor, name='pivot_data_vendor'),
    path('data_customer/', views.pivot_data_customer, name='pivot_data_customer'),
]