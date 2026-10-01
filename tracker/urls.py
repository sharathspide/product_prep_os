from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('phase/<int:phase_id>/', views.phase_detail, name='phase_detail'),
    path('problem/<int:problem_id>/toggle/', views.toggle_problem, name='toggle_problem'),
    path('problem/<int:problem_id>/review/', views.review_problem, name='review_problem'),
    path('problem/<int:problem_id>/notes/', views.update_notes, name='update_notes'),
    path('session/', views.save_session, name='save_session'),
    path('reset/', views.reset_progress, name='reset_progress'),
]
