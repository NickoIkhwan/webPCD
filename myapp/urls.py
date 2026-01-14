from django.urls import path, include
import myapp.views as views
import django.contrib.admin as admin

urlpatterns = [
    path('', views.menu, name='menu'),
    path('traffic/', views.traffic_view, name='traffic'),
    path('about/', views.about, name='about'),
    path('doc/', views.Doc, name='doc'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('detect/<int:file_id>/', views.detect_stream, name='detect_stream'),
    path('api/vehicle-count/', views.get_vehicle_count, name='vehicle_count'),
    path('api/traffic-weight/', views.get_traffic_weight, name='traffic_weight'),
]