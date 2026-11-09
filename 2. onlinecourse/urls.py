from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Route for processing form exam submissions
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    
    # Route for displaying evaluated grade outcomes
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
