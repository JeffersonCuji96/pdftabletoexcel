from django.urls import path
from django.views.generic import RedirectView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('extract-table-pdf/', views.extract_table_pdf, name='extract_table_pdf'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('notfound/', views.notfound, name='notfound'),
    path('<path:anything>/', RedirectView.as_view(url='/notfound/')),
]